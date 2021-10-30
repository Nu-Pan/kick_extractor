
# numpy
import numpy as np

# scipy
from scipy.io import wavfile

# local
from WavData import WavData

def to_float64(wav_data: WavData) -> WavData:
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
    if wav_data.samples.dtype in float_kind:
        dst_samples = wav_data.samples.astype(np.float64)
        return WavData(wav_data.sample_rate, dst_samples)
    elif wav_data.samples.dtype in int_kinds:
        # int の最大値を解決
        info = np.iinfo(wav_data.samples.dtype)
        int_max: np.ndarray = np.max([np.abs(info.min), np.abs(info.max)])
        # 変換
        dst_samples = wav_data.samples.astype(np.float64) / int_max.astype(np.float64)
        # 正常終了
        return WavData(wav_data.sample_rate, dst_samples)
    else:
        raise Exception(f"Unsupported dtype of wav_data({wav_data.samples.np.dtype})")

def load_wav_file(src_path: str) -> WavData:
    '''
    引数 path で指定された wav ファイルから波形データをロードします。
    '''
    sample_rate, samples = wavfile.read(src_path)
    wav_data = WavData(sample_rate, samples.transpose())
    return to_float64(wav_data)

def save_wav_file(dst_path: str, wav_data: WavData) -> None:
    '''
    引数 path で指定された wav ファイルに波形データをセーブします。
    '''
    wavfile.write(dst_path, wav_data.sample_rate, wav_data.samples.astype(np.float32).transpose())
