import matplotlib.pyplot as plt
from WavData import WavData
import numpy as np
from typing import Dict
from numpy.typing import ArrayLike

def plot_wav_data(wav_data_dict: Dict[str, WavData]):
    '''
    WavData をグラフにプロットする。
    '''
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

def plot_envelope(control_points_dict: Dict[str, ArrayLike], is_log_scale:bool=False):
    '''
    エンベロープをグラフにプロットする。
    '''
    if not type(control_points_dict) is dict:
        raise(Exception(f"Parameter 'control_points_dict' is not dict({type(control_points_dict)})"))
    for label, control_points in control_points_dict.items():
        if not type(control_points) is np.ndarray:
            raise(Exception(f"Unexpected type({type(control_points)})"))
        if control_points.ndim != 2:
            raise(Exception(f"Unexpected dimension(expected=2, actual={control_points.ndim})"))
        if control_points.shape[1] < 2:
            raise(Exception(f"Unexpected shape(expected=greater equal than 2, actual={control_points.shape[1]})"))            
        plt.scatter(control_points[0,:], control_points[1,:], label=label, linewidth=0.5)
    plt.xlabel('# of samples')
    plt.ylabel('magnitude')
    if is_log_scale:
        plt.yscale('log')
    plt.legend()
    plt.show()
    