init_deploy:
	. .github/workflows/deployment.sh

dagster:
	tmux send-keys -t dagster.0 "source .venv/bin/activate && dagster dev -h 0.0.0.0 -p 3001" ENTER

streamlit:
	tmux send-keys -t streamlit.0 "source .venv/bin/activate && cd app/charts && streamlit run main.py" ENTER

sleeper:
	sleep 10

deploy: init_deploy sleeper dagster streamlit

cancel_deploy:
	tmux kill-session -t streamlit & tmux kill-session -t dagster