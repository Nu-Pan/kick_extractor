
import json
import argparse
from pathlib import Path
from typing import List

import _common as com
from _common import LL, log
from docker_build import docker_build
from docker_stop import docker_stop

CONFIG_FILE_PATH = com.PROJECT_DIR_PATH / 'config.json'
DEVCON_DIR_PATH = com.PROJECT_DIR_PATH / '.devcontainer'

def docker_run(has_attach: bool, has_bash: bool):
    # 先にビルド
    docker_build()

    # 先に既存コンテナを止める
    docker_stop()

    # bash ログイン設定
    exec_cmd = (
        'bin/bash' if has_bash
        else None
    )

    # アタッチ設定
    attach = (
        '-it' if has_attach
        else '-d'
    )

    # 設定ファイルをロード
    config_body = json.loads(open(CONFIG_FILE_PATH, 'r').read())
    port_int: List[int] = config_body['port']

    # ポート設定をテキストに展開
    port_args = [['-p', f'{p}:{p}'] for p in port_int]

    # uid, gid を解決
    uid, gid, _, _ = com.get_id()

    # docker run
    com.run([
        'docker', 'container', 'run',
        '--name', com.PROJECT_NAME,
        attach,
        '--rm',
        '-v', f'{com.PROJECT_DIR_PATH}:{com.PROJECT_DIR_PATH}',
        port_args,
        '--workdir', com.PROJECT_DIR_PATH,
        '-u', f'{uid}:{gid}',
        com.PROJECT_NAME,
        exec_cmd
    ])

if __name__=='__main__':
    # ログレベル設定
    com.set_log_filter_level(LL.I)

    # 引数をパース
    parser = argparse.ArgumentParser(
        prog=Path(__file__).stem,
        description='Run docker container.'
    )
    parser.add_argument('-a', '--attach', action='store_true')
    parser.add_argument('-b', '--bash', action='store_true')
    args = parser.parse_args()
    
    # コマンド実行
    docker_run(args.attach, args.bash)

    # 正常終了
    exit(0)
