# python
from typing import Dict
import itertools

# bokeh
from bokeh.plotting import output_notebook, figure, show
from bokeh.palettes import Colorblind
output_notebook()

# numpy
import numpy as np
from numpy.typing import ArrayLike

# local
from WavData import WavData

def generate_sample_positions_in_sec(wav_data: WavData):
    return np.linspace(
        start=0,
        stop=wav_data.length_in_sec(),
        num=wav_data.length_in_samples(),
        endpoint=False
    )

def plot_wav_data(wav_data_dict: Dict[str, WavData]):
    '''
    WavData をグラフにプロットする。
    '''
    if not type(wav_data_dict) is dict:
        plot_wav_data({'no name': wav_data_dict})
        return
    plot_colors = itertools.cycle(Colorblind[7])
    fig = figure()
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
        fig.line(generate_sample_positions_in_sec(wav_data), samples, legend_label=label, line_color=next(plot_colors))
    show(fig)

def plot_envelope(control_points_dict: Dict[str, ArrayLike], is_log_scale:bool=False):
    '''
    エンベロープをグラフにプロットする。
    '''
    if not type(control_points_dict) is dict:
        raise(Exception(f"Parameter 'control_points_dict' is not dict({type(control_points_dict)})"))
    plot_colors = itertools.cycle(Colorblind[7])
    fig = figure(y_axis_type='log' if is_log_scale else None)
    for label, control_points in control_points_dict.items():
        if not type(control_points) is np.ndarray:
            raise(Exception(f"Unexpected type({type(control_points)})"))
        if control_points.ndim != 2:
            raise(Exception(f"Unexpected dimension(expected=2, actual={control_points.ndim})"))
        if control_points.shape[1] < 2:
            raise(Exception(f"Unexpected shape(expected=greater equal than 2, actual={control_points.shape[1]})"))  
        fig.circle(control_points[0,:], control_points[1,:], legend_label=label, line_color=next(plot_colors))
    show(fig)
    