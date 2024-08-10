import argparse
from pathlib import Path
import os
import shutil
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('date', help="date folder")
args = parser.parse_args()

AGGREGATED_FOLDER = f'./{args.date}'
CROPPED_FOLDER = f'{AGGREGATED_FOLDER}/cropped'
AUTO_CROPPED_FOLDER = f'{AGGREGATED_FOLDER}/cropped_auto'
Path(AGGREGATED_FOLDER).mkdir(parents=True, exist_ok=True)
Path(CROPPED_FOLDER).mkdir(parents=True, exist_ok=True)
Path(AUTO_CROPPED_FOLDER).mkdir(parents=True, exist_ok=True)

data = {}
LOG_FILE_NAME = f'{AGGREGATED_FOLDER}/log.pickle'
with open(LOG_FILE_NAME, 'wb') as f:
    for dir_name in os.listdir('./'):
        # aggregate sessions
        signature = f'{args.date}_ss'
        if os.path.isdir(dir_name) and signature in dir_name:
            cropped_folder =  f'{dir_name}/cropped'
            shutil.copytree(cropped_folder, CROPPED_FOLDER, dirs_exist_ok = True)
            os.rename(f'{CROPPED_FOLDER}/adoption.pickle', f'{CROPPED_FOLDER}/adoption_{dir_name}.pickle')
            try:
                ss_log_file = f'{dir_name}/taken/taken_log_corrected.pickle'
                shutil.copyfile(f'{dir_name}/taken/taken_log_corrected.pickle',f'{AGGREGATED_FOLDER}/log_{dir_name}.pickle')
                with open(ss_log_file, 'rb') as ss_f:
                    ss_log_data= pickle.load(ss_f)
                    data.update(ss_log_data)
                    print(f'logs of {len(ss_log_data)} are updated.')
            except Exception as e:
                print(e)

        # aggregate auto
        auto_signature = f'{args.date}_auto'
        if os.path.isdir(dir_name) and auto_signature in dir_name:
            cropped_folder =  f'{dir_name}/cropped_auto'
            shutil.copytree(cropped_folder, AUTO_CROPPED_FOLDER, dirs_exist_ok = True)
            os.rename(f'{AUTO_CROPPED_FOLDER}/adoption.pickle', f'{AUTO_CROPPED_FOLDER}/adoption_{dir_name}.pickle')
            try:
                ss_log_file = f'{dir_name}/taken_auto/taken_log_corrected.pickle'
                shutil.copyfile(f'{dir_name}/taken_auto/taken_log_corrected.pickle',f'{AGGREGATED_FOLDER}/log_auto.pickle')
            except Exception as e:
                print(e)

    pickle.dump(data, f)
    print(f'logs of {len(data)} are saved in {LOG_FILE_NAME}')
            

# auto 는 따로 옮겨 주기