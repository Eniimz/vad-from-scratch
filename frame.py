"""
  Step 0: scaffold (I can do this — it's boilerplate)
  vad-from-scratch/
  ├── vad/
  │   ├── __init__.py
  │   ├── framing.py       # you write: split audio into frames
  │   ├── features.py      # you write: energy, ZCR per frame
  │   ├── decision.py       # you write: threshold + hysteresis + hangover
  │   └── io.py             # boilerplate: load wav, write output
  ├── cli.py                # boilerplate: argparse, wire pipeline together
  ├── tests/
  │   └── test_audio.wav    # a short real recording to test against
  └── README.md
"""
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

plot_waveform_energy_zcr(data, sample_rate, energies, zcrs, frame_duration_ms)
