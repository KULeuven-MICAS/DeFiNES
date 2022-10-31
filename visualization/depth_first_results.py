
import pickle
from copy import deepcopy
from typing import Dict, List, Tuple
from typing import TYPE_CHECKING
from collections import defaultdict


if TYPE_CHECKING:
    from classes.cost_model.cost_model import CostModelEvaluation



def plot_cost_model(inputs: Dict[int, List[Tuple['CostModelEvaluation', int]]], title: str, block=False):
    import matplotlib.pyplot as plt
    from classes.mapping.combined_mapping import FourWayDataMoving
    from classes.depthfirst.data_copy_layer import DataCopyLayer

    memory_word_access_summed = {d[0].layer.id: defaultdict( lambda: defaultdict( lambda: FourWayDataMoving(0,0,0,0))) for d in inputs}
    memory_instances = {}

    layer_op_to_mem_op = {'O': 'O', 'W': 'I2', 'I': 'I1'}
    mem_op_to_layer_op = {'O': 'CO', 'I2': 'CW', 'I1': 'CI'}

    for cme in inputs:
            cme, extra = cme
            mh = cme.accelerator.get_core(cme.layer.core_allocation).memory_hierarchy
            for operand in cme.energy_breakdown_further:
                if isinstance(cme, DataCopyLayer):
                    mem_op = operand
                    layer_op = mem_op_to_layer_op[operand]
                else:
                    mem_op = cme.layer.memory_operand_links[operand]
                    layer_op = operand
                operand_memory_levels = mh.get_memory_levels(mem_op)
                for j in range(len(cme.energy_breakdown_further[operand])):
                    try:
                        mem = operand_memory_levels[j].name
                    except IndexError:
                        for d in cme.energy_breakdown_further[operand][j]:
                            if cme.energy_breakdown_further[operand][j][d] != 0:
                                raise ValueError("Non zero 4 way data movement for non-existing memory level")
                        continue
                    memory_instances[mem] = operand_memory_levels[j]
                    memory_word_access_summed[cme.layer.id][layer_op][mem] += \
                        cme.energy_breakdown_further[operand][j]


            # for operand in cme.memory_word_access:
            #     operand_memory_levels = mh.get_memory_levels(cme._CostModelEvaluation__main_inputs.layer.memory_operand_links[operand])
            #     for j in range(len(cme.memory_word_access[operand])):
            #         mem = operand_memory_levels[j].name
            #         memory_word_access_summed[l][operand][mem] += cme.memory_word_access[operand][j]*mul

    all_mems = set()
    for v in memory_word_access_summed.values():
        for vv in v.values():
            for vvv in vv.keys():
                all_mems.add(vvv)
    all_mems = sorted(list(all_mems), key=lambda m:memory_instances[m].memory_instance.size)
    all_ops = set()
    for v in memory_word_access_summed.values():
        for vv in v.keys():
            all_ops.add(vv)
    all_ops = sorted(list(all_ops))

    mac_costs = defaultdict(lambda :0)
    for l in inputs:
        cme, extra = l
        mac_costs[cme.layer.id] = cme.MAC_energy

    from matplotlib.colors import hsv_to_rgb
    import numpy as np
    hues = np.linspace(0, 1, len(all_ops)+1)[:-1]
    #sats = np.linspace(0.3, 1, 4)
    hatches = ['////', '\\\\\\\\', 'xxxx', '++++']

    plt.subplots(constrained_layout=True)
    x = 0
    xticks = {}
    for l in inputs:
        cme, extra = l
        l = cme.layer
        # if l == 'datamovement':
        #     e = sum(dcl.energy_total * mul for dcl, mul in inputs[l])
        #     plt.bar([x], [e], width=1, bottom=0, facecolor='purple')
        #     xticks[x] = 'Copy'
        #     plt.text(x+0.5, e, "{:,d}".format(int(e)),
        #              horizontalalignment='center', verticalalignment='top', weight='bold')
        #     x += 1+len(all_mems)/4
        #     continue
        total_energy = 0
        highest_bar = 0
        startx_of_layer = x
        #mac
        plt.bar([x], [mac_costs[l.id]], width=1, bottom=0, facecolor='k', alpha=0.5)
        total_energy+=mac_costs[l.id]
        highest_bar = mac_costs[l.id]
        xticks[x] = 'MAC'
        x+=1
        #mems
        for mem in all_mems:
            bottom = 0
            for op_i, operand in enumerate(all_ops):
                for dir_i, dir in enumerate(memory_word_access_summed[l.id][operand][mem]):
                    height=memory_word_access_summed[l.id][operand][mem][dir]
                    plt.bar([x], [height], width=1, bottom=[bottom],
                            facecolor=hsv_to_rgb((hues[op_i], 1, 1)), hatch=hatches[dir_i])

                    bottom+=height
            xticks[x] = mem
            total_energy += bottom
            x += 1
            highest_bar = max(bottom, highest_bar)
        plt.text(x*0.5 + startx_of_layer*0.5, highest_bar, "{:,d}".format(int(total_energy)),
                 horizontalalignment='center', verticalalignment='top', weight='bold')
        x += len(all_mems)/4

    for op, h in zip(all_ops, hues):
        plt.bar(0,0,width=1, facecolor = hsv_to_rgb((h, 1, 1)), label=op)

    for dir_i, dir in enumerate(memory_word_access_summed[l.id][operand][mem]):
        plt.bar([0],[0], width=1, bottom=0, facecolor=(1,1,1), hatch=hatches[dir_i], label=dir)

    plt.legend()
    plt.xticks(list(xticks.keys()), list(xticks.values()), rotation=90)
    plt.ylim(0.1, plt.ylim()[1])

    #plt.subplots_adjust(bottom=0.3, top=0.99, right=0.99, left=0.05)
    plt.xlabel("Layer", fontsize=18)
    plt.ylabel("Energy", fontsize=18)
    plt.title(title.split('/')[-1], fontsize=18)
    plt.show(block=block)


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
            plot_cost_model(loaded_data, p,  pi==len(paths)-1 and di==len(data)-1)

    # for cost model debug
    # data_collect[0][0][1][5][0][0].calc_memory_word_access()
    # data_collect[2][0][1][5][0][0].calc_memory_word_access()

    a = 1