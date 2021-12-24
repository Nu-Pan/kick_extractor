from glob import glob
from os import path
import os

# local
from WavData import WavData
import FileUtil

def main_function(wavdata: WavData) -> WavData:
    return wavdata


if __name__ == '__main__':
    prev_result_paths = glob('data/*_out.wav')
    for prev_result_path in prev_result_paths:
        os.remove(prev_result_path)
    src_paths = glob('data/*.wav')
    for src_path in src_paths:
        # wav ファイルロード
        wavdata = FileUtil.load_wav_file(src_path)
        # フィルタを適用
        wavdata = main_function(wavdata)
        # wav ファイルセーブ
        src_basename = path.basename(src_path)
        dst_path = f'data/{src_basename}_out.wav'
        FileUtil.save_wav_file(dst_path, wavdata)
    # 正常終了     
    exit(0)
