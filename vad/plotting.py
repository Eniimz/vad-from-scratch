import numpy as np
import matplotlib.pyplot as plt


def plot_waveform_energy_zcr(
    data,
    sample_rate,
    energies,
    zcrs,
    frame_duration_ms,
    speech,
    out_path="features_preview.png",
):
    time_axis = np.linspace(0, len(data) / sample_rate, num=len(data))
    frame_times = np.arange(len(energies)) * (frame_duration_ms / 1000.0)
    speech_num = [1 if s else 0 for s in speech]

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True, figsize=(12, 10))

    ax1.plot(time_axis, data, color="blue", alpha=0.7)
    ax1.set_title("Waveform")
    ax1.set_ylabel("Amplitude")

    ax2.plot(frame_times, energies, color="green")
    ax2.set_title("Energy per frame")
    ax2.set_ylabel("Energy")

    ax3.plot(frame_times, zcrs, color="orange")
    ax3.set_title("Zero-crossing rate per frame")
    ax3.set_ylabel("ZCR")

    ax4.step(frame_times, speech_num, where="post", color="purple")
    ax4.set_title("Speech (1) vs silence (0)")
    ax4.set_ylabel("Speech")
    ax4.set_ylim(-0.1, 1.2)
    ax4.set_xlabel("Time (Seconds)")

    plt.tight_layout()
    plt.savefig(out_path, dpi=120)
    plt.show()
