import pickle
import cv2
import os

target_path = './datasets/240216/cropped'
taken_path = './datasets/240216/taken'
pickle_path = f'{taken_path}/taken_log_corrected.pickle'

ix, iy, iw, ih = 1000, 500, 4000, 4000

with open(pickle_path, 'rb') as f:
    data = pickle.load(f)
    
for k, v in data.items():
    original_path = k.replace('s4d', 'andongha1')
    class_name = original_path.split('/')[-2]
    img_name = original_path.split('/')[-1]
    
    for env_num, env_logs in v.items():
        for param_num, log in env_logs.items():
            taken_path = log['taken_path']
            print(taken_path)
            if 'fail' in taken_path:
                continue
            img = cv2.imread(taken_path)
            cv2.imshow('img', img)
            
            # Check if image is visible
            print("Press 'n' to skip this image")
            print("Press 'y' to crop this image")
            k = cv2.waitKey(0)
            if k == ord('n'):
                continue
            elif k == ord('y'):
                cv2.destroyAllWindows()
                
            # Crop
            img = img[iy:iy+ih, ix:ix+iw]  # initial crop
            x, y, w, h = cv2.selectROI('ROI selection', img, False)
            x += ix
            y += iy
            print("Cropped:", x, y, w, h)
            
            # Find original image to get the aspect ratio
            original = cv2.imread(original_path)
            oh, ow = original.shape[:2]
            print("Original image size:", ow, oh)
            h = int(oh * w / ow)
            
            # Step 2: Crop all images of same class with the same ROI
            # And save it in proper directory
            for env_num, env_logs in v.items():
                for param_num, log in env_logs.items():
                    image = cv2.imread(taken_path)
                    image = image[y:y+h, x:x+w]
                    save_dir = f'{target_path}/{env_num}/param_{param_num}/{class_name}'
                    os.makedirs(save_dir, exist_ok=True)
                    final_path = f'{target_path}/{env_num}/param_{param_num}/{class_name}/{img_name}'
                    cv2.imwrite(final_path, image)
                    print("Saved:", final_path)
            break
        break            
            
    print("Ready for the next image. Press ESC")