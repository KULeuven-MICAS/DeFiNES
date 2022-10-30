import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom", fontsize=11)

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.3f}",
                     textcolors=["black", "white"],
                     threshold=None, **textkw):
    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max()) / 2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts


from classes.depthfirst.data_copy_layer import DataCopyLayer
from math import ceil


def get_dram_access(data):
    dram_access_elem_copy_layer = 0
    dram_access_elem_normal_layer_A = 0
    dram_access_elem_normal_layer_W = 0
    layer_op_to_mem_op = {'O': 'O', 'W': 'I2', 'I': 'I1'}
    for idx, (cme, extra) in enumerate(data):
        if isinstance(cme, DataCopyLayer):
            for data_copy_layer, repeat_time in extra[1]:
                for data_copy_act in data_copy_layer[0].data_copy_actions:
                    for mem in data_copy_act.data_copy_mem_chain:
                        if mem[0].name == 'dram':
                            dram_access_elem_copy_layer += ceil(data_copy_act.data_amount / 8) * repeat_time
        else:
            for normal_layer, repeat_time in extra[1]:
                elem_move_collect = normal_layer[0].mapping.unit_mem_data_movement
                for op, va in elem_move_collect.items():
                    dram_access_elem = 0
                    if len(va) == len(cme.accelerator.cores[0].mem_hierarchy_dict[layer_op_to_mem_op[op]]):
                        dram_access_elem = (va[-1].data_elem_move_count.rd_out_to_high +
                                            va[-1].data_elem_move_count.rd_out_to_low +
                                            va[-1].data_elem_move_count.wr_in_by_high +
                                            va[-1].data_elem_move_count.wr_in_by_low) \
                                           * repeat_time
                    if op == 'W':
                        dram_access_elem_normal_layer_W += dram_access_elem
                    else:
                        dram_access_elem_normal_layer_A += dram_access_elem

    return int(dram_access_elem_copy_layer), int(dram_access_elem_normal_layer_A), int(dram_access_elem_normal_layer_W)


def get_gb_access(data):
    gb_access_elem_copy_layer = 0
    gb_access_elem_normal_layer_A = 0
    gb_access_elem_normal_layer_W = 0
    layer_op_to_mem_op = {'O': 'O', 'W': 'I2', 'I': 'I1'}
    for idx, (cme, extra) in enumerate(data):
        if isinstance(cme, DataCopyLayer):
            for data_copy_layer, repeat_time in extra[1]:
                for data_copy_act in data_copy_layer[0].data_copy_actions:
                    for mem in data_copy_act.data_copy_mem_chain:
                        if mem[0].name == 'sram_1MB_A':
                            gb_access_elem_copy_layer += ceil(data_copy_act.data_amount / 8) * repeat_time
        else:
            for normal_layer, repeat_time in extra[1]:
                elem_move_collect = normal_layer[0].mapping.unit_mem_data_movement
                for op, va in elem_move_collect.items():
                    gb_access_elem = 0
                    if len(va) == len(cme.accelerator.cores[0].mem_hierarchy_dict[layer_op_to_mem_op[op]]):
                        gb_access_elem = (va[-2].data_elem_move_count.rd_out_to_high +
                                          va[-2].data_elem_move_count.rd_out_to_low +
                                          va[-2].data_elem_move_count.wr_in_by_high +
                                          va[-2].data_elem_move_count.wr_in_by_low) \
                                         * repeat_time
                    elif len(va) == len(cme.accelerator.cores[0].mem_hierarchy_dict[layer_op_to_mem_op[op]]) - 1:
                        gb_access_elem = (va[-1].data_elem_move_count.rd_out_to_high +
                                          va[-1].data_elem_move_count.rd_out_to_low +
                                          va[-1].data_elem_move_count.wr_in_by_high +
                                          va[-1].data_elem_move_count.wr_in_by_low) \
                                         * repeat_time
                    if op == 'W':
                        gb_access_elem_normal_layer_W += gb_access_elem
                    else:
                        gb_access_elem_normal_layer_A += gb_access_elem

    return int(gb_access_elem_copy_layer), int(gb_access_elem_normal_layer_A), int(gb_access_elem_normal_layer_W)


def get_lb_access(data):
    lb_access_elem_copy_layer = 0
    lb_access_elem_normal_layer_A = 0
    lb_access_elem_normal_layer_W = 0
    for idx, (cme, extra) in enumerate(data):
        if isinstance(cme, DataCopyLayer):
            for data_copy_layer, repeat_time in extra[1]:
                for data_copy_act in data_copy_layer[0].data_copy_actions:
                    for mem in data_copy_act.data_copy_mem_chain:
                        if mem[0].name == 'sram_64KB':
                            lb_access_elem_copy_layer += ceil(data_copy_act.data_amount / 8) * repeat_time
        else:
            for normal_layer, repeat_time in extra[1]:
                elem_move_collect = normal_layer[0].mapping.unit_mem_data_movement
                for op, va in elem_move_collect.items():
                    if op == 'I':
                        lb_access_elem = (va[0].data_elem_move_count.rd_out_to_high +
                                          va[0].data_elem_move_count.rd_out_to_low +
                                          va[0].data_elem_move_count.wr_in_by_high +
                                          va[0].data_elem_move_count.wr_in_by_low) \
                                         * repeat_time
                    else:
                        lb_access_elem = (va[1].data_elem_move_count.rd_out_to_high +
                                          va[1].data_elem_move_count.rd_out_to_low +
                                          va[1].data_elem_move_count.wr_in_by_high +
                                          va[1].data_elem_move_count.wr_in_by_low) \
                                         * repeat_time
                    if op == 'W':
                        lb_access_elem_normal_layer_W += lb_access_elem
                    else:
                        lb_access_elem_normal_layer_A += lb_access_elem

    return int(lb_access_elem_copy_layer), int(lb_access_elem_normal_layer_A), int(lb_access_elem_normal_layer_W)


def get_total_en_la(data):
    total_en = 0
    total_la = 0
    for cme, extra_info in data:
        total_en += cme.energy_total
        total_la += cme.latency_total1

    return total_en, total_la


def get_en_breakdown(data):
    from classes.depthfirst.data_copy_layer import DataCopyLayer
    en_break_down = {'MAC': 0, 'Normal Layer': 0, 'Data Copy Layer': 0}
    for cme, extra in data:
        if isinstance(cme, DataCopyLayer):
            en_break_down['Data Copy Layer'] += cme.energy_total
        else:
            en_break_down['MAC'] += cme.MAC_energy
            en_break_down['Normal Layer'] += cme.mem_energy

    return en_break_down


def get_la_breakdown(data):
    from classes.depthfirst.data_copy_layer import DataCopyLayer
    la_break_down = {'Ideal Computation': 0, 'Spatial Stall': 0, 'Temporal Stall': 0, 'Data Preparation': 0}
    for cme, extra in data:
        if isinstance(cme, DataCopyLayer):
            la_break_down['Data Preparation'] += cme.latency_total
        else:
            la_break_down['Ideal Computation'] += cme.ideal_cycle
            la_break_down['Spatial Stall'] += (cme.ideal_temporal_cycle - cme.ideal_cycle)
            la_break_down['Temporal Stall'] += (cme.latency_total0 - cme.ideal_temporal_cycle)
            la_break_down['Data Preparation'] += (cme.latency_total1 - cme.latency_total0)

    return la_break_down


def get_tile_type_count(data):
    tile_type_count = 0
    for idx, (cme, extra) in enumerate(data):
        if isinstance(cme, DataCopyLayer):
            continue
        else:
            tile_type_count = len(extra[1])
        break
    return tile_type_count


def get_MAC_count(data):
    MAC_count = 0
    for idx, (cme, extra) in enumerate(data):
        if isinstance(cme, DataCopyLayer):
            continue
        else:
            for normal_layer, repeat_time in extra[1]:
                MAC_count += normal_layer[1][0].total_MAC_count * repeat_time
    return MAC_count


def data_collect(result_saving_path):
    import glob
    import re
    import pickle

    class DataToPlot:
        def __init__(self):
            self.en_collect = {}
            self.la_collect = {}
            self.MAC_collect = {}
            self.dram_access_collect = {}
            self.dram_access_collect_copy_layer = {}
            self.dram_access_collect_normal_layer_A = {}
            self.dram_access_collect_normal_layer_W = {}
            self.gb_access_collect = {}
            self.gb_access_collect_copy_layer = {}
            self.gb_access_collect_normal_layer_A = {}
            self.gb_access_collect_normal_layer_W = {}
            self.lb_access_collect = {}
            self.lb_access_collect_copy_layer = {}
            self.lb_access_collect_normal_layer_A = {}
            self.lb_access_collect_normal_layer_W = {}
            self.tile_type_collect = {}

    data_to_plot = DataToPlot()
    paths = glob.glob(f'{result_saving_path}/*.pkl')
    for idx, path in enumerate(paths):
        print(f'Reading in result -- {path}')
        ky = re.split('[/ .]', path)[-2]
        with open(path, 'rb') as f:
            data = pickle.load(f)
        f.close()

        data_to_plot.en_collect[ky], data_to_plot.la_collect[ky] = get_total_en_la(data)
        data_to_plot.MAC_collect[ky] = get_MAC_count(data)

        dram_access1, dram_access2, dram_access3 = get_dram_access(data)
        data_to_plot.dram_access_collect[ky] = dram_access1 + dram_access2 + dram_access3
        data_to_plot.dram_access_collect_copy_layer[ky] = dram_access1
        data_to_plot.dram_access_collect_normal_layer_A[ky] = dram_access2
        data_to_plot.dram_access_collect_normal_layer_W[ky] = dram_access3

        gb_access1, gb_access2, gb_access3 = get_gb_access(data)
        data_to_plot.gb_access_collect[ky] = gb_access1 + gb_access2 + gb_access3
        data_to_plot.gb_access_collect_copy_layer[ky] = gb_access1
        data_to_plot.gb_access_collect_normal_layer_A[ky] = gb_access2
        data_to_plot.gb_access_collect_normal_layer_W[ky] = gb_access3

        lb_access1, lb_access2, lb_access3 = get_lb_access(data)
        data_to_plot.lb_access_collect[ky] = lb_access1 + lb_access2 + lb_access3
        data_to_plot.lb_access_collect_copy_layer[ky] = lb_access1
        data_to_plot.lb_access_collect_normal_layer_A[ky] = lb_access2
        data_to_plot.lb_access_collect_normal_layer_W[ky] = lb_access3

        data_to_plot.tile_type_collect[ky] = get_tile_type_count(data)

    return data_to_plot
