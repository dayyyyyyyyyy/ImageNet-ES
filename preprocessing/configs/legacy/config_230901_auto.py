time = 'night'
date = '230901'
target_dir = f'./230901'
saved_dir = f'./09_01_{time}'
dataset = "Restricted_ImageNet"
LOG_FILE_NAME = "taken_log_night_auto_RI_403.pickle"
PARAM_TOTAL_NUM = 5
OPTION = '_auto'
missed_info = {
    'night': [],
    'day': [],
}

delay_info = {
    # values : list of delay data
    'night': [
    # (delay_start, delay_end, missed_image) 
    ],

    'day': [
        ]
}

delayed = [
    # start end missed (end 포함) (shift)
        # start -1 <- start
        # end-1 <- end
        # end <- missed
    ('101CANON/IMG_8456.JPG','101CANON/IMG_8460.JPG', '101CANON/IMG_8460.JPG'),
    ('101CANON/IMG_7778.JPG','101CANON/IMG_7805.JPG', '101CANON/IMG_7806.JPG'),
    ('101CANON/IMG_7957.JPG','101CANON/IMG_7962.JPG', '101CANON/IMG_7963.JPG'),
    ('101CANON/IMG_8288.JPG','101CANON/IMG_8310.JPG', '101CANON/IMG_8311.JPG'),
    ('101CANON/IMG_9075.JPG','101CANON/IMG_9085.JPG', '101CANON/IMG_9086.JPG'),
    ('101CANON/IMG_7545.JPG','101CANON/IMG_7547.JPG', '101CANON/IMG_7548.JPG')
]

blanks = [
    './custom_dataset/n02480495/ILSVRC2012_val_00015876.JPEG', # 나머지로 복사
    './custom_dataset/n02483708/ILSVRC2012_val_00026496.JPEG', # 나머지로 복사
    './custom_dataset/n02099712/ILSVRC2012_val_00040210.JPEG', # 나머지로 복사
    './custom_dataset/n02488291/ILSVRC2012_val_00031294.JPEG', # 나머지로 복사
    './custom_dataset/n02488291/ILSVRC2012_val_00041180.JPEG', # 나머지로 복사
    './custom_dataset/n02493793/ILSVRC2012_val_00026603.JPEG', # 나머지로 복사
    './custom_dataset/n02123045/ILSVRC2012_val_00005358.JPEG', # 나머지 복사
    './custom_dataset/n02093859/ILSVRC2012_val_00015358.JPEG', # 나머지 복사
    './custom_dataset/n02087046/ILSVRC2012_val_00014912.JPEG', # 나머지 복사
    './custom_dataset/n02108000/ILSVRC2012_val_00048636.JPEG',# 나머지 복사,
    './custom_dataset/n02480855/ILSVRC2012_val_00020000.JPEG'
]