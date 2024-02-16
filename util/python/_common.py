import subprocess
from pathlib import Path
from typing import List, Tuple, Any
from enum import IntEnum, auto
from datetime import datetime

# パス（内部利用）
_SELF_FILE_PATH = Path(__file__)


#　パス（外部公開）
PROJECT_DIR_PATH = _SELF_FILE_PATH.parents[2]
PROJECT_NAME = PROJECT_DIR_PATH.name

class LL(IntEnum):
    E = 0  # ERROR
    I = 1  # INFO
    T = 2  # TRACE

LL_TO_STR = [
    'ERROR',
    'INFO ',
    'TRACE'
]

LL_FILTER_LEVEL = LL.I


def flatten_list(nested_list: list) -> list:
    '''
    任意の深さの入れ子になったリストを平坦化する
    '''
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))  # 再帰呼び出し
        else:
            flat_list.append(item)
    return flat_list


def set_log_filter_level(log_level: LL) -> None:
    LL_FILTER_LEVEL = log_level


def log(
    log_level: LL,
    message: Any
) -> None:
    if log_level > LL_FILTER_LEVEL:
        return
    if type(message) is not str:
        message = str(message)
    log_level_text = LL_TO_STR[log_level]
    datetime_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(f'[{log_level_text}][{datetime_text}] {message}')


def run(
    args: str,
    expected_return_code: List[int] = [0],
    silence: bool = False
) -> None:
    '''
    コマンド args を実行する。
    実行結果（戻り値）が expected_return_code ではない場合は例外を投げる。
    '''
    # コマンドを整形・ダンプ
    args = flatten_list(args)
    args = [i for i in args if i is not None]
    args = [i if type(i) is str else str(i) for i in args]
    log(LL.I, ' '.join(args))

    # コマンドを実行
    if silence:
        result = subprocess.run(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    else:
        result = subprocess.run(args)

    # 期待する引数でなければ例外を投げる
    if type(expected_return_code) is not list:
        expected_return_code = [expected_return_code]
    if result.returncode not in expected_return_code:
        raise Exception({
            'reason': 'Failed to subprocess.run',
            'expected': expected_return_code,
            'actual': result.returncode,
            'args': args
        })
    
    # 正常終了
    return


def get_id() -> Tuple[int, int]:
    '''
    このスクリプトを実行しているユーザーの UID, GID, ユーザー名, グループ名 を取得する
    '''
    def run_capture(args):
        return subprocess.run(args, capture_output=True).stdout.decode().replace('\n', '')
    uid = int(run_capture(['id', '-u']))
    gid = int(run_capture(['id', '-g']))
    uname = run_capture(['id', '-un'])
    gname = run_capture(['id', '-gn'])
    return (uid, gid, uname, gname)
