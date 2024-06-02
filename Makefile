init_deploy:
	. .github/workflows/deployment.sh


dagster:
	tmux send-keys -t dagster.0 "source .venv/bin/activate && . ./env.sh && dbt parse && dagster dev -h 0.0.0.0 -p 3001" ENTER

streamlit:
	tmux send-keys -t streamlit.0 "source .venv/bin/activate && . ./env.sh && cd app/charts && streamlit run main.py" ENTER

sleeper:
	sleep 10

init_seed:
	source .venv/bin/activate && . ./env.sh &&\
	python app/helper/scaffold_seeds.py

init_dbt: source .venv/bin/activate && . ./env.sh && dbt deps && dbt compile

init_dev: init_seed init_dbt

deploy: init_deploy sleeper dagster streamlit


deploy-from-scratch: init_seed init_deploy init_dbt sleeper loader dagster streamlit

loader:
	tmux send-keys -t loader.0 "source .venv/bin/activate && source source_env.sh && cd app/ETL && python loader.py" ENTER


cancel_deploy:
	tmux kill-session -t streamlit & tmux kill-session -t dagster