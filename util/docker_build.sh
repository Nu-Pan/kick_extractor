#!/bin/bash

# スクリプトが配置されているディレクトリのパス
self_dir=$(cd $(dirname $0) && pwd)
self_name=$(basename $0)
self_stem=${self_name%.*}
project_dir=$self_dir/..

# プロジェクトディレクトリに移動
pushd $project_dir > /dev/null 2>&1

# スクリプトを実行
python3 $self_dir/python/$self_stem.py $@
if [ $? -ne 0 ]; then
    exit 1
fi

# 正常終了
exit 0
