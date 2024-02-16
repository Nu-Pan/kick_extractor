
import json
import argparse
from pathlib import Path
from typing import List

import _common as com
from _common import LL, log
from docker_build import docker_build

CONFIG_FILE_PATH = com.PROJECT_DIR_PATH / 'config.json'
DEVCON_DIR_PATH = com.PROJECT_DIR_PATH / '.devcontainer'

def docker_stop():
    com.run([
            'docker', 'container', 'stop',
            com.PROJECT_NAME
        ],
        expected_return_code=[0, 1],
        silence=True
    )

if __name__=='__main__':
    # ログレベル設定
    com.set_log_filter_level(LL.I)
    
    # コマンド実行
    docker_stop()

    # 正常終了
    exit(0)
