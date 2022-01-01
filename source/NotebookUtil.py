# python
from typing import List, Union
import itertools
from enum import Enum
import collections

# bokeh
from bokeh.plotting import output_notebook, figure, show
from bokeh.palettes import Colorblind
output_notebook()

# numpy
import numpy as np
from numpy.typing import ArrayLike

# local
from WavData import WavData

def _generate_sample_positions_in_sec(wavdata: WavData) -> np.linspace:
    return np.linspace(
        start=0,
        stop=wavdata.length_in_sec(),
        num=wavdata.length_in_samples(),
        endpoint=False
    )

def _flatten(l):
    '''
    https://note.nkmk.me/python-list-flatten/
    '''
    for el in l:
        if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
            yield from _flatten(el)
        else:
            yield el

def _to_frequency(positions_in_subsample: np.ndarray, sample_rate: int, period_factor: int) -> np.ndarray:
    '''
    サブサンプル精度の「位置」の配列を元に、周波数の配列を生成する。
    '''
    periods_in_subsample = (np.roll(positions_in_subsample, -1) - positions_in_subsample)[:-1] * period_factor
    periods_in_sec = periods_in_subsample / sample_rate
    frequency_in_hz = 1.0 / periods_in_sec
    return frequency_in_hz

class PlotType(Enum):
    '''
    プロットの種類を表す列挙値。
    '''
    LINE = 1
    DOT = 2

class PlotDesc:
    '''
    プロットの内容を記述するクラス。
    '''
    def __init__(self):
        self.label: str = None
        self.array_y: np.ndarray = None
        self.array_x: np.ndarray = None
        self.type: PlotType = None

def describe_wavdata(label: str, wavdata: WavData) -> List[PlotDesc]:
    '''
    WavData を折れ線グラフを記述する。
    '''
    # マルチチャンネルの場合はバラす
    if wavdata.samples.ndim > 1:
        return _flatten([
            describe_wavdata(label+f'[{i}]', WavData(wavdata.sample_rate, wavdata.samples[i,:].flatten()))
            for i in range(wavdata.samples.shape[0])
        ])
    # 記述
    desc = PlotDesc()
    desc.label = label
    desc.array_y = wavdata.samples
    desc.array_x = _generate_sample_positions_in_sec(wavdata)
    desc.type = PlotType.LINE
    return [desc]

def describe_scatter(label: str, points_y: np.ndarray, points_x: np.ndarray) -> List[PlotDesc]:
    '''
    ２つの ndarray を散布図として記述する。
    '''
    # サイズチェック
    if points_y.shape != points_x.shape:
        raise Exception(f"Shape of points_y and points_x has missmatched({points_y.shape} v.s. {points_x.shape})")
    # マルチチャンネルの場合はバラす
    if points_y.ndim > 1 or points_x.ndim > 1:
        return _flatten([
            describe_scatter(label+f'[{i}]', points_y[i,:], points_x[i:])
            for i in range(points_y.shape[0])
        ])
    # 記述
    desc = PlotDesc()
    desc.label = label
    desc.array_y = points_y
    desc.array_x = points_x
    desc.type = PlotType.DOT
    return [desc]

def describe_frequency(label: str, positions_in_subsample: np.ndarray, sample_rate: int, period_factor: int) -> List[PlotDesc]:
    '''
    positions_in_subsample を周波数に変換シた上で散布図として記述する。
    '''
    # 周波数化
    frequencies_in_hz = _to_frequency(
        positions_in_subsample,
        sample_rate,
        period_factor
    )
    # 散布図に流す
    return describe_scatter(
        label,
        frequencies_in_hz,
        positions_in_subsample[:-1]
    )

def describe_dot_on_wavdata(label: str, wavdata: WavData, positions_in_subsample: np.ndarray) -> List[PlotDesc]:
    '''
    wavdata 上の位置 positions_in_sample の点を散布図として記述する。
    '''
    # wavdata 上の位置を線形補間しつつ解決
    positions_in_sample = positions_in_subsample.astype(int)
    sub_position_offsets = positions_in_subsample - positions_in_sample
    sub_magnitude_offsets = (wavdata.samples[positions_in_sample+1] - wavdata.samples[positions_in_sample+0]) * sub_position_offsets
    # 散布図に流す
    return describe_scatter(
        label,
        wavdata.samples[positions_in_sample] + sub_magnitude_offsets,
        positions_in_subsample/wavdata.sample_rate
    )    

def plot(descs :Union[PlotDesc, List[PlotDesc]], is_log_scale:bool=False) -> None:
    '''
    descs の指定どおりにグラフを描画・表示する。
    '''
    # 第一引数をリスト化
    if not type(descs) is list:
        return plot([descs], is_log_scale)
    # プロット設定
    plot_colors = itertools.cycle(Colorblind[7])
    fig = figure(y_axis_type='log' if is_log_scale else None)
    # 一本づつ描画
    for d in _flatten(descs):
        d: PlotDesc
        if not type(d) is PlotDesc:
            raise Exception(f"Invalid type of d({type(d)})")
        args = {'x': d.array_x, 'y':d.array_y, 'legend_label':d.label, 'color':next(plot_colors)}
        if d.type is PlotType.LINE:
            fig.line(**args)
        elif d.type is PlotType.DOT:
            fig.circle(**args)
        else:
            raise Exception(f"Unknown PlotType({d.type})")
    # 表示
    show(fig)
