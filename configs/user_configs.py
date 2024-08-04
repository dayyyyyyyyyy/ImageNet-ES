# Need to update

# Dataset directory should look like:
# - datasets
#   - ImageNet-ES
#     - es-test
#       - param-control
#       - auto-exposure
#   - ImageNet-ES-Natural
#     - es-natural-test
#       - param-control
#       - auto-exposure

DATASET_ROOT_DIR = "path/to/datasets"

SWIN_PT = "/path/to/Swin-weight-file"
RESNET18_PT = "/path/to/Resnet18-weight-file"
EN_PT = "/path/to/EfficientNet-weight-file"
VIT_PT = "/path/to/vit-weight-file"

TARGET_OOD_POSTPROCESSORS = ['msp', 'odin', 'react', 'vim', 'ash']