import numpy as np
import soundfile as sf

from features import calculate_energy, calculate_zcr
from plotting import plot_waveform_energy_zcr
from segments import extract_segments, print_segments, save_segment_clips


def run_vad(wav_path, frame_duration_ms=30):
    data, sample_rate = sf.read(wav_path)

    if len(data.shape) > 1:
        data = data[:, 0]

    frame_size = int(sample_rate * (frame_duration_ms / 1000))
    print("Frame size: ", frame_size)

    frames = []
    for i in range(0, len(data), frame_size):
        frame = data[i : i + frame_size]

        if len(frame) < frame_size:
            frame = np.pad(frame, (0, frame_size - len(frame)), 'constant')

        frames.append(frame)

    energies = [calculate_energy(frame) for frame in frames]
    zcrs = [calculate_zcr(frame) for frame in frames]

    noise_floor = np.percentile(energies, 10)  # quietest 10% of frames, wherever they fall

    speech = []
    in_speech = False
    on_bar_threshold = noise_floor * 5   # upper limit
    off_bar_threshhold = noise_floor * 2  # lower limit

    print(f"Noise floor: {noise_floor:.4f}  ->  on={on_bar_threshold:.4f}  off={off_bar_threshhold:.4f}")

    hangover_frames = 3
    hangover_counter = 0

    onset_frames = 3
    onset_counter = 0

    for energy, zcr in zip(energies, zcrs):

        if in_speech: # talking so energy not low OR not talking & energy now low
            if energy < off_bar_threshhold:
                hangover_counter += 1
                if hangover_counter > hangover_frames:
                    in_speech = False
                    hangover_counter = 0
            else:
                hangover_counter = 0
        else: ## not talking but energy low OR not talking but energy high (flip)
            if energy > on_bar_threshold and zcr < 0.3:
                onset_counter += 1
                if onset_counter > onset_frames:
                    in_speech = True
                    hangover_counter = 0
                    onset_counter = 0
            else:
                onset_counter = 0

        speech.append(in_speech)

    total_duration_s = len(data) / sample_rate
    segments = extract_segments(speech, frame_duration_ms)
    print_segments(segments, total_duration_s)
    save_segment_clips(data, sample_rate, segments)

    plot_waveform_energy_zcr(data, sample_rate, energies, zcrs, frame_duration_ms, speech)

    return segments


if __name__ == "__main__":
    run_vad("tests/transfer_test_audio.wav")
