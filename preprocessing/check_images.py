# Check if images match the log

import pickle
import os

LOG_FILE = 'logs/taken_log_env-control_3x3x3_grid_light_control10-A4_600dpi_center_tine-no-resize2_session0_0429-200808.pickle'
IMAGE_DIR = 'datasets/240429/DCIM/100CANON'

print("Loading log file...")
with open(LOG_FILE, 'rb') as f:
    log = pickle.load(f)
    
image_list = os.listdir(IMAGE_DIR)
image_list.sort()
print("Found images:", len(image_list))
image_index = 0

for i, (image_name, image_info) in enumerate(log.items()):
    print(f"{[i+1]}\tChecking image: {image_name.split('/')[-1]}", end=' --> ')
    for env, env_info in image_info.items():
        for param, param_info in env_info.items():
            if param_info['img_name'] in image_list:
                print("First image name:", param_info['img_name'], end=' --> ')
                print("Images:", int(param_info['img_name'].split('.')[0].split('_')[-1]) - image_index)
                image_index = int(param_info['img_name'].split('.')[0].split('_')[-1])
                break
            else:
                print("Missing image:", param_info['img_name'])
        else:
            continue
        break
    


print("Done")
print("Total logs:", len(log) * 9 * 32)
print("Total images without log:", len(image_list))