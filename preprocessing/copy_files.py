import os

SOURCE_PATH = './datasets/240514'
TARGET_PATH = '/Users/andongha1/dev/ImageNet-ES2/201-400'

PC_DIR = 'param_control'
AE_DIR = 'auto_exposure'
DIR = PC_DIR

def copy_files(dir_type):
    total = 0
    for environment in os.listdir(f'{SOURCE_PATH}/{dir_type}'):
        if environment.startswith('.'):
            continue
        for param in os.listdir(f'{SOURCE_PATH}/{dir_type}/{environment}'):
            if param.startswith('.'):
                continue
            for label in os.listdir(f'{SOURCE_PATH}/{dir_type}/{environment}/{param}'):
                if label.startswith('.'):
                    continue
                target_dir = f'{TARGET_PATH}/{dir_type}/{environment}/{param}/{label}'
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                for image in os.listdir(f'{SOURCE_PATH}/{dir_type}/{environment}/{param}/{label}'):
                    if image.startswith('.'):
                        continue
                    source = f'{SOURCE_PATH}/{dir_type}/{environment}/{param}/{label}/{image}'
                    target = f'{TARGET_PATH}/{dir_type}/{environment}/{param}/{label}/{image}'
                    os.system(f'cp -n {source} {target}')
                    print(f'Copied: {target}')
                    total += 1
    return total
       
total = 0 
total += copy_files(AE_DIR)
total += copy_files(PC_DIR)
print(f'Total: {total} files copied')