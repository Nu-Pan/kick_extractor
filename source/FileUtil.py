
# numpy
import numpy as np

# scipy
from scipy.io import wavfile

# local
from WavData import WavData

def to_float64(wavdata: WavData) -> WavData:
    '''
    wav データを 64 bit float で [-1.0, 1.0) の範囲にスケーリングする。
    '''
    # float 系フォーマットの場合は変換不要なので除外
    float_kind = [
        np.float16,
        np.float32,
        np.float64
    ]
    int_kinds = [
        np.int8,
        np.int16,
        np.int32,
        np.int64
    ]
    if wavdata.samples.dtype in float_kind:
        dst_samples = wavdata.samples.astype(np.float64)
        return WavData(wavdata.sample_rate, dst_samples)
    elif wavdata.samples.dtype in int_kinds:
        # int の最大値を解決
        info = np.iinfo(wavdata.samples.dtype)
        int_max: np.ndarray = np.max([np.abs(info.min), np.abs(info.max)])
        # 変換
        dst_samples = wavdata.samples.astype(np.float64) / int_max.astype(np.float64)
        # 正常終了
        return WavData(wavdata.sample_rate, dst_samples)
    else:
        raise Exception(f"Unsupported dtype of wavdata({wavdata.samples.np.dtype})")

def load_wav_file(src_path: str) -> WavData:
    '''
    引数 path で指定された wav ファイルから波形データをロードします。
    '''
    sample_rate, samples = wavfile.read(src_path)
    wavdata = WavData(sample_rate, samples.transpose())
    return to_float64(wavdata)

def save_wav_file(dst_path: str, wavdata: WavData) -> None:
    '''
    引数 path で指定された wav ファイルに波形データをセーブします。
    '''
    wavfile.write(dst_path, wavdata.sample_rate, wavdata.samples.astype(np.float32).transpose())
