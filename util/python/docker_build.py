
import _common as com
from _common import log, LL

CONFIG_FILE_PATH = com.PROJECT_DIR_PATH / 'config.json'
DEVCON_DIR_PATH = com.PROJECT_DIR_PATH / '.devcontainer'

def docker_build() -> None:
    # id を解決
    user_id, group_id, user_name, group_name = com.get_id()
    id_dict = {
        'USER_ID': user_id,
        'GROUP_ID': group_id,
        'USER_NAME': user_name,
        'GROUP_NAME': group_name
    }
    id_args = [['--build-arg', f'{k}={v}'] for k, v in id_dict.items()]
    log(LL.T, f'id_args = {id_args}')

    # ビルドコマンドを実行
    com.run([
        'docker', 'image', 'build',
        '-t', com.PROJECT_NAME,
        id_args,
        com.PROJECT_DIR_PATH
    ])

    # 正常終了
    return 0

if __name__=='__main__':
    # ログレベル設定
    com.set_log_filter_level(LL.I)
    
    # コマンド実行
    docker_build()

    # 正常終了
    exit(0)
