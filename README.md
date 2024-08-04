# Lens: Adaptive Camera Sensor for Vision Models

### 1. Environment Setup

Expected Dataset Structure

Type in the dataset path in `lens_eval.py` and `configs/user_configs.py`

```
- path/to/datasets
  - ImageNet-ES
    - sampled_tin_no_resize2
    - es-test
      - param-control
      - auto-exposure
  - ImageNet-ES-Natural
    - es-natural-test
      - param-control
      - auto-exposure
```

Run the following to create Anaconda virtual environment

```
conda create -n lens python=3.9
conda activate lens
conda install pytorch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 pytorch-cuda=11.8 -c pytorch -c nvidia
pip install timm==0.9.10 pandas==1.5.3 lpips opencv_python
```

### 2. Run Validation

All execution scripts are prepared in `eval_scripts.sh`. You can run it by:

```
bash eval_scripts.sh
```

Results will be gathered in `val_results` directory

If validation is not available on your working environment, you can download log file for ResNet 50 [here](https://drive.google.com/file/d/1AKToR61rKwNqaxnYXc5YDtvsbmGblJ5u/view?usp=sharing).

You can place it in the following structure:

```
val_results
  - res50
    - eval_imagenet-es.pt
    - eval_imagenet-es-auto.pt
    - eval_imagenet-es-natural.pt
    - eval_imagenet-es-natural-auto.pt
```

### 3. Run Lens Evaluation

Use the following script to evaluate:

```
python3 lens_eval.py -a <model_name> -d <dataset_name>
python3 lens_eval.py -a <model_name> -d <dataset_name> --ae # for auto exposure
```
