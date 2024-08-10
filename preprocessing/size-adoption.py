from PIL import Image
import pickle
import cv2
from glob import glob
import os
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('config', help="config file")
args = parser.parse_args()

config = args.config.replace('/','.')
m = __import__(config[:-3], fromlist=['target_dir', 'OPTION'])

def crop(original, target, ratio=(2.74,2.74), start=(625,635), padding = 4, size=None):
    

    crop_info = {
        'start': start,
        'ratio': ratio,
        'padding': padding
    }
    
    original_size = original.size
    modified_size = (original_size[0]*ratio[0], original_size[1]*ratio[1])
    crop_info['size'] = modified_size
    # for size check
    croppedImage = target.crop((start[0]-padding, start[1]-padding, start[0] + modified_size[0] + padding, start[1]+ modified_size[1] + padding))
    # print(original.size)
    # print(target.size)
    # print(croppedImage.size)
    return croppedImage, crop_info

# size adpotion
TAKEN_FOLDER = f'{m.target_dir}/taken{"_" if len(m.OPTION) > 0 else ""}{m.OPTION}'
LOG_FILE_NAME = glob(os.path.join(TAKEN_FOLDER, '*corrected.pickle'))[0].split('/')[-1]
CROPPED_FOLDER = f'{m.target_dir}/cropped{"_" if len(m.OPTION) > 0 else ""}{m.OPTION}'
Path(CROPPED_FOLDER).mkdir(parents=True, exist_ok=True)
ADOPTION_INFO_FILE_NAME = 'adoption.pickle'

def target_selection(data):
    selected_targets = {}
    for dped_path, envs_log in data.items():
        r_dped_path = dped_path.replace('s4d','andongha1')
        print(f"display original image: {r_dped_path}")
        
        dped = cv2.imread(r_dped_path, cv2.IMREAD_COLOR)
        cv2.imshow('displayed', dped)
        
        k = cv2.waitKey(1000)
        user_input = input(f'##### select? (if yes, enter s).\n')
        if user_input == 's':
            # for env_num, options_log in envs_log.items():
            options_log = envs_log['l1']
            for param_num,  taken_log in options_log.items():
                print(f'param num: {param_num},', taken_log['taken_path'])
                taken = cv2.imread(taken_log['taken_path'], cv2.IMREAD_COLOR)
                cv2.imshow('taken', taken)
                k = cv2.waitKey(1000)
                if k==27:    # Esc key to stop
                    break
                elif k==-1:  # normally -1 returned,so don't print it
                    user_input = input(f'##### select this params??(enter s).\n')
                    if user_input == 's':
                        selected_targets[r_dped_path] = taken_log['taken_path']
                        break
                    else:
                        continue
                else:
                    print('exception is occured') # else print its value                
        print('all params are displayed')
        user_input = input(f'##### show next displayed image?(please take one of n(no) or enter).\n')
        if user_input == 'n':
            break
        else:
            continue
    return selected_targets

def starting_point_selection(cropped, crop_info, original, target):
    while True:
        print(f'crop_info: {crop_info}')
        cropped.show()
        do_continue = input(f'##### start point selection continue? (enter y/n).\n')
        if do_continue == 'n':
            break
        else:
            while True:
                try:
                    s_x, s_y = input(f'##### start point? ex) 185 255 \n').split()
                    crop_info['start'] = (int(s_x), int(s_y))
                    cropped, crop_info = crop(original,  target, **crop_info)
                    break
                except Exception as e:
                    print(e)
    return crop_info
    
def ratio_selection(crop_info, original, target):
    # for size check
    original_size = original.size
    print('original size:', original_size)
    while True:
        do_continue = input(f'##### w, h selection ? (enter y/n).\n')
        if do_continue =='n':
            break
        else:
            width, height = input(f'##### width and height? ex) 185 255 \n').split()
            r_w = float(width) / original_size[0]
            r_h = float(height) / original_size[1]
            crop_info['ratio'] = (r_w, r_h)
            cropped, crop_info = crop(original,  target, **crop_info)
            print(f'crop_info: {crop_info}')
            cropped.show()
    return crop_info

def padding_selection(crop_info, original, target):
    while True:
        do_continue = input(f'##### padding selection ? (enter y/n).\n')
        if do_continue =='n':
            break
        else:
            padding = int(input(f'##### padding? ex) 3 \n'))
            crop_info['padding'] = padding
            cropped, crop_info = crop(original,  target, **crop_info)
            print(f'crop_info: {crop_info}')
            cropped.show()
    return crop_info

# for 1 image
with open(f'{TAKEN_FOLDER}/{LOG_FILE_NAME}', 'rb') as f:
    data = pickle.load(f)
    
    # will_be_removed = []
    # for dped_path, dp_log in data.items():
    #     for env_name, env_log in dp_log.items():
    #         for param, param_log in env_log.items():
    #             if 'taken_path' not in param_log or 'fail' in param_log['taken_path']:
    #                 will_be_removed.append(dped_path)
    #                 print(dped_path)
    #                 print(env_name)
    #                 print(param,env_log)
    #                 # print('prev env log:', prev)
    
    # for dped_path in set(will_be_removed):
    #     del data[dped_path]
            
    selected_targets = target_selection(data)
    
    print('selected:', selected_targets)

    crop_info = {}
    for original_path, taken_path in selected_targets.items():

        print('target path:', taken_path)
        original = Image.open(original_path)
        target = Image.open(taken_path)
        print(target.size)

        # find 는 일단 1번 타겟으로 셋팅
        # try:
        #     target.show() # 여기서 오류 나는거 같음
        # except Exception as e:
        #     print(e)

        cropped, crop_info = crop(original,  target, **crop_info)

        # start point selection
        crop_info = starting_point_selection(cropped, crop_info, original, target)

        # w,h point selection
        crop_info = ratio_selection(crop_info, original, target)
        
        # padding selection
        crop_info = padding_selection(crop_info, original, target)
        
    print('final crop info:', crop_info)
    with open(f'{CROPPED_FOLDER}/{ADOPTION_INFO_FILE_NAME}', 'wb') as f_ad:
        pickle.dump(crop_info, f_ad)
        print('adoption info is saved')

