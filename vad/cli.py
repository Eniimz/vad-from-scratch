import argparse

from framing import run_vad


def main():
    parser = argparse.ArgumentParser(description="Detect speech segments in a wav file.")
    parser.add_argument("wav_path", help="path to a wav file")
    parser.add_argument("--frame-ms", type=int, default=30, help="frame duration in ms (default: 30)")
    args = parser.parse_args()

    run_vad(args.wav_path, frame_duration_ms=args.frame_ms)


if __name__ == "__main__":
    main()
