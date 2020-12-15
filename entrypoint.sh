#!/bin/sh

set -e

echo "sleep 10 ..."
sleep 10

if [ -f requirements.txt ]; then
    echo "pip install -r requirements.txt ..."
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
fi

aerich upgrade

echo "exec $@ ..."
exec $@
