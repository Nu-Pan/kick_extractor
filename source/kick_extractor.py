from glob import glob
from os import path
import os

# local
from WavData import WavData
import FileUtil

def main_function(wav_data: WavData) -> WavData:
    return wav_data


if __name__ == '__main__':
    prev_result_paths = glob('data/*_out.wav')
    for prev_result_path in prev_result_paths:
        os.remove(prev_result_path)
    src_paths = glob('data/*.wav')
    for src_path in src_paths:
        # wav ファイルロード
        wav_data = FileUtil.load_wav_file(src_path)
        # フィルタを適用
        wav_data = main_function(wav_data)
        # wav ファイルセーブ
        src_basename = path.basename(src_path)
        dst_path = f'data/{src_basename}_out.wav'
        FileUtil.save_wav_file(dst_path, wav_data)
    # 正常終了     
    exit(0)
