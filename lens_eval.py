# This file is for Table 1 in the paper
# Requires log file
# To make log files, use --save-details in imagenet_es_eval.py

# Usage: python3 lens_eval.py -a <MODEL_NAME> -d <DATASET_NAME>

# Expected Dataset Structure
# - datasets
#   - ImageNet-ES
#     - sampled_tin_no_resize2
#     - es-test
#       - param-control
#       - auto-exposure
#   - ImageNet-ES-Natural
#     - es-natural-test
#       - param-control
#       - auto-exposure

import os
import torch
import argparse

DATASET_DIR = "path/to/datasets"
LOG_DIR = "path/to/ImageNet-ES-Natural/val_results"

class LensEvaluation:

    VERBOSE = True
    
    def __init__(self, dataset, model):
        self.dataset = dataset  # 'imagenet-es' or 'imagenet-es-natural'
        self.model = model
        self.log_path = os.path.join(LOG_DIR, self.model, f"eval_{self.dataset}.pt")
        self.ae_log_path = os.path.join(LOG_DIR, self.model, f"eval_{self.dataset}-auto.pt")

        if not os.path.exists(self.log_path):
            print(f"Cannot find log file: {self.log_path}")
            exit()

        self.log_file = torch.load(self.log_path)
        self.labels = self.get_labels()
        
        if dataset == 'imagenet-es':
            self.environments = ['l1', 'l5']
            self.dataset_size = 1000
            self.dataset_path = os.path.join(DATASET_DIR, 'ImageNet-ES')
        else:
            self.environments = ['l1', 'l2', 'l3', 'l4', 'l6', 'l7']  # 'l8', 'l9', 'l10' ommitted
            self.dataset_size = 400
            self.dataset_path = f'{DATASET_DIR}/ImageNet-ES-Natural'    
    
    def get_labels(self):
        try:
            label_path = f'{DATASET_DIR}/ImageNet-ES/sampled_tin_no_resize2'
            labels = os.listdir(label_path)
            assert len(labels) == 200
        except FileNotFoundError:
            print('Cannot find reference dataset: sampled_tin_no_resize2')
            exit()
        except AssertionError:
            print('Label count is not 200')
            exit()
        return labels
    
    def verbose(self, method, acc):
        if self.VERBOSE:
            print(f"{self.model} performance on {self.dataset} ({method}) : {acc:.2f} %")
    
    def ae(self):
        """
        Performance evalutation on auto exposure
        """
        if not os.path.exists(self.ae_log_path):
            print(f"Cannot find log file: {self.ae_log_path}")
            return 0
        else:
            self.ae_log_file = torch.load(self.ae_log_path)
            total = 0
            for env in self.environments:
                for i in range(1, 6):
                    for l in self.labels:
                        for img in self.ae_log_file[env][f'param_{i}'][l]:
                            total += self.ae_log_file[env][f'param_{i}'][l][img]['correct']

            acc = total / 5 / len(self.environments) / self.dataset_size * 100
            self.verbose("ae", acc)
            return acc
        
    def naive(self):
        """
        Mean performance of parameters
        """
        total = 0
        for e in self.environments:
            for p in range(1, 28):
                for l in self.labels:
                    for img in self.log_file[e][f'param_{p}'][l]:
                        total += self.log_file[e][f'param_{p}'][l][img]['correct']
                
        acc = total / 27 / len(self.environments) / self.dataset_size * 100
        self.verbose("naive", acc)
        return acc
    
    def oracle(self):
        """
        Performance of sample-wise best parameter selection
        """
        total = 0
        for e in self.environments:
            for l in self.labels:
                for i in self.log_file[e][f'param_1'][l]:
                    total += True in (self.log_file[e][f'param_{p}'][l][i]['correct'] == 1 for p in range(1, 28))
        
        acc = total / len(self.environments) / self.dataset_size * 100
        self.verbose("oracle", acc)
        return acc
    
    def bf(self):
        """
        Best performance of a single parameter over the whole test dataset
        """
        correct_per_params = [0] * 27
        for e in self.environments:
            for p in range(1, 28):
                for l in self.labels:
                    for image in self.log_file[e][f'param_{p}'][l].values():
                        correct_per_params[p-1] += int(image['correct'])
        
        acc = max([correct_per_params[i] / len(self.environments) / self.dataset_size for i in range(27)]) * 100
        self.verbose("best-fixed", acc)
        return acc
    
    def lens(self):
        """
        Performance of confidence-based parameter selection (Proposed method)
        """
        total = 0
        for e in self.environments:
            for l in self.labels:
                for i in self.log_file[e][f'param_1'][l]:
                    best_param = 1
                    best_conf = self.log_file[e][f'param_1'][l][i]['confidence'][0]
                    for p in range(2, 28):
                        if self.log_file[e][f'param_{p}'][l][i]['confidence'][0] > best_conf:
                            best_param = p
                            best_conf = self.log_file[e][f'param_{p}'][l][i]['confidence'][0]
                    total += self.log_file[e][f'param_{best_param}'][l][i]['correct']
        
        acc = total / len(self.environments) / self.dataset_size * 100
        self.verbose("lens", acc)
        return acc


def main():
    args = parser.parse_args()
    if args.data in ['imagenet-es', '1', 'es', 'es1']:
        dataset = 'imagenet-es'
    elif args.data in ['imagenet-es-natural', '2', 'esn', 'es2']:
        dataset = 'imagenet-es-natural'
    else:
        print('Dataset name not valid')
        return
    
    evaluation = LensEvaluation(dataset, args.arch)

    if args.ae:
        evaluation.ae()
    else:
        evaluation.naive()
        evaluation.oracle()
        evaluation.bf()
        evaluation.lens()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluation of Various Camera Control Methods on ImageNet-ES and ImageNet-ES-Natural')
    parser.add_argument('-a', '--arch', metavar='ARCH', default='res50',
                        help='model architecture (default: res50)')
    parser.add_argument('-d', '--data', default='imagenet-es-natural',
                        help='dataset (imagenet-es or imagenet-es-natural, abbreviated to 1 and 2)')
    parser.add_argument('--ae', action='store_true')
    
    main()