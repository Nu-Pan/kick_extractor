
from typing import Tuple
from glob import glob
from os import path

import numpy as np

from scipy.io import wavfile

if __name__ == '__main__':
    src_paths = glob('data/*.wav')
    for src_path in src_paths:
        # ファイルロード
        sample_rate: int
        samples: np.ndarray
        sample_rate, samples = wavfile.read(src_path)
        # ファイルセーブ
        src_basename = path.basename(src_path)
        dst_path = f'data/{src_basename}_out.wav'
        wavfile.write(dst_path, sample_rate, samples)
    # 正常終了     
    exit(0)
