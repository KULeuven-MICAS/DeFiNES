
import pickle
from copy import deepcopy
from typing import Dict, List, Tuple
from typing import TYPE_CHECKING
from collections import defaultdict
import numpy as np


if TYPE_CHECKING:
    from classes.cost_model.cost_model import CostModelEvaluation



def plot_total_data_size(inputs: Dict[int, List[Tuple['CostModelEvaluation', int]]], title: str, block=True):
    import matplotlib.pyplot as plt
    from classes.mapping.combined_mapping import FourWayDataMoving
    from classes.depthfirst.data_copy_layer import DataCopyLayer

    size_all_tile_all_layer = {'W': [], 'I': [], 'O': []}
    for cme, extra_info in inputs:
        if isinstance(cme, DataCopyLayer):
            continue
        repetitive_time = [t for (_, t) in extra_info]

        W_size_all_tile_per_layer = [extra_info[idx][0][1][0].operand_size_elem['W'] for idx in range(len(extra_info))]
        size_all_tile_all_layer['W'].append(W_size_all_tile_per_layer)

        I_size_all_tile_per_layer = [extra_info[idx][0][1][0].operand_size_elem['I'] for idx in range(len(extra_info))]
        size_all_tile_all_layer['I'].append(I_size_all_tile_per_layer)

        O_size_all_tile_per_layer = [extra_info[idx][0][1][0].operand_size_elem['O'] for idx in range(len(extra_info))]
        size_all_tile_all_layer['O'].append(O_size_all_tile_per_layer)

    nb_layer = len(size_all_tile_all_layer['O'])
    nb_tile = len(repetitive_time)
    bars = {op: [[] for _ in range(nb_tile)] for op in ['W', 'I', 'O']}
    for operand in ['W', 'I', 'O']:
        for layer_idx in range(nb_layer):
            for tile_idx in range(nb_tile):
                bars[operand][tile_idx].append(size_all_tile_all_layer[operand][layer_idx][tile_idx])

    fig, ax = plt.subplots(constrained_layout=True, figsize=(15, 4))
    x = [[nb_layer*j+i+1 for i in range(nb_layer)] for j in range(nb_tile)]
    x = np.array(x)
    y1 = bars['W']
    y2 = bars['I']
    y3 = bars['O']
    y2_largest = max([max(y2_li) for y2_li in y2])
    y3_largest = max([max(y3_li) for y3_li in y3])
    largest = max(y2_largest, y3_largest)
    width = 0.2  # the width of the bars
    for i in range(len(x)-1):
        # ax.bar(x[i] - width, y1[i],  width, facecolor='g')
        ax.bar(x[i] - 0.5*width, y2[i], width, facecolor='r', alpha=0.7)
        ax.bar(x[i] + 0.5*width, y3[i], width, facecolor='b', alpha=0.7)

    for i in range(len(x)-1, len(x)):
        # ax.bar(x[i] - width, y1[i], width, label='Weight', facecolor='g')
        ax.bar(x[i],         y2[i], width, label='Input', facecolor='r', alpha=0.7)
        ax.bar(x[i] + width, y3[i], width, label='Output', facecolor='b', alpha=0.7)

    # plt.yticks(np.arange(1, 5), ['Reg', 'LB', 'GB', 'DRAM'])
    xlbls = [f'L{layer+1}' for tile_type in range(nb_tile) for layer in range(nb_layer)]
    plt.xticks(np.arange(1, 1+nb_layer*nb_tile), xlbls, rotation=45)
    vline_pos = [nb_layer*j+0.5 for j in range(1+nb_tile)]
    for idx, pos in enumerate(vline_pos):
        plt.axvline(x=pos, color='k', linestyle=':')
        if idx > 0:
            if repetitive_time[idx-1] == 1:
                plt.text((vline_pos[idx]+vline_pos[idx-1])/2, largest*0.95, f'Tile type {idx}\n({repetitive_time[idx-1]} time)', dict(size=12), ha='center', va='center')
            else:
                plt.text((vline_pos[idx]+vline_pos[idx-1])/2, largest*0.95, f'Tile type {idx}\n({repetitive_time[idx-1]} times)', dict(size=12), ha='center', va='center')
    plt.legend(loc='upper right')
    plt.xlabel("Tile type and Layer (L)", fontsize=18)
    plt.ylabel("Data size (elem)", fontsize=18)
    plt.title(title.split('/')[-1], fontsize=18)
    plt.show(block=block)




    a=1

if __name__ == '__main__':
    import pickle
    import sys
    import glob
    data = sys.argv[1:]
    data_collect = []
    for di, d in enumerate(data):
        paths = glob.glob(d)
        for pi, p in enumerate(paths):
            print(p)
            with open(p, 'rb') as f:
                loaded_data = pickle.load(f)
                data_collect.append(loaded_data)
            plot_total_data_size(loaded_data, p,  pi==len(paths)-1 and di==len(data)-1)

