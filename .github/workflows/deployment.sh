#!/bin/bash

WORKDIR=$(pwd)

. $WORKDIR/.venv/bin/activate
. $WORKDIR/bootstrap_env.sh

# Array of tmux session names
sessions=("dagster" "loader" "gtd_search")

for session in "${sessions[@]}"; do
    # Check if the session exists
    if tmux has-session -t "$session" 2>/dev/null; then
        # Session exists, kill the old one
        tmux kill-session -t "$session"
    fi
    # Create a new session
    tmux new-session -s "$session" -d
done