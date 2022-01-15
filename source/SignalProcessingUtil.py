
# numpy
import numpy as np

# scipy
from scipy import signal

# local
from WavData import WavData

def apply_peak_filter(
    src_data: WavData,
    retaining_frequency_in_hz: float,
    bandwidth_in_hz: float
    ):
    '''
    src_data にピークフィルタを適用。
    - retaining_frequency_in_hz
        - ピーク中心周波数
    - bandwidth_in_hz
        - -3dB のロールオフになる
    '''
    # IIR ピークフィルタを設計
    b, a = signal.iirpeak(
        retaining_frequency_in_hz,
        retaining_frequency_in_hz/bandwidth_in_hz,
        src_data.sample_rate
        )
    # 順 --> 逆で同じフィルタを適用（ゼロ位相）
    dst_samples = signal.filtfilt(b, a, src_data.samples)
    # 正常終了
    return WavData(src_data.sample_rate, dst_samples)

def to_frequency(positions_in_subsample: np.ndarray, sample_rate: int, period_factor: int) -> np.ndarray:
    '''
    サブサンプル精度の「位置」の配列を元に、周波数の配列を生成する。
    '''
    periods_in_subsample = (np.roll(positions_in_subsample, -1) - positions_in_subsample)[:-1] * period_factor
    periods_in_sec = periods_in_subsample / sample_rate
    frequency_in_hz = 1.0 / periods_in_sec
    return frequency_in_hz
