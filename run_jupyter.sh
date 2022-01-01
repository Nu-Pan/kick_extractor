#!/bin/bash

# スクリプトが配置されているディレクトリのパス
# つまりワークスペースのホーム
workspace_dir_path=$(cd $(dirname $0) && pwd)

# 設定をロード
source $workspace_dir_path/.env

# docker コンテナ内部かどうかで分岐
if [ -e "/.dockerenv" ]; then
    # コンテナ内ならそのまま実行
    $jupyter_cmd
    if [ $? -ne 0 ]; then
        echo "error: $jupyter_cmd"
        exit $?
    fi
else
    # コンテナ外ならコンテナをビルド・実行
    $workspace_dir_path/docker_build.sh
    if [ $? -ne 0 ]; then
        echo "error: $workspace_dir_path/docker_build.sh"
        exit $?
    fi
    $workspace_dir_path/docker_run.sh $jupyter_cmd
    if [ $? -ne 0 ]; then
        echo "error: $workspace_dir_path/docker_run.sh $jupyter_cmd"
        exit $?
    fi
fi

# 正常終了
echo "ok"
exit 0