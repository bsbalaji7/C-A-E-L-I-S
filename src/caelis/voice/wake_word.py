import numpy as np
import sounddevice as sd
import openwakeword
from openwakeword.model import Model


class WakeWordDetector:
    def __init__(self):
        print("[WAKE] Initializing wake-word engine...")

        self.sample_rate = 16000
        self.block_size = 1280
        self.threshold = 0.5

        model_path = openwakeword.MODELS["hey_jarvis"]["model_path"]

        self.model = Model(
            wakeword_models=[model_path]
        )

        print("[WAKE] Engine ready.")
        print("[WAKE] Temporary wake phrase: Hey Jarvis")

    def wait(self) -> bool:
        self.model.reset()

        print()
        print("[WAKE] STANDBY")
        print("[WAKE] Say: KAY-liss")

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            blocksize=self.block_size,
        ) as stream:

            while True:
                audio, overflowed = stream.read(
                    self.block_size
                )

                if overflowed:
                    continue

                audio = np.squeeze(audio)

                predictions = self.model.predict(audio)

                for model_name, score in predictions.items():
                    if score >= self.threshold:
                        print()
                        print(
                            f"[WAKE] DETECTED: "
                            f"{model_name} "
                            f"score={score:.2f}"
                        )

                        return True