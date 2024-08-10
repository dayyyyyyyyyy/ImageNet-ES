time = 'day'
date = '230817'
target_dir = f'./2023_08_17_{time}'
saved_dir = f'./08_17_{time}'
dataset = "Restricted_ImageNet"
taken_log = f'taken_log_{time}.pickle'


missed_info = {
    'night': ['/Users/edw2n/Downloads/custom_dataset/n02480495/ILSVRC2012_val_00015876.JPEG',
    '/Users/edw2n/Downloads/custom_dataset/n02483708/ILSVRC2012_val_00026496.JPEG',
    ],
    'day': [],
}

delay_info = {
    # values : list of delay data
    'night': [
    # (delay_start, delay_end, missed_image) 
    ('/Users/edw2n/Downloads/custom_dataset/n02113186/ILSVRC2012_val_00019678.JPEG', '/Users/edw2n/Downloads/custom_dataset/n02655020/ILSVRC2012_val_00011321.JPEG', 'IMG_7848.JPG'),
    ('/Users/edw2n/Downloads/custom_dataset/n02099712/ILSVRC2012_val_00040210.JPEG', '/Users/edw2n/Downloads/custom_dataset/n02490219/ILSVRC2012_val_00008550.JPEG', 'IMG_8054.JPG'),
    ],

    'day': [
        ('/Users/edw2n/Downloads/custom_dataset/n02108089/ILSVRC2012_val_00016299.JPEG', '/Users/edw2n/Downloads/custom_dataset/n02108089/ILSVRC2012_val_00016299.JPEG', 'IMG_7481.JPG'),
        ]
}