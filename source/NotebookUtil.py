import matplotlib.pyplot as plt
from WavData import WavData
import numpy as np

def plot_wav_data(wav_data_dict):
    if not type(wav_data_dict) is dict:
        plot_wav_data({'no name': wav_data_dict})
        return
    for label, wav_data in wav_data_dict.items():
        samples = None
        if type(wav_data) is WavData:
            samples = wav_data.samples
        elif type(wav_data) is np.ndarray:
            samples = wav_data
        else:
            raise(Exception(f"Unknown type({type(wav_data)})"))
        if len(samples.shape) > 1:
            samples = samples[0]
        plt.plot(samples, label=label, linewidth=0.5)
    plt.xlabel('# of samples')
    plt.ylabel('magnitude')
    plt.ylim(-1.2, +1.2)
    plt.legend()
    plt.show()
