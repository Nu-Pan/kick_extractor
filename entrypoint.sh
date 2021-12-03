#!/bin/bash

# https://qiita.com/yohm/items/047b2e68d008ebb0f001

NEW_USER_ID=${HOST_UID:-9001}
NEW_GROUP_ID=${HOST_UID:-9001}

if [ $(id -u $USER_NAME) -ne $NEW_USER_ID ]; then
    usermod -d /home/$USER_NAME -u $NEW_USER_ID -o -m $USER_NAME
fi
if [ $(id -g $USER_NAME) -ne $NEW_GROUP_ID ]; then
    groupmod -g $NEW_GROUP_ID $USER_NAME
fi

exec /usr/sbin/gosu $USER_NAME "$@"

