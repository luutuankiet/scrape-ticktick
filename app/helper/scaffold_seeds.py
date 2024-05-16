#%%
import os,sys

# to use packages in current dir
sys.path.append(os.path.dirname((__file__))) 

# to use packages in other relative dir
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))

from ETL.lvl3_helper import mapping_sheet,seed_path

import csv

#%%

def init_mapping_seed(results=None):
    with open(seed_path,'w') as f:
        writer = csv.writer(f)
        writer.writerows(mapping_sheet.get_values())


if __name__ == '__main__':
    init_mapping_seed()