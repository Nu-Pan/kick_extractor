#!/bin/bash

# スクリプトが配置されているディレクトリのパス
# つまりワークスペースのホーム
workspace_dir_path=$(cd $(dirname $0) && pwd)

# 設定をロード
source $workspace_dir_path/.env

# 引数なしの場合は bash で置き換え
if [ $# -gt 1 ]; then
    exec_cmd="$@"
else
    exec_cmd="bash"
fi

# bash の場合は -it で実行
if [ "$exec_cmd"="bash" ]; then
    it_option=-it
fi

# コンテナを実行
docker run \
    $it_option \
    --rm \
    -v $workspace_dir_path:$incontainer_home \
    -p $container_port \
    --workdir $incontainer_home \
    -e PWD=$incontainer_home \
    -e LOCAL_UID=$(id -u $USER) \
    -e LOCAL_GID=$(id -g $USER) \
    $docker_container_tag \
    $exec_cmd
if [ $? -ne 0 ]; then
    exit $?
fi

# 正常終了
exit 0