import os
import time
import random
from datetime import datetime, timedelta, timezone
import re

from helper.source_env import ETL_env_path
from ticktick.oauth2 import OAuth2        # OAuth2 Manager
from ticktick.api import TickTickClient   # Main Interface
from loader import new_login

from dagster import op, job, in_process_executor, OpExecutionContext

cache_path = os.path.join(ETL_env_path, '.token-oauth')
client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
username = os.environ.get('username')
password = os.environ.get('password')
redirect_uri = os.environ.get('redirect_uri')


TickTickClient._login = new_login
auth_client = OAuth2(client_id=client_id,
                    client_secret=client_secret,
                    redirect_uri=redirect_uri,
                    cache_path=cache_path
                    )
class StaleTasks():
    def __init__(self):
        self.client = TickTickClient(username, password, auth_client)

    def parse_human_friendly_time(self,input_str, context: OpExecutionContext):
        """
        Parses a human-friendly time string and returns a timedelta object.
        """
        match = re.match(r"(\d+)\s*(day|week|month|year)s?\s*ago", input_str)
        if not match:
            context.log.info(f'invalid format {input_str}; falling back to default 3 months.')
            quantity = 3
            unit = 'month'
        
        
        else:
            quantity = int(match.group(1))
            unit = match.group(2)

        if unit == "day":
            return timedelta(days=quantity)
        elif unit == "week":
            return timedelta(weeks=quantity)
        elif unit == "month":
            return timedelta(days=30 * quantity)
        elif unit == "year":
            return timedelta(days=365 * quantity)

    def add_stale_tags(self, tasks,context: OpExecutionContext, time_period="3 months ago"):
        """
        Adds a 'stale' tag to tasks if their 'dueDate' is older than the specified time period.

        Arguments:
            tasks (list): List of task dictionaries.
            time_period (str): Human-friendly time period string (e.g., '3 months ago').

        Returns:
            int: Total number of tasks flagged as 'stale'.
        """
        # Calculate the date based on the provided time period
        try:
            time_delta = self.parse_human_friendly_time(str(time_period), context)
        except ValueError as e:
            context.log.info(e)
            return 0

        cutoff_date = datetime.now(timezone.utc) - time_delta

        if len(tasks) == 0:
            raise ValueError("Could not retrieve tasks")
        tasks = [
            task for task in tasks
            if 'tags' in task and 'tickler' not in task['tags']  # Task['tags'] must be present and not include 'tickler'
            and task.get('kind') == 'TEXT'  # Task['type'] must be 'text'
            and task.get('dueDate') is None  
        ]
        if len(tasks) == 0:
            context.log.info("No tasks to process.")
            return 0

        stale_count = 0  # Initialize counter for stale tasks

        for task in tasks:
            anchor_date = datetime.strptime(task['modifiedTime'], '%Y-%m-%dT%H:%M:%S.%f%z')
            if anchor_date < cutoff_date:
                # Add 'stale' tag if not already present
                if 'stale' not in task['tags']:
                    task['tags'].append('stale')
                    self.client.task.update(task)
                    task_result = task['title'] + " | " + 'https://ticktick.com/webapp/#p/' + task['projectId'] + '/tasks/' + task['id']

                    context.log.info(f"flagged task: {task_result}")
                    stale_count += 1  # Increment counter

                    # Introduce a random cooldown
                    cooldown = random.uniform(1, 10)
                    # context.log.info(f"Sleeping for {cooldown:.2f} seconds to avoid rate limiting.")
                    time.sleep(cooldown)

        context.log.info(f'COMPELTED. Total stale tasks: {stale_count}')
        return stale_count  # Return the count of stale tasks

    def get_new_tasks(self) -> list:
        new_tasks = self.client.state['tasks']
        return new_tasks


@op
def op_add_stale_tags(context: OpExecutionContext, **kwargs):
    Stale = StaleTasks()
    new_tasks = Stale.get_new_tasks()
    Stale.add_stale_tags(new_tasks, context, kwargs)


@job(
        name="add_stale_tags",
        executor_def=in_process_executor
        )
def job_add_stale_tags():
    op_add_stale_tags()


if __name__ == "__main__":
    result = job_add_stale_tags.execute_in_process()
    if result.success:
        print("Job executed successfully.")
    else:
        print("Job execution failed.")
