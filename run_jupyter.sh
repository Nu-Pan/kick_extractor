#!/bin/bash

# スクリプトが配置されているディレクトリのパス
# つまりワークスペースのホーム
workspace_dir_path=$(cd $(dirname $0) && pwd)

# jupyter lab 実行コマンド
jupyer_cmd="jupyter-lab --ip=0.0.0.0 --allow-root"

# docker コンテナ名
docker_container_tag=nupan/kick_extractor

# docker コンテナ内部かどうかで分岐
if [ -e "/.dockerenv" ]; then
    # コンテナ内ならそのまま実行
    $jupyer_cmd
else
    # コンテナ外ならビルドしてコンテナ内で実行
    docker build \
        -t $docker_container_tag \
        $workspace_dir_path/
    docker run \
        --rm \
        --volume $workspace_dir_path:/kick_extractor \
        -p 8888:8888 \
        $docker_container_tag \
        $jupyer_cmd
fi

exit 0