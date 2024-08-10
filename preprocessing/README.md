# Preprocessing code for S4D dataset collection

## 1. Preparation

1. Run the following command in local environment.

```bash
cd path/to/ImageNet-ES-Natural/preprocessing
ln -s /Volumes/<SD_CARD_NAME>  ./datasets/<YYMMDD>  # Symbolic link to the SD card
```

2. Copy the log file from collection environment to your machine and save it in `logs` directory.

3. Create a config file in `configs` directory. See `configs/config_template.py` for the template. 
    - Name the config file as `config_YYMMDD.py` and `config_YYMMDD_auto.py`.
    - `date` field should match with dataset directory name and config file name. (YYMMDD)

## 2. Preprocessing

1. Run the restoration script.
```bash
python3 restore_unified.py configs/config_YYMMDD.py
python3 restore_unified.py configs/config_YYMMDD_auto.py
```

2. Run the delay correction script.
```bash
python3 delay_correction.py configs/config_YYMMDD.py
python3 delay_correction.py configs/config_YYMMDD_auto.py
```

3. Run the crop script.

```bash
python3 crop-save.py configs/config_YYMMDD_auto.py
python3 crop-save.py configs/config_YYMMDD.py
```

- Run the auto exposure first. AE images are more feasible for cropping.
- Manual exposure images will be cropped automatically according to the crop coordinates of AE images.
- How to crop images:
    - Press 'z' to zoom in and 'x' to zoom out.
    - Use your mouse to draw a rectangle on the image.
    - Press 'Enter' to crop and proceed to the next image.