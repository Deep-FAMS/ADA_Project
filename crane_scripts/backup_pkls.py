import os
WORK = os.environ["WORK"]
PROJ_DIR = f'{WORK}/ADA_Project'
os.chdir(PROJ_DIR)
print(os.getcwd())


import sys
sys.path.insert(0, f'{WORK}/ADA_Project')
sys.path.insert(0, f'{WORK}/ADA_Project/DeepFAMS')


from glob import glob
from tqdm import tqdm
from pathlib import Path
import shutil
from pprint import pprint
from datetime import datetime

import DeepFAMS


def backup_pickles(PROJ_DIR):
    
    Tstamp = datetime.now().strftime("%m%d%Y_%H%M")
    
    WORK = Path(PROJ_DIR).parent
    backups_folder = f'{WORK}/ADA_Project_pkl_backups/{Tstamp}'
    Path(backups_folder).mkdir(parents=True, exist_ok=True)
    
    TRfolders = glob(f'{PROJ_DIR}/training_runs/*')
    
    latest_snaps = []
    
    for folder in TRfolders:
        for num in range(-1, -10, -1):
            files = sorted(glob(folder + "/**/*"))
            files = [x for x in files if 'network-snapshot' in x]
            if files == []:
                continue
            else:
                latest_snap = sorted(files)[-1]
                latest_snaps.append(latest_snap)
                break


    print('=' * 100,
         '\nLatest snaps:\n')
    pprint(latest_snaps)
    print('=' * 100, '\n')

    for pkl in latest_snaps:
        pkl_dst_name = f'{backups_folder}/{Path(pkl).parent.name}__{Path(pkl).name}'
        shutil.copyfile(pkl, pkl_dst_name)
        print(f'Copied: {Path(pkl).parent.parent.name.replace("_training-runs", "")}\'s latest pickle '
             f'to ==> {pkl_dst_name}')

    print('\nUploading to Google Drive...')
    
    DeepFAMS.utils.executePopen(f'''#!/bin/bash
    module load rclone
    rclone copy {backups_folder} GoogleDrive:/ADA_Project_pkl_backups/{Path(backups_folder).name} -P''',
    PROJ_DIR)

    print('\nDone!')
