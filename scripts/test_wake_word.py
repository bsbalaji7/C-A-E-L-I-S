from caelis.voice.wake_word import WakeWordDetector


def main():
    detector = WakeWordDetector()

    detector.wait()

    print()
    print("SUCCESS!")
    print("Wake-word detection is working.")


if __name__ == "__main__":
    main()