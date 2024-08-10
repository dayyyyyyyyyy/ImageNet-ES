import pickle

LOG_FILE_PATH = './datasets/240512/taken_auto'
LOG_FILE_NAME = 'taken_log_env-control_auto-light_control-A4_600dpi_center_tine-no-resize2_session0_0512-144653_restored.pickle'

with open(f'{LOG_FILE_PATH}/{LOG_FILE_NAME}', 'rb') as f:
    data = pickle.load(f)

total = 0
for dped_path, dp_log in data.items():
    for env_name, env_log in dp_log.items():
        for param, param_log in env_log.items():
            total += 1
            try:
                if param_log['taken_path'] == LOG_FILE_PATH + '/101_IMG_0002.JPG':
                    print("\nFound:")
                    print(dped_path)
                    print(env_name)
                    print(param)
                    print(param_log)
            except KeyError:
                print("\nKeyError!!")
                print(dped_path)
                print(env_name)
                print(param)
                print(param_log)
                print()
                param_log['img_name'] = 'IMG_0001.JPG'
                param_log['camera_folder'] = '101CANON'
                param_log['taken_path'] = LOG_FILE_PATH + '/101_IMG_0001.JPG'
                print(data[dped_path][env_name][param])
                pickle.dump(data, open(f'{LOG_FILE_PATH}/{LOG_FILE_NAME}', 'wb'))
                break
        else:
            continue
        break
    else:
        continue
    break

print(f'Total: {total} files')