#!/bin/bash
. ./.venv/bin/activate

. ./env_init.sh
. ./.env

pip install -r -q requirements.txt

# setup sessions for service
STREAMLIT="streamlit"

# Kill the existing session if it exists
tmux has-session -t $STREAMLIT 2>/dev/null

if [ $? != 0 ]; then
    # Session doesn't exist, create a new one
    tmux new-session -s $STREAMLIT -d
else
    # Session exists, kill the old one and create a new one
    tmux kill-session -t $STREAMLIT
    tmux new-session -s $STREAMLIT -d
fi




DAGSTER="dagster"

# Kill the existing session if it exists
tmux has-session -t $DAGSTER 2>/dev/null

if [ $? != 0 ]; then
    # Session doesn't exist, create a new one
    tmux new-session -s $DAGSTER -d
else
    # Session exists, kill the old one and create a new one
    tmux kill-session -t $DAGSTER
    tmux new-session -s $DAGSTER -d
fi

