#!/bin/bash

if [ ${TRAVIS_BRANCH} == "master" ]; then
    sshpass -p "${MASTER_PASS}" ssh -o "StrictHostKeyChecking no" master@oott.me "/bin/sh ~/server/build.sh"
elif [ ${TRAVIS_BRANCH} == "develop" ]; then
    sshpass -p "${DEVELOP_PASS}" ssh -o "StrictHostKeyChecking no" develop@oott.me "/bin/sh ~/server/build.sh"
elif [ ${TRAVIS_BRANCH} == "xugengtao" ]; then
    sshpass -p "${XUGENGTAO_PASS}" ssh -o "StrictHostKeyChecking no" xugengtao@oott.me "/bin/sh ~/server/build.sh"
elif [ ${TRAVIS_BRANCH} == "xuyichao" ]; then
    sshpass -p "${XUYICHAO_PASS}" ssh -o "StrictHostKeyChecking no" xuyichao@oott.me "/bin/sh ~/server/build.sh"
elif [ ${TRAVIS_BRANCH} == "liguangjun" ]; then
    sshpass -p "${LIGUANGJUN_PASS}" ssh -o "StrictHostKeyChecking no" liguangjun@oott.me "/bin/sh ~/server/build.sh"
elif [ ${TRAVIS_BRANCH} == "guoyaoxing" ]; then
    sshpass -p "${GUOYAOXING_PASS}" ssh -o "StrictHostKeyChecking no" guoyaoxing@oott.me "/bin/sh ~/server/build.sh"
fi
