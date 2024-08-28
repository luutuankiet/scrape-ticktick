init_deploy:
	. .github/workflows/deployment.sh


dagster:
	tmux send-keys -t dagster.0 ". ./.venv/bin/activate && . ./bootstrap_env.sh && dagster dev -m ETL -h 0.0.0.0 -p 60001" ENTER

sleeper:
	sleep 10

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

deploy: init_deploy sleeper dagster streamlit


deploy-from-scratch: init_seed init_deploy init_dbt sleeper loader dagster streamlit

loader:
	tmux send-keys -t loader.0 ". ./.venv/bin/activate && . ./bootstrap_env.sh && cd app/ETL && python loader.py" ENTER


cancel_deploy:
	tmux kill-session -t streamlit & tmux kill-session -t dagster

loader_helper:
	tmux kill-session -t loader && tmux new-session -d -s loader

loader_rerun: loader_helper loader


# command after each reboot the vm
up: init_deploy sleeper dagster loader