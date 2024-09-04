#!/usr/bin/env bash
set -e

TIMEOUT=15
HOST="$1"
PORT="$2"

echo "Waiting for $HOST:$PORT to be available..."

until (echo > /dev/tcp/"$HOST"/"$PORT") &> /dev/null; do
    sleep 1
    TIMEOUT=$(($TIMEOUT-1))
    if [ $TIMEOUT -eq 0 ]; then
        echo "Timeout while waiting for $HOST:$PORT"
        exit 1
    fi
done

echo "$HOST:$PORT is available"
exec "${@:3}"
