
################################### PyTorch evaluation script ############################################

CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a eff_b0 -b 1024 --pretrained     --dataset imagenet-tin --log_file logs_eff_b0_imagenet-tin.txt 
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a eff_b0 -b 1024 --pretrained     --dataset imagenet-es-natural     --log_file logs_eff_b0_imagenet-es-natural.txt  --save_details
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a eff_b0 -b 1024 --pretrained     --dataset imagenet-es-natural-auto     --log_file logs_eff_b0_imagenet-es-natural-auto.txt  --save_details


CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res50 -b 1024 --pretrained     --dataset imagenet-tin --log_file logs_res50_imagenet-tin.txt 
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res50 -b 1024 --pretrained     --dataset imagenet-es-natural     --log_file logs_res50_imagenet-es-natural.txt --save_features  --save_details
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res50 -b 1024 --pretrained     --dataset imagenet-es-natural-auto     --log_file logs_res50_imagenet-es-natural-auto.txt --save_features  --save_details

CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res152 --pretrained --dataset imagenet-tin --log_file logs_res152_imagenet-tin.txt 
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res152 --pretrained --dataset imagenet-es-natural     --log_file logs_res152_imagenet-es-natural.txt  --save_details
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res152 --pretrained --dataset imagenet-es-natural-auto     --log_file logs_res152_imagenet-es-natural-auto.txt  --save_details

CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res50_aug -b 1024 --pretrained --dataset imagenet-tin --log_file logs_res50_aug_imagenet-tin.txt  
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res50_aug -b 1024 --pretrained --dataset imagenet-es-natural     --log_file logs_res50_aug_imagenet-es-natural.txt  --save_details
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res50_aug -b 1024 --pretrained --dataset imagenet-es-natural-auto     --log_file logs_res50_aug_imagenet-es-natural-auto.txt  --save_details

CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_t -b 1024 --pretrained --dataset imagenet-tin --log_file logs_swin_t_imagenet-tin.txt 
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_t -b 1024 --pretrained --dataset imagenet-es-natural     --log_file logs_swin_t_imagenet-es-natural.txt  --save_details
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_t -b 1024 --pretrained --dataset imagenet-es-natural-auto     --log_file logs_swin_t_imagenet-es-natural-auto.txt  --save_details

CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_s -b 1024 --pretrained --dataset imagenet-tin --log_file logs_swin_s_imagenet-tin.txt 
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_s -b 1024 --pretrained --dataset imagenet-es-natural     --log_file logs_swin_s_imagenet-es-natural.txt  --save_details
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_s -b 1024 --pretrained --dataset imagenet-es-natural-auto     --log_file logs_swin_s_imagenet-es-natural-auto.txt  --save_details

CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_b -b 1024 --pretrained --dataset imagenet-tin --log_file logs_swin_b_imagenet-tin.txt  
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_b -b 1024 --pretrained --dataset imagenet-es-natural     --log_file logs_swin_b_imagenet-es-natural.txt  --save_details
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_b -b 1024 --pretrained --dataset imagenet-es-natural-auto     --log_file logs_swin_b_imagenet-es-natural-auto.txt  --save_details

CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a dinov2 --pretrained --dataset imagenet-tin --log_file logs_dinov2_imagenet-tin.txt 
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a dinov2 --pretrained --dataset imagenet-es-natural --log_file logs_dinov2_imagenet-es-natural.txt  --save_details
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a dinov2 --pretrained --dataset imagenet-es-natural-auto --log_file logs_dinov2_imagenet-es-natural-auto.txt  --save_details

CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a dinov2_b --pretrained --dataset imagenet-tin --log_file logs_dinov2_b_imagenet-tin.txt 
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a dinov2_b --pretrained --dataset imagenet-es-natural --log_file logs_dinov2_b_imagenet-es-natural.txt  --save_details
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a dinov2_b --pretrained --dataset imagenet-es-natural-auto --log_file logs_dinov2_b_imagenet-es-natural-auto.txt  --save_details

CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a eff_b3 -b 1024 --pretrained     --dataset imagenet-tin --log_file logs_eff_b3_imagenet-tin.txt 
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a eff_b3 -b 1024 --pretrained     --dataset imagenet-es-natural     --log_file logs_eff_b3_imagenet-es-natural.txt  --save_details
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a eff_b3 -b 1024 --pretrained     --dataset imagenet-es-natural-auto     --log_file logs_eff_b3_imagenet-es-natural-auto.txt  --save_details


# OpenCLIP is not supported by PyTorch, instead use timm version
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a clip_b --pretrained --timm    --dataset imagenet-tin --log_file logs_clip_l_imagenet-tin_timm.txt  
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a clip_b --pretrained --timm    --dataset imagenet-es-natural --log_file logs_clip_b_imagenet-es-natural_timm.txt   --save_details
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a clip_b --pretrained --timm    --dataset imagenet-es-natural-auto --log_file logs_clip_b_imagenet-es-natural-auto_timm.txt  --save_details

CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a clip_h --pretrained --timm    --dataset imagenet-tin --log_file logs_clip_h_imagenet-tin_timm.txt  
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a clip_h --pretrained --timm    --dataset imagenet-es-natural --log_file logs_clip_h_imagenet-es-natural_timm.txt   --save_details
CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a clip_h --pretrained --timm    --dataset imagenet-es-natural-auto --log_file logs_clip_h_imagenet-es-natural-auto_timm.txt  --save_details

################################### TIMM evaluation script ############################################

# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res50 -b 1024 --pretrained --timm    --dataset imagenet-tin --log_file logs_res50_imagenet-tin_timm.txt
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res50 -b 1024 --pretrained --timm    --dataset imagenet-es-natural     --log_file logs_res50_imagenet-es-natural_timm.txt
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res50 -b 1024 --pretrained --timm    --dataset imagenet-es-natural-auto     --log_file logs_res50_imagenet-es-natural-auto_timm.txt

# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res152 --pretrained --timm    --dataset imagenet-tin --log_file logs_res152_imagenet-tin_timm.txt
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res152 --pretrained --timm    --dataset imagenet-es-natural     --log_file logs_res152_imagenet-es-natural_timm.txt
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res152 --pretrained --timm    --dataset imagenet-es-natural-auto     --log_file logs_res152_imagenet-es-natural-auto_timm.txt

# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res50_aug -b 1024 --pretrained --timm            --dataset imagenet-tin --log_file logs_res50_aug_imagenet-tin.txt
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res50_aug -b 1024 --pretrained --timm     --dataset imagenet-es-natural     --log_file logs_res50_aug_imagenet-es-natural.txt
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a res50_aug -b 1024 --pretrained --timm     --dataset imagenet-es-natural-auto     --log_file logs_res50_aug_imagenet-es-natural-auto.txt

# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_t -b 1024 --pretrained --timm    --dataset imagenet-tin --log_file logs_swin_t_imagenet-tin_timm.txt
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_t -b 1024 --pretrained --timm    --dataset imagenet-es-natural     --log_file logs_swin_t_imagenet-es-natural_timm.txt
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_t -b 1024 --pretrained --timm    --dataset imagenet-es-natural-auto     --log_file logs_swin_t_imagenet-es-natural-auto_timm.txt

# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_s -b 1024 --pretrained --timm    --dataset imagenet-tin --log_file logs_swin_s_imagenet-tin_timm.txt
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_s -b 1024 --pretrained --timm    --dataset imagenet-es-natural     --log_file logs_swin_s_imagenet-es-natural_timm.txt
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_s -b 1024 --pretrained --timm    --dataset imagenet-es-natural-auto     --log_file logs_swin_s_imagenet-es-natural-auto_timm.txt

# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_b -b 1024 --pretrained --timm    --dataset imagenet-tin --log_file logs_swin_b_imagenet-tin_timm.txt
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_b -b 1024 --pretrained --timm    --dataset imagenet-es-natural     --log_file logs_swin_b_imagenet-es-natural_timm.txt
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_b -b 1024 --pretrained --timm    --dataset imagenet-es-natural-auto     --log_file logs_swin_b_imagenet-es-natural-auto_timm.txt

# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_l --pretrained --timm    --dataset imagenet-tin --log_file logs_swin_l_imagenet-tin_timm.txt
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_l --pretrained --timm    --dataset imagenet-es-natural     --log_file logs_swin_l_imagenet-es-natural_timm.txt
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a swin_l --pretrained --timm    --dataset imagenet-es-natural-auto     --log_file logs_swin_l_imagenet-es-natural-auto_timm.txt

# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a dinov2 --pretrained --timm    --dataset imagenet-tin --log_file logs_dinov2_imagenet-tin_timm.txt
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a dinov2 --pretrained --timm    --dataset imagenet-es-natural --log_file logs_dinov2_imagenet-es-natural_timm.txt
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a dinov2 --pretrained --timm    --dataset imagenet-es-natural-auto --log_file logs_dinov2_imagenet-es-natural-auto_timm.txt

# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a clip_b --pretrained --timm    --dataset imagenet-tin --log_file logs_clip_l_imagenet-tin_timm.txt 
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a clip_b --pretrained --timm    --dataset imagenet-es-natural --log_file logs_clip_b_imagenet-es-natural_timm.txt 
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a clip_b --pretrained --timm    --dataset imagenet-es-natural-auto --log_file logs_clip_b_imagenet-es-natural-auto_timm.txt

# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a clip_l --pretrained --timm    --dataset imagenet-tin --log_file logs_clip_l_imagenet-tin_timm.txt 
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a clip_l --pretrained --timm    --dataset imagenet-es-natural --log_file logs_clip_l_imagenet-es-natural_timm.txt --data_root ~/datasets
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a clip_l --pretrained --timm    --dataset imagenet-es-natural-auto --log_file logs_clip_l_imagenet-es-natural-auto_timm.txt --data_root ~/datasets


# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a clip_h --pretrained --timm    --dataset imagenet-tin --log_file logs_clip_h_imagenet-tin_timm.txt 
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a clip_h --pretrained --timm    --dataset imagenet-es-natural --log_file logs_clip_h_imagenet-es-natural_timm.txt 
# CUDA_VISIBLE_DEVICES=0 python imagenet_es_eval.py -a clip_h --pretrained --timm    --dataset imagenet-es-natural-auto --log_file logs_clip_h_imagenet-es-natural-auto_timm.txt
