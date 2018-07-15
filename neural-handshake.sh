#!/usr/bin/env bash

set -e

done_message="Handshake established"
result_message="Pair effectiveness"
lag_probability=20
lag_delay=1


BOLD=$(tput bold)
NORMAL=$(tput sgr0)
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

get_percent_color()
{
    if [ $1 -gt 66 ]
    then
        color=$GREEN
    elif [ $1 -gt 33 ]
    then
        color=$YELLOW
    else
        color=$RED
    fi
    echo $color
}
run_neural_handshake()
{
    loading_message="Establishing neural handshake between $(git config user.name)"

    progress=0

    echo -en "\n$loading_message: ${RED}${BOLD}$progress%${NORMAL}${NC}"
    sleep 1

    while [ $progress -lt 100 ]
    do
        progress=$(($progress+1))

        color=$(get_percent_color $progress)

        echo -en "\r$loading_message: ${color}${BOLD}$progress%${NORMAL}${NC}"

    

        if [ $(($RANDOM%$lag_probability)) == 0 ] || [ $progress == 100 ]
        then
            sleep $lag_delay
        else
            sleep 0.01
        fi
    done

    echo -en "\n$done_message\n"

    sleep 0.5

    pair_effectiveness=$(($RANDOM%101))

    color=$(get_percent_color $pair_effectiveness)

    echo -en "\n$result_message: ${color}${BOLD}$pair_effectiveness%${NORMAL}${NC}\n"
}

if [ $# -gt 0 ]
then
    git pair $1 $2 $3
fi

if [ $# -gt 1 ]
then
    run_neural_handshake
fi
