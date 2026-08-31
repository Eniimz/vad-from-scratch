import numpy as np
import soundfile as sf

from features import calculate_energy, calculate_zcr
from plotting import plot_waveform_energy_zcr


data, sample_rate = sf.read("tests/test_audio.wav")


if len(data.shape)> 1:
    data = data[:, 0]

frame_duration_ms = 30  #30 ms
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

speech = []
in_speech = False
on_bar_threshold = 0.12 #upper limit
off_bar_threshhold = 0.04 #lower limit

hangover_frames = 3
hangover_counter = 0

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
        if energy > on_bar_threshold and zcr < 0.35:
            in_speech = True
            hangover_counter = 0
    
    speech.append(in_speech)

plot_waveform_energy_zcr(data, sample_rate, energies, zcrs, frame_duration_ms, speech)
