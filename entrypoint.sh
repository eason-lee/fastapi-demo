#!/bin/sh

set -e

aerich upgrade

echo "exec $@ ..."
exec $@
