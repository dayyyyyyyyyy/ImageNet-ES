
import torch as ch
from PIL import Image
import seaborn as sns
import numpy as np
from robustness.tools.vis_tools import show_image_column
import matplotlib.pyplot as plt
import colorcet as cc
from sklearn.manifold import TSNE

from configs.tin_config import LOADER_CONFIG
from configs.datasets import DATA_ROOT_DIR, SAMPLE_DIR_MAP, OPS_NUM
from utils.visual_encoding import LABEL_DICT, COLOR

TRANSFORMATIONS = LOADER_CONFIG['DATA_TRANSFORMS']
ENVIRONMENTS = ['l1', 'l3'] #, 'l3', 'l4', 'l6', 'l7', 'l8', 'l9', 'l10']
N = 3
LIMIT = 10

class Interest():
    def __init__(self, accs_pc_df, accs_ae_df):
        self.accs_pc_df = accs_pc_df
        self.accs_ae_df = accs_ae_df
        
    def get_interest_settings(self, TARGET_ENV):
        TARGETS = self.accs_pc_df[self.accs_pc_df['Light']==TARGET_ENV]
        interest_settings = {
            f'BEST{N}_SETTING': list(TARGETS.nlargest(N,'Acc.')['Camera Parameter'])[:N],
            f'WORST{N}_SETTING': list(TARGETS.nsmallest(N,'Acc.')['Camera Parameter'])[:N],
            f'MAL{N}_SETTING': list(TARGETS.nlargest(10,'Acc.')['Camera Parameter'])[LIMIT-N:LIMIT],
            'AUTO5_SETTING': list(map(lambda i: f'param_{i}', range(1,5+1))),
        }
        print(interest_settings)
        return interest_settings 

class QualCanvas(Interest):
    def __init__(self, accs_pc_df, accs_ae_df, dataset_dir=DATA_ROOT_DIR, target_dir='es2-test', sample_dir_map=SAMPLE_DIR_MAP):
        super().__init__(accs_pc_df, accs_ae_df)
        
        self.dataset_dir = dataset_dir
        self.target_dir = target_dir
        self.sample_dir_map = sample_dir_map

        interests = {e: self.get_interest_settings(e) for e in ENVIRONMENTS}
        
        self.top5s, self.bot5s = dict(), dict()
        for e, interest in interests.items():
            self.top5s[e] = [int(setting_name.split('_')[-1]) for setting_name in interest[f'BEST{N}_SETTING']]
            self.bot5s[e] = [int(setting_name.split('_')[-1]) for setting_name in interest[f'WORST{N}_SETTING']]
        
        def to_avg_acc(target_settings, env, target_df=self.accs_pc_df):
            targets = target_df[target_df['Light']==env]
            return sum(list(targets[targets['Camera Parameter'].isin(target_settings)]['Acc.']))/len(target_settings)
        
        self.avg_acc = {
            'sampled': 86.3,
        }
        for e, interest in interests.items():
            self.avg_acc[f'top{N}_{e}'] = to_avg_acc(interest[f'BEST{N}_SETTING'], e)
            self.avg_acc[f'bot{N}_{e}'] = to_avg_acc(interest[f'WORST{N}_SETTING'], e)
            self.avg_acc[f'ae5_{e}'] = to_avg_acc(interest['AUTO5_SETTING'], e, target_df=self.accs_ae_df)
  
            
    def set_target_dir(self, target_dir_name):
        self.target_dir = target_dir_name
    
    def load_img(self, FULL_PATH):
            try:
                image = Image.open(FULL_PATH)
                tensor = TRANSFORMATIONS['draw'](image)
            except Exception as e:
                print(e, FULL_PATH)
                tensor = ch.ones((3,224,224))
                tensor[1] *= 0
                tensor[2] *= 0
            return tensor
    
    def load_imgs(self, path, obj, splits=None):
        
        ROOT_DIR = f'{self.dataset_dir}/{self.target_dir}'
        obj_path = dict()

        for e in ENVIRONMENTS:
            obj_path[f'ae_{e}'] = f'auto_exposure/{e}'
            obj_path[f'pc_{e}'] = f'param_control/{e}'
        
        ops_num = OPS_NUM[self.target_dir]
        
        ae_num = splits if splits else 3
        obj_param_num = dict()

        for e in ENVIRONMENTS:
            obj_param_num[f'ae_{e}'] = [f'param_{i+1}' for i in range(ae_num)]
            obj_param_num[f'pc_{e}'] = [f'param_{i}' for i in range(1,ops_num+1)]

        FINAL_ROOT_PATH = f'{ROOT_DIR}/{obj_path[obj]}'
        
        tensors = ch.stack(list(map(lambda obj_param: self.load_img(f'{FINAL_ROOT_PATH}/{obj_param}/{path}'), obj_param_num[obj])),axis=0)
        if splits:
            column_nums = len(tensors)//splits
            tensors_divided = [tensors[column_nums*i:column_nums*(i+1)] for i in range(splits)]
            return tensors_divided
        return tensors
    
    def draw_representatives(self, path, file_name=None, splits=3):
        pc_l1 = self.load_imgs(path,'pc_l1', splits=splits)
        pc_l5 = self.load_imgs(path,'pc_l5', splits=splits)
        ae_l1 = self.load_imgs(path,'ae_l1', splits=splits)
        ae_l5 = self.load_imgs(path,'ae_l5', splits=splits)
        empty = ch.ones(ae_l1[0].shape)

        rows = [
            *[ch.concat([s_ae, s_pc])for s_ae, s_pc in zip(ae_l1, pc_l1)],
            *[ch.concat([s_ae, s_pc])for s_ae, s_pc in zip(ae_l5, pc_l5)],
        ]
        
        titles_rows = [
            *[['On-AE']+ [f'On-{i*len(s_pc)+j+1}' for j in range(len(s_pc))] for i, (_, s_pc) in enumerate(zip(ae_l1, pc_l1))],
            *[['Off-AE']+ [f'Off-{i*len(s_pc)+j+1}' for j in range(len(s_pc))] for i, (_, s_pc) in enumerate(zip(ae_l5, pc_l5))],
        ]
        
        cols = [ ch.stack([*col]) for col in zip(*rows)]
        titles_cols = [ [*col] for col in zip(*titles_rows)]
        
        
        for i, sample in enumerate(cols[0]):
            if i % splits !=0:
                cols[0][i] = empty
                titles_cols[0][i] = ''
        
        ROOT_DIR = f'{self.dataset_dir}/{self.target_dir}/{self.sample_dir_map[self.target_dir]}'
        ORIGINAL_PATH = f'{ROOT_DIR}/{path}'
        original_img = self.load_img(ORIGINAL_PATH)
        show_image_column([[original_img]], tlist=[['Original sample']])
        
        show_image_column(cols,  ['' for i in range(1,len(cols)+1)], filename=file_name, tlist=titles_cols)
    
    def draw_qualitatives(self, path_list, picked_list, file_name=None):
        rows = []
        for path, picked in zip(path_list, picked_list):
            rows.append(self.get_quals(path, picked))
        titles = [f'sampled\n{self.avg_acc["sampled"]:.2f}%',]

        for e in ENVIRONMENTS:
            titles.append(f'{e} top {N}\n{self.avg_acc[f"top{N}_{e}"]:.2f}%')
            titles.append(f'{e} bottom {N}\n{self.avg_acc[f"bot{N}_{e}"]:.2f}%')
            titles.append(f'{e} AE 5\n{self.avg_acc[f"ae5_{e}"]:.2f}%')
            
        self.draw_multiple_qualitatives(rows, titles, file_name=file_name)
     
    def draw_multiple_qualitatives(self, targets, titles, file_name=None):
        targets = [ch.concat([*xx]) for xx in zip(*targets)]
        print('Qualitative results of ImageNet-ES\n(avgerage accuracy of each group)')
        show_image_column(targets, titles, filename=file_name)
        return None   
    
    def get_quals(self, path, picked):
        
        pc, ae = dict(), dict()
        
        for e in ENVIRONMENTS:
            pc[e] = self.load_imgs(path, f'pc_{e}')
            ae[e] = self.load_imgs(path, f'ae_{e}')
        
        targets = []
        for i, e in enumerate(ENVIRONMENTS):
            b, w = picked[i]
            targets.append(pc[e][self.top5s[e][b:b+1]])
            targets.append(pc[e][self.bot5s[e][w:w+1]])
            targets.append(ae[e][0:1])
        
        ROOT_DIR = f'{self.dataset_dir}/{self.target_dir}/{self.sample_dir_map[self.target_dir]}'
        ORIGINAL_PATH = f'{ROOT_DIR}/{path}'
        image = Image.open(ORIGINAL_PATH)
        tensor = TRANSFORMATIONS['draw'](image)
        final = [ch.stack([tensor])]
        return final+targets

class FeatureCanvas(Interest):
    def __init__(self, accs_pc_df, accs_ae_df, fvs):
        super().__init__(accs_pc_df, accs_ae_df)
        self.fvs = fvs  
    
    def plot_vecs_n_labels(self, v, labels, ax=None):
        ax.axis('off')
        sns.set_style('darkgrid')
        palette = sns.color_palette(cc.glasbey, n_colors=200)
        sns.scatterplot(x=v[:,0], y=v[:,1], hue=labels, legend='brief', palette=palette, ax=ax, s=20)
        ax.get_legend().remove()

    def draw_embeddings(self, data_list, ax, perplexity=30, title=None):
        fs = []
        labels = []
        for data in data_list:
            fs += sum(data.values(),[])
            labels += sum(map(lambda x: [x]*2, data.keys()), [])
        fs = np.array(fs)
        pred_tsne = TSNE(n_components=2, perplexity=perplexity).fit_transform(fs)
        self.plot_vecs_n_labels(pred_tsne, labels,  ax=ax)
        if title:
            ax.set_title(f'{title}', fontsize=20)
    
    def draw_multiple_embeddings(self, fv_dict, figsize=(16,4), file_name=None):
        fig, axes = plt.subplots(1,len(fv_dict), figsize=figsize)
        for i, (setting_name, data) in enumerate(fv_dict.items()):
            self.draw_embeddings(data, axes[i], title=LABEL_DICT[setting_name])
        plt.tight_layout()
        
        if file_name:
            plt.savefig(file_name)
            
    def plot_activation_dist(self, activations, file_name=None):
        # plt.figure(figsize=(6,2))
        subfigs = len(activations.keys())
        fig, axs = plt.subplots(subfigs, 1, figsize=(6, 2 * subfigs))
        max_y = 2
        
        for i, (k, v) in enumerate(activations.items()):
            targets = v.values()
            fv_num = len(list(targets)[0][0])
            
            axs[i].plot(range(fv_num), np.array(sum(targets,[])).mean(axis=0), label=LABEL_DICT[k], c=COLOR[k])
            axs[i].legend()
            axs[i].set_ylim(0, max_y)
            
        plt.ylabel('Activation', fontsize=10)
        plt.xlabel('Feature representation indices', fontsize=10)
        plt.tight_layout()
        
        if file_name:
            plt.savefig(file_name)
        
        



