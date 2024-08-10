import sys
import os
import cv2
import pickle
import argparse

# Constants for initial crop
# Crop based on the A4 banner
IMAGE_SIZE = cv2.imread('100_IMG_3486.JPG').shape[:2]
CH, CW = 4000, 4000
CX, CY = (IMAGE_SIZE[1] - CW) // 2, (IMAGE_SIZE[0] - CH) // 2
ZOOM_UNIT = 200

# Change these before running the script
LOG_FILE_NAME = "taken_log_corrected.pickle"
USERNAME = 'andongha1'


parser = argparse.ArgumentParser()
parser.add_argument('config', help="config file")
args = parser.parse_args()
config = args.config.replace('/','.')
m = __import__(config[:-3], fromlist=['target_dir', 'OPTION'])
save_path = f"{m.target_dir}/cropped_{m.OPTION}".rstrip('_')

def show_image(taken_path, zoom):
    cv2.destroyAllWindows()
    img = cv2.imread(taken_path)
    h, w = CH - zoom * 2 * ZOOM_UNIT, CW - zoom * 2 * ZOOM_UNIT
    x, y = CX + zoom * ZOOM_UNIT, CY + zoom * ZOOM_UNIT
    img = img[y:y+h, x:x+w]
    cv2.imshow('img', img)
    
    
def save_image(image_name, image_log, x, y, w, h):
    class_dir_name = image_name.split('/')[-2]
    image_file_name = image_name.split('/')[-1]
    i = 0
    for env, env_data in image_log.items():
        for param, param_data in env_data.items():
            taken_path = param_data['taken_path']
            img = cv2.imread(taken_path)
            img = img[y:y+h, x:x+w]
            save_dir_path = os.path.join(save_path, env, f'param_{param}', class_dir_name)
            os.makedirs(save_dir_path, exist_ok=True)
            final_path = os.path.join(save_dir_path, image_file_name)
            if cv2.imwrite(final_path, img):
                print("Saved:", final_path)
            else:
                print("Failed to save:", final_path)
            i += 1
    print(f"Saved {i} images")


def crop():
    log_file_path = m.target_dir + "/" + f"taken_{m.OPTION}".rstrip('_') + "/" + LOG_FILE_NAME
    coordinates_log = {}
    
    with open(log_file_path, 'rb') as f:
        data = pickle.load(f)
    
    for image_name, image_data in data.items():
        print("Current image:", image_name)
        for env, env_data in image_data.items():
            for param, param_data in env_data.items():
                taken_path = param_data['taken_path']
                zoom = 0
                show_image(taken_path, zoom)
                
                skip_image = False
                while True:
                    k = cv2.waitKey(0)
                    if k == ord('n'):
                        skip_image = True
                        break
                    elif k == ord('y'):
                        cv2.destroyAllWindows()
                        break
                    elif k == ord('z'):
                        # zoom in towards center
                        zoom = min(9, zoom + 1)
                        show_image(taken_path, zoom)
                    elif k == ord('x'):
                        # zoom out from center
                        zoom = max(0, zoom - 1)
                        show_image(taken_path, zoom)
                    elif k == ord('q'):
                        cv2.destroyAllWindows()
                        sys.exit()
                if skip_image:
                    continue
                
                # Crop
                img = cv2.imread(taken_path)
                ih, iw = CH - zoom * 2 * ZOOM_UNIT, CW - zoom * 2 * ZOOM_UNIT
                ix, iy = CX + zoom * ZOOM_UNIT, CY + zoom * ZOOM_UNIT
                img = img[iy:iy+ih, ix:ix+iw]
                x, y, w, h = cv2.selectROI('ROI selection', img, False)
                x += ix
                y += iy
                print("Cropped:", x, y, w, h)
                
                # Find original image to get the aspect ratio
                original_path = os.path.join(image_name.replace('s4d', USERNAME))
                oh, ow = cv2.imread(original_path).shape[:2]
                print("Original image size:", ow, oh)
                h = int(oh * w / ow)
                
                # Crop and save all images in the directory with the same ROI
                save_image(image_name, image_data, x, y, w, h)
                coordinates_log[image_name] = [x, y, w, h]
                break
                
            else:
                continue
            break
                
    pickle.dump(coordinates_log, open(f"{m.target_dir}/crop_coordinates_log.pickle", 'wb'))
    
    
def load_and_crop():
    log_file_path = m.target_dir + "/" + f"taken_{m.OPTION}".rstrip('_') + "/" + LOG_FILE_NAME
    coordinates_log = pickle.load(open(f"{m.target_dir}/crop_coordinates_log.pickle", 'rb'))
    
    with open(log_file_path, 'rb') as f:
        data = pickle.load(f)
    
    for image_name, image_data in data.items():
        print("Current image:", image_name)
        x, y, w, h = coordinates_log[image_name]
        save_image(image_name, image_data, x, y, w, h)

## Run the script
if __name__ == "__main__":
    if args.config.endswith('auto.py'):
        crop()
    else:
        load_and_crop()
    print("Done")