#!/bin/bash

# スクリプトが配置されているディレクトリのパス
# つまりワークスペースのホーム
workspace_dir_path=$(cd $(dirname $0) && pwd)

# 設定をロード
source $workspace_dir_path/.env

# コンテナをビルド
docker build \
    -t $docker_container_tag \
    $workspace_dir_path/
if [ $? -ne 0 ]; then
    exit $?
fi

# 正常終了
exit 0
