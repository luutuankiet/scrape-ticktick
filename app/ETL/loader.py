# a standalone job to run once and stay on for the duration of the machine.
# this helps retain one tick tick api call in the duration.

#%%
import secrets
from ticktick.oauth2 import OAuth2        # OAuth2 Manager
from ticktick.api import TickTickClient   # Main Interface

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0"
X_DEVICE_ = '{"platform":"web","os":"OS X","device":"Firefox 95.0","name":"unofficial api!","version":4531,' \
                '"id":"6490' + secrets.token_hex(10) + '","channel":"website","campaign":"","websocket":""}'

TickTickClient.HEADERS = {'User-Agent': USER_AGENT,
               'x-device': X_DEVICE_}

# per this issue : https://github.com/lazeroffmichael/ticktick-py/issues/42

from os import environ
import os
import json
from datetime import datetime, timedelta,timezone
import logging
from logging.handlers import TimedRotatingFileHandler
import time
import sys; sys.path.append('..') # to allow import helper which is 1 dir away
from helper.source_env import dotenv_path,raw_path
import asyncio

#%%

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# Configure logging with a TimedRotatingFileHandler for log rotation
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = TimedRotatingFileHandler(filename='app.log', when='D', backupCount=0)
log_handler.setFormatter(log_formatter)
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)


cache_path=os.path.join(dotenv_path,'.token-oauth')

client_id=environ.get('client_id')
client_secret=environ.get('client_secret')
username=environ.get('username')
password=environ.get('password')
redirect_uri=environ.get('redirect_uri')

tasks_file_path = os.path.join(raw_path,'tasks_raw.json')
lists_file_path = os.path.join(raw_path,'lists_raw.json')
folders_file_path = os.path.join(raw_path,'folders_raw.json')

default_start = datetime(2022, 7, 23,tzinfo=timezone.utc)
date_format = '%Y-%m-%dT%H:%M:%S.%f%z'

#%%



def new_login(self, username, password):
    url = self.BASE_URL + 'user/signon?wc=true&remember=true'
    user_info = {
        'username': username,
        'password': password,
    }
    parameters = {
        'wc': True,
        'remember': True
    }

    response = self.http_post(url, json=user_info, params=parameters, headers=self.HEADERS)
    self.access_token = response['token']
    self.cookies['t'] = self.access_token




cutoff_date = datetime(2024, 4, 1, tzinfo=timezone.utc)

def _delete_tasks(start=None, end=cutoff_date, full_load=True,**kwargs):
    """_summary_
    a utility to delete completed tasks. make sure you archive the data before doing this operation!
    usage : specify the cutoffdate, the start date, then _delete_tasks()
    """
    
    logging.info('start deleting tasks')

    if full_load:
        current_date=default_start
    elif not full_load: 
        current_date=start
    while current_date <= end+timedelta(days=1):
        client = kwargs.get('client')
        tasks=client.task.get_completed(current_date)
        if tasks != []:
            deleted = client.task.delete(tasks)
            logging.info(f'deleted {len(deleted)} tasks from {current_date}. next interation...')
        current_date += timedelta(days=1)
    print('all specified tasks deleted.')







#%%
def deduplicate(source) -> list:
    """
    checks each item and remove duplicated
    """
    unique_items={}
    unique_list=[]

    for item in source:
        item_id=item.get("id")

        if item_id not in unique_items:
            unique_list.append(item)
            unique_items[item_id]=True
    return unique_list


def _get_completed_tasks(start=None, end=datetime.now(timezone.utc), full_load=True):
    """_summary_
    returns a json string
    internal func - uses tickpy to grab completed tasks from start > end.
    `start` has a default value 2022/07/23 which is the start of my ticktick interactions
    `end` defaults to the runtime date.

    Returns:
        list: all the completed tasks in the interval.
    """
    
    completed_tasks=[] 
    logging.info('start loading tasks')

    if full_load:
        current_date=default_start
    elif not full_load: 
        current_date=start
    while current_date <= end+timedelta(days=1):
        tasks=client.task.get_completed(current_date)
        if tasks != []:
            for task in tasks:
                completed_tasks.append(task)
            logging.info(f'loaded {len(tasks)} new tasks from {current_date}. next interation...')
            
        current_date += timedelta(days=1)
    return completed_tasks

def get_completed_task() -> list:
    """
    returns a list the full completed tasks and utilize existing file as cache if available.
    """
    try:
        with open(tasks_file_path,'r') as f:
            cached=json.load(f)
            cached_completed=[item for item in cached if 'completedTime' in item]
            last_cached_date=[item['completedTime'] for item in cached if 'completedTime' in item]
            last_cached_date=max(last_cached_date)
            last_cached_date=datetime.strptime(last_cached_date,date_format)
            last_cached_date=last_cached_date - timedelta(days=1)
            full_load=False
            metadata=last_cached_date
    except FileNotFoundError:
        logging.info('no cache found. doing full load...')
        cached_completed=[]
        last_cached_date=None
        full_load=True
        metadata=None
    
    # checks existing and append to cached list 
    net_new=_get_completed_tasks(start=last_cached_date,full_load=full_load)
    today = datetime.today()
    new_today = client.task.get_completed(today)
    net_new += new_today # manual fix missing today data while loops loads

    # concatenate final completed list
    all_completed_tasks=net_new+cached_completed
    all_completed_tasks=deduplicate(all_completed_tasks)
    return all_completed_tasks,metadata
    

def get_new_tasks() -> list:
    new_tasks=client.state['tasks']
    return new_tasks


def extract_json():
    # task
    client.task._client.sync()
    new=get_new_tasks()
    logging.info(f'new tasks : {len(new)}')
    completed,metadata=get_completed_task()
    logging.info(f'completed tasks : {len(completed)}. cached from : {metadata}')
    all_tasks=new+completed
    logging.info(f'all tasks : {len(all_tasks)}')
    


    # list
    lists = client.state['projects']

    # folders
    folders = client.state['project_folders']

    
    return all_tasks,folders,lists



def _dump_to_file(source:list, target:str):
    """
    takes source then dumps to json raw file 
    """

    with open(target,'w') as f:
        json.dump(source,f,indent=4,)

def dump_to_file(extract_json):
    all_tasks,folders,lists = extract_json
    _dump_to_file(lists,lists_file_path)
    _dump_to_file(folders,folders_file_path)
    _dump_to_file(all_tasks,tasks_file_path)
    return None


# Path to the flag file
FLAG_FILE = 'force_sync.flag'

# Introduce a global variable to track the synchronization state
is_sync_running = False

# Modify the trigger_sync function to prioritize the current instance
def trigger_sync():
    global is_sync_running
    
    if is_sync_running:
        # If a synchronization process is already running, prioritize the current instance
        logging.info('Synchronization process is already running. Priority given to current instance.')
        return
    
    try:
        # Set the flag to indicate that a synchronization process is running
        is_sync_running = True
        
        # Start the synchronization process
        logging.info('Triggering synchronization...')
        dump_to_file(extract_json())
        logging.info('Synchronization completed.')
    finally:
        # Reset the flag when the synchronization process completes or encounters an error
        is_sync_running = False


def signal_handler(sig, frame):
    """
    Signal handler function to handle external signals.
    """
    if os.path.exists(FLAG_FILE):
        os.remove(FLAG_FILE)
        trigger_sync()

def check_for_flag_file():
    """
    Check if the flag file exists and trigger synchronization if it does.
    """
    if os.path.exists(FLAG_FILE):
        os.remove(FLAG_FILE)
        trigger_sync()


async def regular_sync():
    """
    Regular synchronization process.
    """
    while True:
        logging.info('No flag file found. Triggering regular synchronization...')
        trigger_sync()
        # Sleep for 30 minutes
        await asyncio.sleep(1800)


async def main():
    # Create tasks for coroutines
    flag_task = asyncio.create_task(check_for_flag_file_forever())
    sync_task = asyncio.create_task(regular_sync())

    # Await the tasks using asyncio.wait
    await asyncio.wait([flag_task, sync_task])


async def check_for_flag_file_forever():
    """
    Check for the flag file continuously.
    """
    while True:
        check_for_flag_file()
        await asyncio.sleep(1)

if __name__ == '__main__':
    TickTickClient._login = new_login
    auth_client = OAuth2(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        cache_path=cache_path
                        )
    client = TickTickClient(username, password, auth_client)

    asyncio.run(main())

