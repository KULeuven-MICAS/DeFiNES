
import pickle
from copy import deepcopy
from typing import Dict, List, Tuple
from typing import TYPE_CHECKING
from collections import defaultdict
import numpy as np


if TYPE_CHECKING:
    from classes.cost_model.cost_model import CostModelEvaluation



def plot_max_mem_lv(inputs: Dict[int, List[Tuple['CostModelEvaluation', int]]], title: str, block=False):
    import matplotlib.pyplot as plt
    from classes.mapping.combined_mapping import FourWayDataMoving
    from classes.depthfirst.data_copy_layer import DataCopyLayer

    mem_lv_all_tile_all_layer = []
    for cme, extra_info in inputs:
        if isinstance(cme, DataCopyLayer):
            continue
        repetitive_time = [t for (_, t) in extra_info]
        mem_lv_all_tile_per_layer = [(extra_info[idx][0][0].active_mem_level, repetitive_time[idx]) for idx in range(len(extra_info))]
        for idx, a in enumerate(mem_lv_all_tile_per_layer):
            for op, mem_lv in a[0].items():
                if op=='W' and mem_lv==3:
                    mem_lv_all_tile_per_layer[idx][0]['W'] = 4
        mem_lv_all_tile_all_layer.append(mem_lv_all_tile_per_layer)

    nb_layer = len(mem_lv_all_tile_all_layer)
    nb_tile = len(mem_lv_all_tile_all_layer[0])
    lines = {op: [[] for _ in range(nb_tile)] for op in ['W', 'I', 'O']}
    for operand in ['W', 'I', 'O']:
        for layer_idx in range(nb_layer):
            for tile_idx in range(nb_tile):
                lines[operand][tile_idx].append(mem_lv_all_tile_all_layer[layer_idx][tile_idx][0][operand])

    fig, ax = plt.subplots(constrained_layout=True, figsize=(15, 4))
    x = [[nb_layer*j+i+1 for i in range(nb_layer)] for j in range(nb_tile)]
    y1 = lines['W']
    y2 = lines['I']
    y3 = lines['O']
    for i in range(len(x)-1):
        plt.plot(x[i], y1[i], '-gD')
        plt.plot(x[i], y2[i], '-r^')
        plt.plot(x[i], y3[i], '-b+')

    for i in range(len(x)-1, len(x)):
        plt.plot(x[i], y1[i], '-gD', label='Weight')
        plt.plot(x[i], y2[i], '-r^', label='Input')
        plt.plot(x[i], y3[i], '-b+', label='Output')

    plt.yticks(np.arange(1, 5), ['Reg', 'LB', 'GB', 'DRAM'])
    xlbls = [f'L{layer+1}' for tile_type in range(nb_tile) for layer in range(nb_layer)]
    plt.xticks(np.arange(1, 1+nb_layer*nb_tile), xlbls, rotation=45)
    vline_pos = [nb_layer*j+0.5 for j in range(1+nb_tile)]
    for idx, pos in enumerate(vline_pos):
        plt.axvline(x=pos, color='k', linestyle=':')
        if idx > 0:
            if repetitive_time[idx-1] == 1:
                plt.text((vline_pos[idx]+vline_pos[idx-1])/2, 1.3, f'Tile type {idx}\n({repetitive_time[idx-1]} time)', dict(size=12), ha='center', va='center')
            else:
                plt.text((vline_pos[idx]+vline_pos[idx-1])/2, 1.3, f'Tile type {idx}\n({repetitive_time[idx-1]} times)', dict(size=12), ha='center', va='center')
    plt.legend(loc='upper right')
    plt.xlabel("Tile type and Layer (L)", fontsize=18)
    plt.ylabel("Top Mem Level", fontsize=18)
    plt.title(title.split('/')[-1], fontsize=18)
    plt.show(block=block)
    # fig.savefig(f"{title.split('/')[-1]}.png", bbox_inches='tight')



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
            plot_max_mem_lv(loaded_data, p,  pi==len(paths)-1 and di==len(data)-1)

