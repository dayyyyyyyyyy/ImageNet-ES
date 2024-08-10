# Check files

import os

TARGET_PATH = '/Users/andongha1/dev/ImageNet-ES2/001-200'
PC_DIR = 'param_control'
AE_DIR = 'auto_exposure'

ENV = ['l1', 'l2', 'l3', 'l4', 'l6', 'l7', 'l8', 'l9', 'l10']
PC_PARAM = 27
AE_PARAM = 5

total = 0

for env in ENV:
    for i in range(1, PC_PARAM+1):
        path = f'{TARGET_PATH}/{PC_DIR}/{env}/param_{i}'
        if not os.path.exists(path):
            print(f'Not found: {path}')
        elif len(os.listdir(path)) == 0:
            print(f'Empty: {path}')
        else:
            for file in os.listdir(path):
                if file.startswith('.'):
                    print(f'Hidden file: {path}/{file}')
                    # delete
                    os.remove(f'{path}/{file}')
            total += len(os.listdir(path))

for env in ENV:
    for i in range(1, AE_PARAM+1):
        path = f'{TARGET_PATH}/{AE_DIR}/{env}/param_{i}'
        if not os.path.exists(path):
            print(f'Not found: {path}')
        elif len(os.listdir(path)) == 0:
            print(f'Empty: {path}')
        else:
            for file in os.listdir(path):
                if file.startswith('.'):
                    print(f'Hidden file: {path}/{file}')
                    # delete
                    os.remove(f'{path}/{file}')
            total += len(os.listdir(path))
            
print(f'Total: {total} files')