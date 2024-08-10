# Preprocessing code for S4D dataset collection

## 1. Preparation

1. Run the following command in local environment.

```bash
cd path/to/ImageNet-ES-Natural/preprocessing
ln -s /Volumes/<SD_CARD_NAME>  ./datasets/<SD_CARD_NAME>  # Symbolic link to the SD card
```

2. Copy the log file from collection environment to your machine and save it in `logs` directory.

3. Create a config file in `configs` directory. See `configs/config_template.py` for the template.

## 2. Preprocessing

