import os

import soundfile as sf


def extract_segments(speech, frame_duration_ms):
    """Turn a per-frame speech/silence list into (start_sec, end_sec) segments."""
    segments = []
    start_frame = None

    for i, is_speech in enumerate(speech):
        if is_speech and start_frame is None:
            start_frame = i
        elif not is_speech and start_frame is not None:
            segments.append((start_frame, i))
            start_frame = None

    if start_frame is not None:
        segments.append((start_frame, len(speech)))

    frame_duration_s = frame_duration_ms / 1000.0
    return [
        (start * frame_duration_s, end * frame_duration_s)
        for start, end in segments
    ]


def print_segments(segments, total_duration_s):
    if not segments:
        print("No speech detected.")
        return

    total_speech_s = sum(end - start for start, end in segments)

    print(f"\n{len(segments)} speech segment(s) detected:")
    for start, end in segments:
        print(f"  {start:6.2f}s -> {end:6.2f}s  ({end - start:.2f}s)")

    pct = 100 * total_speech_s / total_duration_s
    print(f"\nTotal speech: {total_speech_s:.2f}s / {total_duration_s:.2f}s ({pct:.1f}%)")


def save_segment_clips(data, sample_rate, segments, out_dir="output_segments"):
    os.makedirs(out_dir, exist_ok=True)

    for f in os.listdir(out_dir):
        os.remove(os.path.join(out_dir, f))

    for i, (start, end) in enumerate(segments):
        start_sample = int(start * sample_rate)
        end_sample = int(end * sample_rate)
        clip = data[start_sample:end_sample]

        path = os.path.join(out_dir, f"segment_{i:02d}_{start:.2f}s-{end:.2f}s.wav")
        sf.write(path, clip, sample_rate)

    print(f"Saved {len(segments)} clip(s) to {out_dir}/ — play them to check they're really speech")
