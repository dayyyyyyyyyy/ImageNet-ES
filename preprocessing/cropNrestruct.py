from PIL import Image
import pickle
import cv2
from glob import glob
import os
from pathlib import Path
# from tqdm import tqdm
from multiprocessing import Pool
import concurrent.futures
import time
import PIL

from PIL import ImageFile
# ImageFile.LOAD_TRUNCATED_IMAGES = True

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('config', help="config file")
args = parser.parse_args()


config = args.config.replace('/','.')
m = __import__(config[:-3], fromlist=['target_dir', 'OPTION', 'PARAM_TOTAL_NUM'])

def crop(original, target, ratio=(1,1), start=(185,255), padding = 2, size=None):

    crop_info = {
        'start': start,
        'ratio': ratio,
        'padding': padding
    }
    
    # print(crop_info)
    original_size = original.size
    modified_size = (original_size[0]*ratio[0], original_size[1]*ratio[1])

    # for size check
    try:
        croppedImage = target.crop((start[0]-padding, start[1]-padding, start[0] + modified_size[0] + padding, start[1]+ modified_size[1] + padding))
    except Exception as e:
        print(e)

        print(original.size)
        print(target.size)
        print(start[0]-padding, start[1]-padding, start[0] + modified_size[0] + padding, start[1]+ modified_size[1] + padding)
        croppedImage = None
    # print(croppedImage.size)
    return croppedImage, crop_info

def crop_items(items):
    remove_list = []
    cropped = None
    for dped_path, env_logs in items:
        r_dped_path = dped_path.replace('s4d','andongha1')
        print(f"display original image: {r_dped_path}")
        original = Image.open(r_dped_path)
        target_class_dir = r_dped_path.split('/')[-2]
        # print(dped_path)
        for env_num, option_logs in env_logs.items():
            for param_num, log in option_logs.items():
                taken_path = log['taken_path']
                # print('target path:', taken_path)
                file_name = r_dped_path.split('/')[-1]
                    
                dst_folder = f'{CROPPED_FOLDER}/{env_num}/param_{param_num}/{target_class_dir}'
                Path(dst_folder).mkdir(parents=True, exist_ok=True)
                dst = f'{dst_folder}/{file_name}'
                if os.path.exists(dst):
                    continue
                # auto 일때만...
                if m.OPTION == 'auto' and 'JPG' not in log['taken_path']:
                    for i in range(5):
                        taken_path = option_logs[i+1]['taken_path']
                        if 'JPG' in taken_path:
                            break
                
                try:
                    target = Image.open(taken_path)
                    # target.save("./test.jpg", "JPEG")
                    # target = Image.open("./test.jpg")
                    # print(target.size)
                    # try:
                    #     target.show() # 여기서 오류 나는거 같음
                    # except Exception as e:
                    #     print(e)
                    
                    # padding = adoption_info['padding']
                    # s_x, s_y = adoption_info['start']
                    # r_w, r_h = adoption_info['ratio']
                    cropped, _ = crop(original, target, **adoption_info)
                    # file_name = taken_path.split('/')[-1]
                except PIL.UnidentifiedImageError as e:
                    print(e)
                    remove_list.append(r_dped_path)

                # cropped.show()
                if cropped:
                    cropped.save(dst)
                else:
                    print("=======================")
                    print(taken_path)
                    # print(target.size)
                    print(adoption_info)
                    print("=======================")
                # print(f'saved in {dst}')
    return len(items), remove_list

# size adpotion
TAKEN_FOLDER = f'{m.target_dir}/taken{"_" if len(m.OPTION) > 0 else ""}{m.OPTION}'
LOG_FILE_NAME = glob(os.path.join(TAKEN_FOLDER, '*corrected.pickle'))[0].split('/')[-1]
CROPPED_FOLDER = f'{m.target_dir}/cropped{"_" if len(m.OPTION) > 0 else ""}{m.OPTION}'
Path(CROPPED_FOLDER).mkdir(parents=True, exist_ok=True)
ADOPTION_INFO_FILE_NAME = 'adoption.pickle'

adoption_info = None
with open(f'{CROPPED_FOLDER}/{ADOPTION_INFO_FILE_NAME}', 'rb') as f:
    adoption_info = pickle.load(f)

for key, value in adoption_info.items():
    print(value, type(value))
# for 1 image


if __name__ == '__main__':
    start = time.perf_counter()
    with open(f'{TAKEN_FOLDER}/{LOG_FILE_NAME}', 'rb') as f:
        data = pickle.load(f)

        p = Pool(processes=10) # multiprocessing 기반
        data_list = list(data.items())
        block_size = len(data)//10
        left = len(data) - block_size * 10
        items = list(map(lambda i: data_list[i*block_size:(i+1)*block_size], range(10)))
        items[-1] += data_list[-left:]

        print(len(data))

        result, removed_list = zip(*p.map(crop_items, items))
        print(sum(result))
        removed_list = list(set(sum(removed_list, [])))
        print('removed_list~~~~')
        print(removed_list) # 얘네 지워줘야함
        print(len(removed_list))

        for dped_path in removed_list:
            target = '/'.join(dped_path.split('/')[-2:])
            for i in range(m.PARAM_TOTAL_NUM):
                dst = f'{CROPPED_FOLDER}/param_{i}/{target}'
                print(dst, 'is removed')
                try:
                    os.remove(dst)
                except Exception as e:
                    print(f"Error while deleting file, {e} ", dst)

        # 그리고 c최종 log file 기록

    
        # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor: #multi threading 기반?
        #     futures = [executor.submit(crop_items, item) for item in items]
    
    finish = time.perf_counter()
    print(f'{round(finish-start,2)} seconds')

    
