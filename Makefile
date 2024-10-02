init_deploy:
	tmux new-session -s dagster -d
	tmux new-session -s loader -d
	tmux new-session -s gtd_search -d

init_seed:
	. ./.venv/bin/activate
	. ./bootstrap_env.sh
	python app/helper/scaffold_seeds.py

init_dbt: 
	. ./.venv/bin/activate 
	. ./bootstrap_env.sh 
	dbt deps 
	dbt compile

init_dev: init_seed init_dbt


sleeper:
	sleep 10

dagster:
	tmux send-keys -t dagster.0 'echo' ENTER
	tmux send-keys -t dagster.0 '. ./.venv/bin/activate && . ./bootstrap_env.sh && dagster dev -m ETL -h 0.0.0.0 -p 60001' ENTER


loader:
	tmux send-keys -t loader.0 'echo' ENTER
	tmux send-keys -t loader.0 '. ./.venv/bin/activate && . ./bootstrap_env.sh && cd app/ETL && python loader.py' ENTER

gtd_search:
	tmux send-keys -t gtd_search.0 'echo' ENTER
	tmux send-keys -t gtd_search.0 '. ./.venv/bin/activate && . ./bootstrap_env.sh && cd app/search_GUI && python app.py' ENTER


deploy-from-scratch: init_seed init_deploy init_dbt sleeper loader dagster

# command after each reboot the vm
up: init_deploy dagster loader

deploy: dagster_helper dagster


loader_helper:
	tmux kill-session -t loader && tmux new-session -d -s loader

dagster_helper:
	tmux kill-session -t dagster && tmux new-session -d -s dagster

loader_rerun: loader_helper loader


