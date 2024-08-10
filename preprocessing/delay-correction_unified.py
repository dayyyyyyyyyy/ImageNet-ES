from PIL import Image
import pickle
import os
import shutil
from glob import glob
from functools import reduce
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('config', help="config file")
args = parser.parse_args()

config = args.config.replace('/','.')
m = __import__(config[:-3], fromlist=['target_dir', 'OPTION'])
TAKEN_FOLDER = f'{m.target_dir}/taken{"_" if len(m.OPTION) > 0 else ""}{m.OPTION}'
LOADED_FOLDER = f'{m.target_dir}/loaded'
LOG_FILE_NAME = glob(os.path.join(TAKEN_FOLDER, '*restored.pickle'))[0].split('/')[-1]

# def solve_delay_issue(discontinuous_info, options_log):
#     print("check start,last, prev, curr, after image of list are matched to original image")
#     print("if there is not matched image, we have to remove or do something for them")
                
#     for param_num, log in options_log.items():
#         print(param_num, log['taken_path'])
    
#     for key in discontinuous_info:
#         while True:
#             user_input = input(f'if backward correction (remove prev), please enter b. (if enter f -> forward correction (remove curr or do something)\n')
#             if user_input not in ['f','b']:
#                 print("please type b/f .")
#             elif user_input == 'b':
#                 print('do backward correction')
#                 # correct_backward(options_log, key)
#                 break
#             else:
#                 print('not implemented(forward correction)')
#                 break
#     print('after correction')
#     for param_num, log in options_log.items():
#         print(param_num, log['taken_path'])

def get_diff_log(prev, curr):
    try:
        
        dir1 = int(prev.split('_')[0])
        img1 = int(prev.split('_')[-1][:-4])
        dir2 = int(curr.split('_')[0])
        img2 = int(curr.split('_')[-1][:-4])
    except Exception as e:
        diff = 'undefined'
        print(e)
        return diff
    diff = None
    if dir1 == dir2:
        diff = img2 - img1
    elif dir2 - dir1 == 1:
        diff = 1 + img2 - 1 + 9999 - img1
    else:
        diff = 'undefined'
    return diff

def is_solvable(discontinuous_info, taken_list):
    # record solvable info
    solvable = None
    diff_sum = sum(map(lambda x: x["diff"], discontinuous_info.values()))
    normal_diff_sum = len(taken_list) - 1
    present_diff_sum = get_diff_log(taken_list[0], taken_list[-1])

    if len(discontinuous_info) ==0:
        # print("do nothing")
        solvable = True
    elif present_diff_sum - normal_diff_sum == diff_sum - len(discontinuous_info):
        print("shift 1 each")
        print("dis continuous info:", discontinuous_info)
        solvable = True
        # correct delay forward ( curr에 맞춤), correct delay backwrad (prev에 맞춤)
    else:
        print("do somethings more")
        print(discontinuous_info)
    return solvable

def is_continuous(prev, taken_list):
    '''
    [in]
    - prev
    - taken_list: taken img name list,
    '''
    discontinuous_info = {}
    solvable = False

    # record discontinuous info
    for idx, curr in enumerate(taken_list):
        if not prev:
             prev = curr # 첫번째 옵션이면 continuous check 안하나봐
             # prev 가 없어도 continuous 검사는 해야하는 거 아녀?
             # prev랑만 비교하나?
             # 로그 안에서 비교 안하는 이유라도...?
             # 밑에가 로그 안에서 비교함

             continue
        
        diff = get_diff_log(prev, curr)
        if diff != 1:
            print('not continuous info')
            print(f'prev:{prev}')
            print(f'curr:{curr}')

            # return discontinuous info
            discontinuous_info[f'pram_{idx+1}'] = {
                'prev': prev,
                'curr': curr,
                'diff': diff
            }

        prev = curr

    
    # record solvable info
    # solvable = is_solvable(discontinuous_info, taken_list)

    return discontinuous_info, solvable

def user_input_handler():
    pass

def decide_correction(key, delay_info, start_init):
    correction_info = None
    while True:
        if delay_info['prev'] == 'None' and delay_info['curr'] != 'None':
            user_input = 'prev'
        elif delay_info['prev'] != 'None' and delay_info['curr'] == 'None':
            user_input = 'next'
        elif delay_info['diff'] == 2 and start_init:
            user_input = 'prev'
        else:
            user_input = input(f'select the correction target prev/next.')

        print(user_input)
        print('#########')
        if user_input == 'prev':
            # get prev correction info
            print(delay_info)
            if delay_info["diff"] == 2:
                curr_num = delay_info['curr'].split('_')[-1].split('.')[0]
                if curr_num == '0001':
                    missed = delay_info['prev'][:-8] + '9999'+ '.JPG'
                else:
                    missed = delay_info['curr'][:-8] + f'{int(curr_num)-1:04}' + '.JPG'
                if start_init:
                    start = start_init
                    start_init = None
                else:
                    start = int(key.split('_')[-1]) - (delay_info["diff"] -1)
                estimated = {
                    'start': start,
                    'end': int(key.split('_')[-1])-1,
                    'missed': missed
                }
                print(f"estrimated correction info:{estimated}")
                # user_input = input('do you take this suggestion? y/n')
                user_input = 'y'
                if user_input == 'y':
                    return estimated, start_init
                # print('new case1! implement for this case!')
            elif delay_info["diff"] == 'undefined':
                ll =get_diff_log(delay_info['prev_delay_prev'],delay_info['curr'])
                print(ll)
                if ll != 'undefined' and int(ll)>0 and int(ll)<27:
                    start_init = int(key.split('_')[-1]) - ll
                    # print(key)
                    # print(ll)
                    # start = int(key.split('_')[-1]) - 1
                    # end = int(input('end index(from 1)?'))
                    # missed = input('missed?(if none, type none')
                    # estimated = {
                    #     'start': start,
                    #     'end': end,
                    #     'missed': missed
                    # }
                else:
                    user_input = input('is it delay? (y/n)')
                    if user_input == 'y':
                        start_init = int(input('start param num?'))
                # print(f"estrimated correction info:{estimated}")
                # user_input = input('do you take this suggestion? y/n')
                # if user_input == 'y':
                #     return estimated, start_init
                # start, end check
                return correction_info, start_init
            else:
                print('new case3!')
        elif user_input == 'next':
            # get next correction info
            if delay_info["diff"] == 'undefined': #curr not defined (next에서 고치게 두기)
                pass
            else:
                print('new case2! implement for this case!')
        else:
            print('Please enter character among (y/n).')
        print('return here')
        return correction_info, start_init

def get_delay_info(discontinuous_info):
    delay_info = []
    prev_delay_prev = None
    start_init = None
    for key, val in discontinuous_info.items():
        print('hui',key)
        print(val)
        while True:
            if val['diff'] == 'undefined' and val['prev'] == 'None' and val['curr'] == 'None':
                break
            elif val['diff'] in [2, 'undefined'] and (key != 'pram_1' or (key=='pram_1' and val['curr'] == 'None')):
                user_input = 'y'
            else:
                user_input = input(f'is it delay? y/n.')
            # 시작 이미지 , 마지막 이미지, dp 이미지가 같은지 체크 
            # 시작 이미지 -1, 마지막 이미지 +1이 다른 이미진지 체크
            # 리스트에 blank 없는지 체크 
            # 위 세가지 조건 모두 만족하면 n
            if user_input == 'y':
                # start, end, missed를 찾아줘야함.
                # estimated = missed 로
                val['prev_delay_prev'] = prev_delay_prev
                X = decide_correction(key,val,start_init)
                print(X)
                correction_info, start_init = X
                prev_delay_prev = val['prev']
                if correction_info:
                    delay_info.append(correction_info)
                
                break
            elif user_input == 'n':
                break
            else:
                print('Please enter character among (y/n).')
    return delay_info

def detect_delay(data):
    '''
    for taken data, detect delayed images
    if solvable => correct, else record solvable

    [in]
    - data: {'dp path':taken_logs}

    [out]
    - not_solved
    '''
    prev = None
    delays = {}
    # print(data)
    for dped_path, envs_log in data.items():
        # check continuous
        print(envs_log)
        env_delays = {}
        for env_num, options_log in envs_log.items():
            # print(options_log)
            try:
                taken_list = list(map(lambda x: x['taken_path'].split('/')[-1] if x['taken_path'] else 'None', options_log.values()))
            except Exception as e:
                options_log = list(options_log.values())
                print(options_log)
                taken_list = []
                for x in options_log:
                    try:
                        taken_list.append(x['taken_path'].split('/')[-1])
                    except Exception as e :
                        print(e)
                        taken_list.append('None')
                
            discontinuous_info, solvable = is_continuous(prev, taken_list)
            if discontinuous_info:
                print(taken_list)
                print(dped_path)
                delay_info = get_delay_info(discontinuous_info)
                if delay_info:
                    env_delays[env_num] = delay_info
            prev = taken_list[-1] # solve 하면 고쳐야 하지 않오? 요건 이따 보자요
        if env_delays:
            delays[dped_path] = env_delays
    return delays

def correct_delay(data, delay_info):
    # delay = start, end, missed
    # start <- start+1
    # ...
    # end-1 <- end
    # end <- missed

    # x = list(delay_info.items())[0]
    # env_del_info = list(x[1].values())[0][0]['missed']
    # print(env_del_info)
    # param_del_info = env_del_info[0]['missed']
    # print(param_del_info['missed'])
    # print(list((list(x[1].values())[0].values()))[0]['missed'])
    sorted_delay_info = dict(sorted(delay_info.items(), key=lambda x: list(x[1].values())[0][0]['missed']))
    update_targets = ['camera_folder', 'img_name', 'taken_path']

    for dped_path, delay_info in sorted_delay_info.items():
        for env, env_delay_info in delay_info.items():
            for delay in env_delay_info: # delay_info 내 delay끼리 구간 안겹친다 가정
                for i in range(delay['start'], delay['end']):
                    next_log = data[dped_path][env][i+1]
                    # print(next_log)
                    if 'taken_path' not in next_log:
                        next_log['taken_path'] = 'None'
                    
                    update_info = list(map(lambda update_target: next_log[update_target], update_targets))
                    updates = dict(zip(update_targets, update_info))
                    print(updates)
                    print(data[dped_path][env][i])
                    data[dped_path][env][i].update(updates)
                
                if delay['missed'] !='none':
                    folder, _, img = delay['missed'].split('_')
                    img = 'IMG_' + img

                    #copy src to dst
                    src = f'{LOADED_FOLDER}/{folder}CANON/{img}'
                    taken_path = f'{TAKEN_FOLDER}/{delay["missed"]}'
                    shutil.copyfile(src, taken_path)

                    update_info = {
                        'camera_folder': folder,
                        'img_name': img,
                        'taken_path': taken_path
                    }
                    
                    # 여기서 부터 정신 차려야 함.
                    data[dped_path][env][delay['end']].update(update_info)
                    print(delay_info)
                    print(data[dped_path][env])
                    # print(list(map(lambda x: x['taken_path'], data[dped_path][env].values())))

def fill_blanks(taken_paths, blanks):
    for idx in blanks:
        targets = taken_paths[5*idx:5*(idx+1)]
        corrected = []
        multiple_append = 0
        for idx, i in enumerate(targets):
            if 'IMG' in i:
                corrected += [i] * (multiple_append+1)
                multiple_append = 0
            elif idx==0 or len(corrected)<1:
                multiple_append +=1
            else:
                corrected += [corrected[-1]] * (multiple_append+1)
                multiple_append = 0
            print(corrected)

        taken_paths[5*idx:5*(idx+1)] = corrected

    return taken_paths
        
with open(f'{TAKEN_FOLDER}/{LOG_FILE_NAME}', 'rb') as f:
    data = pickle.load(f)
    # step1
    delays = detect_delay(data)

    # keys = list(data.keys())
    # taken_paths1 = []

    
    # step2 
    correct_delay(data, delays)
    # print(taken_paths1)
    # print(len(taken_paths1))

    # step3 
    # blanks_indice = map(lambda x: keys.index(x), blanks)
    # taken_paths1 = fill_blanks(taken_paths1, blanks_indice)
    # print(len(taken_paths1))
    
    # taken_paths1 => list of dict of len 5
    # step4
    # for idx, (dped_path, options_log) in enumerate(data.items()):
    #     targets = taken_paths1[5*idx:5*(idx+1)]
    #     for key, param_log in options_log.items():
    #         # print(key-1)
    #         # print(targets)
    #         param_log['taken_path'] = targets[key-1]

    # step5
    # print(data)
    
    # taken fail => remove? and cnt and print
    will_be_removed = []
    for dped_path, dp_log in data.items():
        for env_name, env_log in dp_log.items():
            for param, param_log in env_log.items():
                print(param_log.keys())
                if not param_log['taken_path'] or 'taken_path' not in param_log or 'fail' in param_log['taken_path']:
                    will_be_removed.append(dped_path)
                    print(dped_path)
                    print(env_name)
                    print(param,env_log)
                    # print('prev env log:', prev)
    
    for dped_path in set(will_be_removed):
        del data[dped_path]
                    
    with open(f'{TAKEN_FOLDER}/taken_log_corrected.pickle', 'wb') as f:
        pickle.dump(data, f)
        print(data)
        print(f'{len(data)} correction logs are saved')

    

