#%%
import os,sys


# from ETL.lvl3_helper import mapping_sheet
from helper.source_env import dbt_project_dir,service_account_path
import gspread


import csv

#%%


client = gspread.service_account(service_account_path)
workbook = client.open_by_url("https://docs.google.com/spreadsheets/d/1My7VU0GrAlYTa46Hj1ciOBXivcF7QKSYeRVXXbyV74o/edit#gid=0")
helper_sheet = workbook.get_worksheet(1)
mapping_sheet = workbook.get_worksheet(0)

seed_path = os.path.join(dbt_project_dir,'seeds/list_goal_mapping.csv')


def init_mapping_seed(results=None):
    with open(seed_path,'w') as f:
        writer = csv.writer(f)
        writer.writerows(mapping_sheet.get_values())
    print(f'seeds mapping done. checkout the file at {seed_path}')


if __name__ == '__main__':
    init_mapping_seed()