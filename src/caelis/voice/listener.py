import os
import tempfile
import time

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel


class VoiceListener:
    def __init__(self):
        print("[STT] Initializing multilingual Whisper...")

        self.sample_rate = 16000

        # Better accuracy than tiny while still reasonable
        # for Ryzen 3 5300U + 8 GB RAM.
        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8",
            cpu_threads=4,
            num_workers=1,
        )

        print("[STT] Whisper ready.")

    def listen(self) -> str | None:
        try:
            print()
            print("[VOICE] Listening...")

            audio = self._record_until_silence()

            if audio is None:
                print("[VOICE] No speech detected.")
                return None

            return self._transcribe(audio)

        except KeyboardInterrupt:
            raise

        except Exception as error:
            print(f"[STT ERROR] {error}")
            return None

    def _record_until_silence(self):
        """
        Record microphone audio until the user stops speaking.
        """

        block_duration = 0.1

        block_size = int(
            self.sample_rate * block_duration
        )

        # Increase/decrease this later depending on
        # your microphone/background noise.
        silence_threshold = 0.012

        # Fast response after user stops speaking.
        silence_duration = 0.7

        # Maximum command duration.
        max_duration = 10

        required_silent_blocks = int(
            silence_duration / block_duration
        )

        max_blocks = int(
            max_duration / block_duration
        )

        audio_blocks = []

        speech_started = False
        silent_blocks = 0

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            blocksize=block_size,
        ) as stream:

            for _ in range(max_blocks):
                block, overflowed = stream.read(
                    block_size
                )

                if overflowed:
                    print("[VOICE] Microphone overflow.")

                volume = float(
                    np.sqrt(
                        np.mean(
                            np.square(block)
                        )
                    )
                )

                if volume > silence_threshold:
                    speech_started = True
                    silent_blocks = 0

                elif speech_started:
                    silent_blocks += 1

                if speech_started:
                    audio_blocks.append(
                        block.copy()
                    )

                if (
                    speech_started
                    and silent_blocks
                    >= required_silent_blocks
                ):
                    break

        if not speech_started:
            return None

        if not audio_blocks:
            return None

        return np.concatenate(
            audio_blocks,
            axis=0,
        )

    def _transcribe(self, audio):
        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False,
            ) as temp_file:
                temp_path = temp_file.name

            audio_int16 = np.int16(
                np.clip(
                    audio,
                    -1.0,
                    1.0,
                )
                * 32767
            )

            write(
                temp_path,
                self.sample_rate,
                audio_int16,
            )

            print("[STT] Understanding...")

            start_time = time.perf_counter()

            # IMPORTANT:
            # Use temp_path here, not audio_path.
            segments, info = self.model.transcribe(
                temp_path,

                # Fast decoding.
                beam_size=1,
                best_of=1,
                temperature=0,

                # Each CAELIS command is independent.
                condition_on_previous_text=False,

                # Filter silence/noise.
                vad_filter=True,

                vad_parameters={
                    "min_silence_duration_ms": 400,
                },
            )

            text_parts = []

            for segment in segments:
                segment_text = segment.text.strip()

                if segment_text:
                    text_parts.append(
                        segment_text
                    )

            text = " ".join(
                text_parts
            ).strip()

            elapsed = (
                time.perf_counter()
                - start_time
            )

            print(
                f"[STT] Transcription time: "
                f"{elapsed:.2f}s"
            )

            if not text:
                print(
                    "[STT] Speech not understood."
                )
                return None

            whisper_language = getattr(
                info,
                "language",
                "unknown",
            )

            probability = getattr(
                info,
                "language_probability",
                0.0,
            )

            # This is only Whisper's detected language.
            # CAELIS detector.py should decide whether
            # the resulting text is English/Thanglish.
            print(
                "[STT] Whisper language: "
                f"{whisper_language} "
                f"({probability:.2f})"
            )

            print(f"BS: {text}")

            return text

        except Exception as error:
            print(
                f"[STT TRANSCRIBE ERROR] {error}"
            )
            return None

        finally:
            if (
                temp_path
                and os.path.exists(temp_path)
            ):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass