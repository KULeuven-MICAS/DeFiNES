import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from plot_cs1_helper_funcs import heatmap, annotate_heatmap, data_collect


def plot_Fig12_total_en_and_la_heatmap(plotinfo):
    # plotinfo: a numpy array of 3 rows for different overlap-storing modes, 2 columns for energy and latency, and a 6x6 y by x tilesize grid
    fig, ax = plt.subplots(3, 2, figsize=(10, 8))
    x_label = [1, 4, 16, 60, 240, 960]
    y_label = [1, 4, 18, 72, 270, 540]

    for storing_more in range(3):
        for y_tile in range(6):
            for x_tile in range(6):
                plotinfo[storing_more][0][y_tile][x_tile] /= 1e9  # change energy's unit from pJ to mJ
    for storing_more in range(3):
        for y_tile in range(6):
            for x_tile in range(6):
                plotinfo[storing_more][1][y_tile][x_tile] /= 1e6  # change latency's unit from cycle to million cycles

    im, cbar = heatmap(plotinfo[0][0], y_label, x_label, ax=ax[0][0], cmap="viridis_r", cbarlabel='Energy (mJ)', norm=colors.LogNorm(vmin=1.8, vmax=47.3))
    annotate_heatmap(im, valfmt="{x:.1f}")
    ax[0][0].set_title('Fully-recompute, Energy')
    ax[0][0].set_ylabel('Y-Dim Tile Size (Ty)')
    ax[0][0].set_xlabel('X-Dim Tile Size (Tx)')
    ax[0][0].set_aspect(5/7)

    im, cbar = heatmap(plotinfo[1][0], y_label, x_label, ax=ax[1][0], cmap="viridis_r", cbarlabel='Energy (mJ)', norm=colors.LogNorm(vmin=1.8, vmax=47.3))
    annotate_heatmap(im, valfmt="{x:.1f}")
    ax[1][0].set_title('H-cached V-recompute, Energy')
    ax[1][0].set_ylabel('Y-Dim Tile Size (Ty)')
    ax[1][0].set_xlabel('X-Dim Tile Size (Tx)')
    ax[1][0].set_aspect(5/7)

    im, cbar = heatmap(plotinfo[2][0], y_label, x_label, ax=ax[2][0], cmap="viridis_r", cbarlabel='Energy (mJ)', norm=colors.LogNorm(vmin=1.8, vmax=47.3))
    annotate_heatmap(im, valfmt="{x:.1f}")
    ax[2][0].set_title('Fully-cached, Energy')
    ax[2][0].set_ylabel('Y-Dim Tile Size (Ty)')
    ax[2][0].set_xlabel('X-Dim Tile Size (Tx)')
    ax[2][0].set_aspect(5/7)

    im, cbar = heatmap(plotinfo[0][1], y_label, x_label, ax=ax[0][1], cmap="viridis_r", cbarlabel='Latency (million cycle)', norm=colors.LogNorm(vmin=18, vmax=1026))
    annotate_heatmap(im, valfmt="{x:.0f}")
    ax[0][1].set_title('Fully-recompute, Latency')
    ax[0][1].set_ylabel('Y-Dim Tile Size (Ty)')
    ax[0][1].set_xlabel('X-Dim Tile Size (Tx)')
    ax[0][1].set_aspect(5/7)

    im, cbar = heatmap(plotinfo[1][1], y_label, x_label, ax=ax[1][1], cmap="viridis_r", cbarlabel='Latency (million cycle)', norm=colors.LogNorm(vmin=18, vmax=1026))
    annotate_heatmap(im, valfmt="{x:.0f}")
    ax[1][1].set_title('H-cached V-recompute, Latency')
    ax[1][1].set_ylabel('Y-Dim Tile Size (Ty)')
    ax[1][1].set_xlabel('X-Dim Tile Size (Tx)')
    ax[1][1].set_aspect(5/7)

    im, cbar = heatmap(plotinfo[2][1], y_label, x_label, ax=ax[2][1], cmap="viridis_r", cbarlabel='Latency (million cycle)', norm=colors.LogNorm(vmin=18, vmax=1026))
    annotate_heatmap(im, valfmt="{x:.0f}")
    ax[2][1].set_title('Fully-cached, Latency')
    ax[2][1].set_ylabel('Y-Dim Tile Size (Ty)')
    ax[2][1].set_xlabel('X-Dim Tile Size (Tx)')
    ax[2][1].set_aspect(5/7)

    fig.suptitle('Fig12 Overall Energy and Latency Comparison', fontsize=14)
    fig.tight_layout()
    plt.savefig('./result_plot/Fig12.pdf')
    plt.show()


def plot_Fig13_MAC_Op_count(data):
    modes = ['True_True', 'True_False', 'False_False']
    tile_sizes = ['1_1', '4_4', '16_18', '60_72', '240_270', '960_540']
    MAC_collect_all = {'fully recompute': {}, 'H-cache V-recompute': {}, 'fully cache': {}}
    for mode in modes:
        MAC_collect = data.MAC_collect
        for tile_size in tile_sizes:
            if mode == 'True_True':
                MAC_collect_all['fully cache'][f'{tile_size}'] = MAC_collect[f'{tile_size}_{mode}']
            elif mode == 'True_False':
                MAC_collect_all['H-cache V-recompute'][f'{tile_size}'] = MAC_collect[f'{tile_size}_{mode}']
            elif mode == 'False_False':
                MAC_collect_all['fully recompute'][f'{tile_size}'] = MAC_collect[f'{tile_size}_{mode}']

    xticks_list = [f'({tile.split("_")[0]},{tile.split("_")[1]})' for tile in tile_sizes]
    fig, ax = plt.subplots(figsize=(6, 3))
    color_list = ['#f10c45', '#f5bf03', '#0d75f8', '#cb00f5']
    width = 0.2
    fs=12
    x1 = list(range(len(MAC_collect_all['fully recompute'])))
    y2 = [MAC_collect_all['fully recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y3 = [MAC_collect_all['H-cache V-recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y4 = [MAC_collect_all['fully cache'][f'{tile_size}'] for tile_size in tile_sizes]
    ax.bar(np.array(x1) - 1 * width, y2, width=width, color=color_list[1], label='Fully-recom.')
    ax.bar(np.array(x1)            , y3, width=width, color=color_list[2], label='H-cac. V-recom.')
    ax.bar(np.array(x1) + 1 * width, y4, width=width, color=color_list[3], label='Fully-cac.')
    ax.set_yscale('log')
    ax.set_ylabel('# MAC Op', fontsize=fs)
    plt.xticks(list(range(len(xticks_list))), xticks_list, rotation=0)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, which='major', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle='-')
    ax.yaxis.grid(True, which='minor', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle=':')
    ax.legend(loc='upper right', ncol=1, fontsize=fs-0.5, handlelength=0.8, handleheight=0.8)
    ax.set_ylim(5e9, 3e11)
    ax.set_xlabel('Tile Size (Tx,Ty)', fontsize=fs)
    for item in (ax.get_yticklabels()):
        item.set_fontsize(fs - 1)
    for item in (ax.get_xticklabels()):
        item.set_fontsize(fs - 1)
    fig.suptitle('Fig13 MAC Operation Count', fontsize=14)
    fig.tight_layout()
    plt.savefig('./result_plot/Fig13.pdf')
    plt.show(block=False)


def plot_Fig14_a_mem_access_breakdown(data):
    modes = ['True_True', 'True_False', 'False_False']
    tile_sizes = ['1_1', '4_4', '16_18', '60_72', '240_270', '960_540']
    dram_collect_all = {'fully recompute': {}, 'H-cache V-recompute': {}, 'fully cache': {}}
    gb_collect_all = {'fully recompute': {}, 'H-cache V-recompute': {}, 'fully cache': {}}
    lb_collect_all = {'fully recompute': {}, 'H-cache V-recompute': {}, 'fully cache': {}}
    for mode in modes:
        dram_collect = data.dram_access_collect_normal_layer_A
        gb_collect = data.gb_access_collect_normal_layer_A
        lb_collect = data.lb_access_collect_normal_layer_A
        for tile_size in tile_sizes:
            if mode == 'True_True':
                dram_collect_all['fully cache'][f'{tile_size}'] = dram_collect[f'{tile_size}_{mode}']
                gb_collect_all['fully cache'][f'{tile_size}'] = gb_collect[f'{tile_size}_{mode}']
                lb_collect_all['fully cache'][f'{tile_size}'] = lb_collect[f'{tile_size}_{mode}']
            elif mode == 'True_False':
                dram_collect_all['H-cache V-recompute'][f'{tile_size}'] = dram_collect[f'{tile_size}_{mode}']
                gb_collect_all['H-cache V-recompute'][f'{tile_size}'] = gb_collect[f'{tile_size}_{mode}']
                lb_collect_all['H-cache V-recompute'][f'{tile_size}'] = lb_collect[f'{tile_size}_{mode}']
            elif mode == 'False_False':
                dram_collect_all['fully recompute'][f'{tile_size}'] = dram_collect[f'{tile_size}_{mode}']
                gb_collect_all['fully recompute'][f'{tile_size}'] = gb_collect[f'{tile_size}_{mode}']
                lb_collect_all['fully recompute'][f'{tile_size}'] = lb_collect[f'{tile_size}_{mode}']

    xticks_list = [f'({tile.split("_")[0]},{tile.split("_")[1]})' for tile in tile_sizes]
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True, figsize=(4, 5))
    color_list = ['#f10c45', '#f5bf03', '#0d75f8', '#cb00f5']
    width = 0.2
    fs=12
    x1 = list(range(len(dram_collect_all['fully recompute'])))
    y2 = [dram_collect_all['fully recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y3 = [dram_collect_all['H-cache V-recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y4 = [dram_collect_all['fully cache'][f'{tile_size}'] for tile_size in tile_sizes]
    ax1.bar(np.array(x1) - 1 * width, y2, width=width, color=color_list[1], label='Fully-recom.')
    ax1.bar(np.array(x1)            , y3, width=width, color=color_list[2], label='H-cac. V-recom.')
    ax1.bar(np.array(x1) + 1 * width, y4, width=width, color=color_list[3], label='Fully-cac.')
    ax1.set_yscale('log')
    ax1.set_ylabel('DRAM Access\n(Elem.)', fontsize=fs)

    y2 = [gb_collect_all['fully recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y3 = [gb_collect_all['H-cache V-recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y4 = [gb_collect_all['fully cache'][f'{tile_size}'] for tile_size in tile_sizes]
    ax2.bar(np.array(x1) - 1 * width, y2, width=width, color=color_list[1], label='fully recompute')
    ax2.bar(np.array(x1)            , y3, width=width, color=color_list[2], label='H-cache V-recompute')
    ax2.bar(np.array(x1) + 1 * width, y4, width=width, color=color_list[3], label='fully cache')
    ax2.set_yscale('log')
    ax2.set_ylabel('GB Access\n(Elem.)', fontsize=fs)

    y2 = [lb_collect_all['fully recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y3 = [lb_collect_all['H-cache V-recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y4 = [lb_collect_all['fully cache'][f'{tile_size}'] for tile_size in tile_sizes]
    ax3.bar(np.array(x1) - 1 * width, y2, width=width, color=color_list[1], label='fully recompute')
    ax3.bar(np.array(x1)            , y3, width=width, color=color_list[2], label='H-cache V-recompute')
    ax3.bar(np.array(x1) + 1 * width, y4, width=width, color=color_list[3], label='fully cache')
    ax3.set_yscale('log')
    ax3.set_ylabel('LB Access\n(Elem.)', fontsize=fs)

    ax3.set_xlabel('Tile Size (Tx,Ty)', fontsize=fs)
    plt.xticks(list(range(len(xticks_list))), xticks_list, rotation=20)
    ax1.set_axisbelow(True)
    ax1.yaxis.grid(True, which='major', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle='-')
    ax1.yaxis.grid(True, which='minor', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle=':')
    ax2.set_axisbelow(True)
    ax2.yaxis.grid(True, which='major', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle='-')
    ax2.yaxis.grid(True, which='minor', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle=':')
    ax3.set_axisbelow(True)
    ax3.yaxis.grid(True, which='major', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle='-')
    ax3.yaxis.grid(True, which='minor', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle=':')
    ax1.legend(loc='upper left', ncol=1, fontsize=fs-0.5, handlelength=0.8, handleheight=0.8)
    for ax in [ax1, ax2, ax3]:
        for item in (ax.get_yticklabels()):
            item.set_fontsize(fs - 1)
        for item in (ax.get_xticklabels()):
            item.set_fontsize(fs - 1)
    fig.suptitle('Fig14(a) Activation Mem Access', fontsize=14)
    fig.tight_layout()
    plt.savefig('./result_plot/Fig14_a.pdf')
    plt.show(block=False)


def plot_Fig14_b_mem_access_breakdown(data):
    modes = ['True_True', 'True_False', 'False_False']
    tile_sizes = ['1_1', '4_4', '16_18', '60_72', '240_270', '960_540']
    dram_collect_all = {'fully recompute': {}, 'H-cache V-recompute': {}, 'fully cache': {}}
    gb_collect_all = {'fully recompute': {}, 'H-cache V-recompute': {}, 'fully cache': {}}
    lb_collect_all = {'fully recompute': {}, 'H-cache V-recompute': {}, 'fully cache': {}}
    for mode in modes:
        dram_collect = data.dram_access_collect_normal_layer_W
        gb_collect = data.gb_access_collect_normal_layer_W
        lb_collect = data.lb_access_collect_normal_layer_W
        for tile_size in tile_sizes:
            if mode == 'True_True':
                dram_collect_all['fully cache'][f'{tile_size}'] = dram_collect[f'{tile_size}_{mode}']
                gb_collect_all['fully cache'][f'{tile_size}'] = gb_collect[f'{tile_size}_{mode}']
                lb_collect_all['fully cache'][f'{tile_size}'] = lb_collect[f'{tile_size}_{mode}']
            elif mode == 'True_False':
                dram_collect_all['H-cache V-recompute'][f'{tile_size}'] = dram_collect[f'{tile_size}_{mode}']
                gb_collect_all['H-cache V-recompute'][f'{tile_size}'] = gb_collect[f'{tile_size}_{mode}']
                lb_collect_all['H-cache V-recompute'][f'{tile_size}'] = lb_collect[f'{tile_size}_{mode}']
            elif mode == 'False_False':
                dram_collect_all['fully recompute'][f'{tile_size}'] = dram_collect[f'{tile_size}_{mode}']
                gb_collect_all['fully recompute'][f'{tile_size}'] = gb_collect[f'{tile_size}_{mode}']
                lb_collect_all['fully recompute'][f'{tile_size}'] = lb_collect[f'{tile_size}_{mode}']

    xticks_list = [f'({tile.split("_")[0]},{tile.split("_")[1]})' for tile in tile_sizes]
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True, figsize=(4, 5))
    color_list = ['#f10c45', '#f5bf03', '#0d75f8', '#cb00f5']
    width = 0.2
    fs=12
    x1 = list(range(len(dram_collect_all['fully recompute'])))
    y2 = [dram_collect_all['fully recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y3 = [dram_collect_all['H-cache V-recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y4 = [dram_collect_all['fully cache'][f'{tile_size}'] for tile_size in tile_sizes]
    ax1.bar(np.array(x1) - 1 * width, y2, width=width, color=color_list[1], label='Fully-recom.')
    ax1.bar(np.array(x1)            , y3, width=width, color=color_list[2], label='H-cac. V-recom.')
    ax1.bar(np.array(x1) + 1 * width, y4, width=width, color=color_list[3], label='Fully-cac.')
    ax1.set_yscale('log')
    ax1.set_ylabel('DRAM Access\n(Elem.)', fontsize=fs)

    y2 = [gb_collect_all['fully recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y3 = [gb_collect_all['H-cache V-recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y4 = [gb_collect_all['fully cache'][f'{tile_size}'] for tile_size in tile_sizes]
    ax2.bar(np.array(x1) - 1 * width, y2, width=width, color=color_list[1], label='fully recompute')
    ax2.bar(np.array(x1)            , y3, width=width, color=color_list[2], label='H-cache V-recompute')
    ax2.bar(np.array(x1) + 1 * width, y4, width=width, color=color_list[3], label='fully cache')
    ax2.set_yscale('log')
    ax2.set_ylabel('GB Access\n(Elem.)', fontsize=fs)

    y2 = [lb_collect_all['fully recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y3 = [lb_collect_all['H-cache V-recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y4 = [lb_collect_all['fully cache'][f'{tile_size}'] for tile_size in tile_sizes]
    ax3.bar(np.array(x1) - 1 * width, y2, width=width, color=color_list[1], label='fully recompute')
    ax3.bar(np.array(x1)            , y3, width=width, color=color_list[2], label='H-cache V-recompute')
    ax3.bar(np.array(x1) + 1 * width, y4, width=width, color=color_list[3], label='fully cache')
    ax3.set_yscale('log')
    ax3.set_ylabel('LB Access\n(Elem.)', fontsize=fs)

    ax3.set_xlabel('Tile Size (Tx,Ty)', fontsize=fs)
    plt.xticks(list(range(len(xticks_list))), xticks_list, rotation=20)
    ax1.set_axisbelow(True)
    ax1.yaxis.grid(True, which='major', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle='-')
    ax1.yaxis.grid(True, which='minor', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle=':')
    ax2.set_axisbelow(True)
    ax2.yaxis.grid(True, which='major', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle='-')
    ax2.yaxis.grid(True, which='minor', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle=':')
    ax3.set_axisbelow(True)
    ax3.yaxis.grid(True, which='major', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle='-')
    ax3.yaxis.grid(True, which='minor', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle=':')
    # ax1.legend(loc='upper left', ncol=1, fontsize=fs-0.5, handlelength=0.8, handleheight=0.8)
    for ax in [ax1, ax2, ax3]:
        for item in (ax.get_yticklabels()):
            item.set_fontsize(fs - 1)
        for item in (ax.get_xticklabels()):
            item.set_fontsize(fs - 1)
    fig.suptitle('Fig14(b) Weight Mem Access', fontsize=14)
    fig.tight_layout()
    plt.savefig('./result_plot/Fig14_b.pdf')
    plt.show(block=False)


def plot_Fig14_c_mem_access_breakdown(data):
    modes = ['True_True', 'True_False', 'False_False']
    tile_sizes = ['1_1', '4_4', '16_18', '60_72', '240_270', '960_540']
    dram_collect_all = {'fully recompute': {}, 'H-cache V-recompute': {}, 'fully cache': {}}
    gb_collect_all = {'fully recompute': {}, 'H-cache V-recompute': {}, 'fully cache': {}}
    lb_collect_all = {'fully recompute': {}, 'H-cache V-recompute': {}, 'fully cache': {}}
    for mode in modes:
        dram_collect = data.dram_access_collect_copy_layer
        gb_collect = data.gb_access_collect_copy_layer
        lb_collect = data.lb_access_collect_copy_layer
        for tile_size in tile_sizes:
            if mode == 'True_True':
                dram_collect_all['fully cache'][f'{tile_size}'] = dram_collect[f'{tile_size}_{mode}']
                gb_collect_all['fully cache'][f'{tile_size}'] = gb_collect[f'{tile_size}_{mode}']
                lb_collect_all['fully cache'][f'{tile_size}'] = lb_collect[f'{tile_size}_{mode}']
            elif mode == 'True_False':
                dram_collect_all['H-cache V-recompute'][f'{tile_size}'] = dram_collect[f'{tile_size}_{mode}']
                gb_collect_all['H-cache V-recompute'][f'{tile_size}'] = gb_collect[f'{tile_size}_{mode}']
                lb_collect_all['H-cache V-recompute'][f'{tile_size}'] = lb_collect[f'{tile_size}_{mode}']
            elif mode == 'False_False':
                dram_collect_all['fully recompute'][f'{tile_size}'] = dram_collect[f'{tile_size}_{mode}']
                gb_collect_all['fully recompute'][f'{tile_size}'] = gb_collect[f'{tile_size}_{mode}']
                lb_collect_all['fully recompute'][f'{tile_size}'] = lb_collect[f'{tile_size}_{mode}']

    xticks_list = [f'({tile.split("_")[0]},{tile.split("_")[1]})' for tile in tile_sizes]
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True, figsize=(4, 5))
    color_list = ['#f10c45', '#f5bf03', '#0d75f8', '#cb00f5']
    width = 0.2
    fs=12
    x1 = list(range(len(dram_collect_all['fully recompute'])))
    y2 = [dram_collect_all['fully recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y3 = [dram_collect_all['H-cache V-recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y4 = [dram_collect_all['fully cache'][f'{tile_size}'] for tile_size in tile_sizes]
    ax1.bar(np.array(x1) - 1 * width, y2, width=width, color=color_list[1], label='Fully-recom.')
    ax1.bar(np.array(x1)            , y3, width=width, color=color_list[2], label='H-cac. V-recom.')
    ax1.bar(np.array(x1) + 1 * width, y4, width=width, color=color_list[3], label='Fully-cac.')
    ax1.set_yscale('log')
    ax1.set_ylabel('DRAM Access\n(Elem.)', fontsize=fs)

    y2 = [gb_collect_all['fully recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y3 = [gb_collect_all['H-cache V-recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y4 = [gb_collect_all['fully cache'][f'{tile_size}'] for tile_size in tile_sizes]
    ax2.bar(np.array(x1) - 1 * width, y2, width=width, color=color_list[1], label='fully recompute')
    ax2.bar(np.array(x1)            , y3, width=width, color=color_list[2], label='H-cache V-recompute')
    ax2.bar(np.array(x1) + 1 * width, y4, width=width, color=color_list[3], label='fully cache')
    ax2.set_yscale('log')
    ax2.set_ylabel('GB Access\n(Elem.)', fontsize=fs)

    y2 = [lb_collect_all['fully recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y3 = [lb_collect_all['H-cache V-recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y4 = [lb_collect_all['fully cache'][f'{tile_size}'] for tile_size in tile_sizes]
    ax3.bar(np.array(x1) - 1 * width, y2, width=width, color=color_list[1], label='fully recompute')
    ax3.bar(np.array(x1)            , y3, width=width, color=color_list[2], label='H-cache V-recompute')
    ax3.bar(np.array(x1) + 1 * width, y4, width=width, color=color_list[3], label='fully cache')
    ax3.set_yscale('log')
    ax3.set_ylabel('LB Access\n(Elem.)', fontsize=fs)

    ax3.set_xlabel('Tile Size (Tx,Ty)', fontsize=fs)
    plt.xticks(list(range(len(xticks_list))), xticks_list, rotation=20)
    ax1.set_axisbelow(True)
    ax1.yaxis.grid(True, which='major', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle='-')
    ax1.yaxis.grid(True, which='minor', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle=':')
    ax2.set_axisbelow(True)
    ax2.yaxis.grid(True, which='major', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle='-')
    ax2.yaxis.grid(True, which='minor', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle=':')
    ax3.set_axisbelow(True)
    ax3.yaxis.grid(True, which='major', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle='-')
    ax3.yaxis.grid(True, which='minor', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle=':')
    # ax1.legend(loc='upper left', ncol=1, fontsize=fs-0.5, handlelength=0.8, handleheight=0.8)
    for ax in [ax1, ax2, ax3]:
        for item in (ax.get_yticklabels()):
            item.set_fontsize(fs - 1)
        for item in (ax.get_xticklabels()):
            item.set_fontsize(fs - 1)
    fig.suptitle('Fig14(c) Data Copy Layer Mem Access', fontsize=14)
    fig.tight_layout()
    plt.savefig('./result_plot/Fig14_c.pdf')
    plt.show(block=False)


def plot_Fig14_d_mem_access_breakdown(data):
    modes = ['True_True', 'True_False', 'False_False']
    tile_sizes = ['1_1', '4_4', '16_18', '60_72', '240_270', '960_540']
    dram_collect_all = {'fully recompute': {}, 'H-cache V-recompute': {}, 'fully cache': {}}
    gb_collect_all = {'fully recompute': {}, 'H-cache V-recompute': {}, 'fully cache': {}}
    lb_collect_all = {'fully recompute': {}, 'H-cache V-recompute': {}, 'fully cache': {}}
    for mode in modes:
        dram_collect = data.dram_access_collect
        gb_collect = data.gb_access_collect
        lb_collect = data.lb_access_collect
        for tile_size in tile_sizes:
            if mode == 'True_True':
                dram_collect_all['fully cache'][f'{tile_size}'] = dram_collect[f'{tile_size}_{mode}']
                gb_collect_all['fully cache'][f'{tile_size}'] = gb_collect[f'{tile_size}_{mode}']
                lb_collect_all['fully cache'][f'{tile_size}'] = lb_collect[f'{tile_size}_{mode}']
            elif mode == 'True_False':
                dram_collect_all['H-cache V-recompute'][f'{tile_size}'] = dram_collect[f'{tile_size}_{mode}']
                gb_collect_all['H-cache V-recompute'][f'{tile_size}'] = gb_collect[f'{tile_size}_{mode}']
                lb_collect_all['H-cache V-recompute'][f'{tile_size}'] = lb_collect[f'{tile_size}_{mode}']
            elif mode == 'False_False':
                dram_collect_all['fully recompute'][f'{tile_size}'] = dram_collect[f'{tile_size}_{mode}']
                gb_collect_all['fully recompute'][f'{tile_size}'] = gb_collect[f'{tile_size}_{mode}']
                lb_collect_all['fully recompute'][f'{tile_size}'] = lb_collect[f'{tile_size}_{mode}']

    xticks_list = [f'({tile.split("_")[0]},{tile.split("_")[1]})' for tile in tile_sizes]
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True, figsize=(4, 5))
    color_list = ['#f10c45', '#f5bf03', '#0d75f8', '#cb00f5']
    width = 0.2
    fs=12
    x1 = list(range(len(dram_collect_all['fully recompute'])))
    y2 = [dram_collect_all['fully recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y3 = [dram_collect_all['H-cache V-recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y4 = [dram_collect_all['fully cache'][f'{tile_size}'] for tile_size in tile_sizes]
    ax1.bar(np.array(x1) - 1 * width, y2, width=width, color=color_list[1], label='Fully-recom.')
    ax1.bar(np.array(x1)            , y3, width=width, color=color_list[2], label='H-cac. V-recom.')
    ax1.bar(np.array(x1) + 1 * width, y4, width=width, color=color_list[3], label='Fully-cac.')
    ax1.set_yscale('log')
    ax1.set_ylabel('DRAM Access\n(Elem.)', fontsize=fs)

    y2 = [gb_collect_all['fully recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y3 = [gb_collect_all['H-cache V-recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y4 = [gb_collect_all['fully cache'][f'{tile_size}'] for tile_size in tile_sizes]
    ax2.bar(np.array(x1) - 1 * width, y2, width=width, color=color_list[1], label='fully recompute')
    ax2.bar(np.array(x1)            , y3, width=width, color=color_list[2], label='H-cache V-recompute')
    ax2.bar(np.array(x1) + 1 * width, y4, width=width, color=color_list[3], label='fully cache')
    ax2.set_yscale('log')
    ax2.set_ylabel('GB Access\n(Elem.)', fontsize=fs)

    y2 = [lb_collect_all['fully recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y3 = [lb_collect_all['H-cache V-recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y4 = [lb_collect_all['fully cache'][f'{tile_size}'] for tile_size in tile_sizes]
    ax3.bar(np.array(x1) - 1 * width, y2, width=width, color=color_list[1], label='fully recompute')
    ax3.bar(np.array(x1)            , y3, width=width, color=color_list[2], label='H-cache V-recompute')
    ax3.bar(np.array(x1) + 1 * width, y4, width=width, color=color_list[3], label='fully cache')
    ax3.set_yscale('log')
    ax3.set_ylabel('LB Access\n(Elem.)', fontsize=fs)

    ax3.set_xlabel('Tile Size (Tx,Ty)', fontsize=fs)
    plt.xticks(list(range(len(xticks_list))), xticks_list, rotation=20)
    ax1.set_axisbelow(True)
    ax1.yaxis.grid(True, which='major', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle='-')
    ax1.yaxis.grid(True, which='minor', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle=':')
    ax2.set_axisbelow(True)
    ax2.yaxis.grid(True, which='major', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle='-')
    ax2.yaxis.grid(True, which='minor', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle=':')
    ax3.set_axisbelow(True)
    ax3.yaxis.grid(True, which='major', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle='-')
    ax3.yaxis.grid(True, which='minor', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle=':')
    # ax1.legend(loc='upper left', ncol=1, fontsize=fs-0.5, handlelength=0.8, handleheight=0.8)
    for ax in [ax1, ax2, ax3]:
        for item in (ax.get_yticklabels()):
            item.set_fontsize(fs - 1)
        for item in (ax.get_xticklabels()):
            item.set_fontsize(fs - 1)
    fig.suptitle('Fig14(d) Total Mem Access', fontsize=14)
    fig.tight_layout()
    plt.savefig('./result_plot/Fig14_d.pdf')
    plt.show(block=False)


def plot_Fig15_total_en_and_la_barchart(data):
    modes = ['True_True', 'True_False', 'False_False']
    tile_sizes = ['1_1', '4_4', '16_18', '60_72', '240_270', '960_540']
    en_collect_all = {'fully recompute': {}, 'H-cache V-recompute': {}, 'fully cache': {}}
    la_collect_all = {'fully recompute': {}, 'H-cache V-recompute': {}, 'fully cache': {}}
    for mode in modes:
        en_collect = data.en_collect
        la_collect = data.la_collect
        for tile_size in tile_sizes:
            if mode == 'True_True':
                en_collect_all['fully cache'][f'{tile_size}'] = en_collect[f'{tile_size}_{mode}']
                la_collect_all['fully cache'][f'{tile_size}'] = la_collect[f'{tile_size}_{mode}']
            elif mode == 'True_False':
                en_collect_all['H-cache V-recompute'][f'{tile_size}'] = en_collect[f'{tile_size}_{mode}']
                la_collect_all['H-cache V-recompute'][f'{tile_size}'] = la_collect[f'{tile_size}_{mode}']
            elif mode == 'False_False':
                en_collect_all['fully recompute'][f'{tile_size}'] = en_collect[f'{tile_size}_{mode}']
                la_collect_all['fully recompute'][f'{tile_size}'] = la_collect[f'{tile_size}_{mode}']

    xticks_list = [f'({tile.split("_")[0]},{tile.split("_")[1]})' for tile in tile_sizes]
    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True, figsize=(6, 4.5))
    color_list = ['#f10c45', '#f5bf03', '#0d75f8', '#cb00f5']
    width = 0.2
    fs=12
    x1 = list(range(len(en_collect_all['fully recompute'])))
    y2 = [en_collect_all['fully recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y3 = [en_collect_all['H-cache V-recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y4 = [en_collect_all['fully cache'][f'{tile_size}'] for tile_size in tile_sizes]
    ax1.plot(np.array(x1), y2, marker='o', markersize=4, color=color_list[1], label='Fully-recom.')
    ax1.plot(np.array(x1), y3, marker='o', markersize=4, color=color_list[2], label='H-cac. V-recom.')
    ax1.plot(np.array(x1), y4, marker='o', markersize=4, color=color_list[3], label='Fully-cac.')
    ax1.set_yscale('log')
    ax1.set_ylabel('Energy (mJ)', fontsize=fs)

    y2 = [la_collect_all['fully recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y3 = [la_collect_all['H-cache V-recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y4 = [la_collect_all['fully cache'][f'{tile_size}'] for tile_size in tile_sizes]
    ax2.plot(np.array(x1), y2, marker='o', markersize=4, color=color_list[1], label='Fully-recom.')
    ax2.plot(np.array(x1), y3, marker='o', markersize=4, color=color_list[2], label='H-cac. V-recom.')
    ax2.plot(np.array(x1), y4, marker='o', markersize=4, color=color_list[3], label='Fully-cac.')
    ax2.set_yscale('log')
    ax2.set_ylabel('Latency\n(million cycles)', fontsize=fs)

    ax2.set_xlabel('Tile Size (Tx,Ty)', fontsize=fs)
    plt.xticks(list(range(len(xticks_list))), xticks_list, rotation=0)
    ax1.set_axisbelow(True)
    ax1.yaxis.grid(True, which='major', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle='-')
    ax1.yaxis.grid(True, which='minor', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle=':')
    ax2.set_axisbelow(True)
    ax2.yaxis.grid(True, which='major', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle='-')
    ax2.yaxis.grid(True, which='minor', color=(0.2, 0.2, 0.2), linewidth=0.25, linestyle=':')
    ax2.legend(loc='upper right', ncol=1, fontsize=fs-0.5)
    for ax in [ax1, ax2]:
        for item in (ax.get_yticklabels()):
            item.set_fontsize(fs - 1)
        for item in (ax.get_xticklabels()):
            item.set_fontsize(fs - 1)
    fig.suptitle('Fig15 Total Energy and Latency \n of selected design points', fontsize=14)
    fig.tight_layout()
    plt.savefig('./result_plot/Fig15.pdf')
    plt.show(block=False)


def plot_Fig6_tile_type_count(data):
    modes = ['True_True', 'True_False', 'False_False']
    tile_sizes = ['1_1', '16_18', '60_72', '240_270']
    tile_type_collect_all = {'fully recompute': {}, 'H-cache V-recompute': {}, 'fully cache': {}}
    for mode in modes:
        tile_type_collect = data.tile_type_collect
        for tile_size in tile_sizes:
            if mode == 'True_True':
                tile_type_collect_all['fully cache'][f'{tile_size}'] = tile_type_collect[f'{tile_size}_{mode}']
            elif mode == 'True_False':
                tile_type_collect_all['H-cache V-recompute'][f'{tile_size}'] = tile_type_collect[f'{tile_size}_{mode}']
            elif mode == 'False_False':
                tile_type_collect_all['fully recompute'][f'{tile_size}'] = tile_type_collect[f'{tile_size}_{mode}']

    xticks_list = [f'({tile.split("_")[0]},{tile.split("_")[1]})' for tile in tile_sizes]
    fig, ax1 = plt.subplots(figsize=(7, 6))
    color_list = ['#f10c45', '#f5bf03', '#0d75f8', '#cb00f5']
    width = 0.25
    fs = 14
    x1 = list(range(len(tile_type_collect_all['fully recompute'])))
    y2 = [tile_type_collect_all['fully recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y3 = [tile_type_collect_all['H-cache V-recompute'][f'{tile_size}'] for tile_size in tile_sizes]
    y4 = [tile_type_collect_all['fully cache'][f'{tile_size}'] for tile_size in tile_sizes]
    ax1.bar(np.array(x1) - 1 * width, y2, width=width, color=color_list[1], label='Fully-recompute')
    ax1.bar(np.array(x1)            , y3, width=width, color=color_list[2], label='H-cache V-recompute')
    ax1.bar(np.array(x1) + 1 * width, y4, width=width, color=color_list[3], label='Fully-cached')

    ax1.set_ylabel('Tile type count', fontsize=fs)
    ax1.set_xlabel('Tile Size (Tx,Ty)', fontsize=fs)
    plt.xticks(list(range(len(xticks_list))), xticks_list, rotation=15)
    ax1.yaxis.grid(True, which='major', color='black', linewidth=0.5)
    ax1.yaxis.grid(True, which='minor', color='gray', linewidth=0.1, linestyle='--')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, ncol=1)
    for ax in [ax1]:
        for item in (ax.get_yticklabels()):
            item.set_fontsize(fs - 1)
        for item in (ax.get_xticklabels()):
            item.set_fontsize(fs - 1)
    fig.suptitle('Fig6 Tile Type Count', fontsize=14)
    fig.tight_layout()
    plt.savefig('./result_plot/Fig6.pdf')
    plt.show(block=False)


def plot_Fig9_top_mem_level_visualization(result_saving_path, design_to_visualize):
    from classes.depthfirst.data_copy_layer import DataCopyLayer
    import pickle

    with open(f'{result_saving_path}/{design_to_visualize}.pkl', 'rb') as f:
        loaded_data = pickle.load(f)

    mem_lv_all_tile_all_layer = []

    i = 0
    # get I and O memory level
    for cme, extra_info in loaded_data:
        if isinstance(cme, DataCopyLayer):
            continue
        extra_info = extra_info[1]
        repetitive_time = [t for (_, t) in extra_info]
        mem_lv_all_tile_per_layer = [extra_info[idx][0][0].active_mem_level for idx in range(len(extra_info))]
        for idx, a in enumerate(mem_lv_all_tile_per_layer):
            for op, mem_lv in a.items():
                if op == 'I':
                    mem_lv_all_tile_per_layer[idx]['I'] += 1
                    if i == 0:
                        mem_lv_all_tile_per_layer[idx]['I'] = 4
        i += 1
        mem_lv_all_tile_all_layer.append(mem_lv_all_tile_per_layer)

    # get CI and CO memory level (not used for plotting)
    # for cme, extra_info in loaded_data:
    #     if not isinstance(cme, DataCopyLayer):
    #         continue
    #     extra_info = extra_info[1]
    #     layer_idx = int(extra_info[0][0][1][0].split('_')[-1])
    #     if layer_idx == -1:
    #         layer_idx = 0
    #     for tile_idx, copy_layer_detail in enumerate(extra_info):
    #         print()
    #         print(f'{tile_idx=}')
    #         for copy_action in copy_layer_detail[0][0].data_copy_actions:
    #             print(f'{copy_action}=')
    #             cached_op = copy_action.source_op
    #             if cached_op[0] == 'I':
    #                 cached_op = 'CI'
    #                 cached_lv = copy_action.source_lv + 2
    #             else:
    #                 cached_op = 'CO'
    #                 cached_lv = copy_action.dest_lv + 1
    #
    #             mem_lv_all_tile_all_layer[layer_idx][tile_idx][cached_op] = cached_lv
    #         op_check = list(mem_lv_all_tile_all_layer[layer_idx][tile_idx].keys())
    #         if 'CI' not in op_check:
    #             mem_lv_all_tile_all_layer[layer_idx][tile_idx]['CI'] = mem_lv_all_tile_all_layer[layer_idx][tile_idx]['I']
    #         if 'CO' not in op_check:
    #             mem_lv_all_tile_all_layer[layer_idx][tile_idx]['CO'] = mem_lv_all_tile_all_layer[layer_idx][tile_idx]['O']


    nb_layer = len(mem_lv_all_tile_all_layer)
    nb_tile = len(mem_lv_all_tile_all_layer[0])
    # lines = {op: [[] for _ in range(nb_tile)] for op in ['W', 'I', 'O', 'CI', 'CO']}
    lines = {op: [[] for _ in range(nb_tile)] for op in ['W', 'I', 'O']}
    # for operand in ['W', 'I', 'O', 'CI', 'CO']:
    for operand in ['W', 'I', 'O']:
        for layer_idx in range(nb_layer):
            for tile_idx in range(nb_tile):
                lines[operand][tile_idx].append(mem_lv_all_tile_all_layer[layer_idx][tile_idx][operand])

    fig, ax = plt.subplots(constrained_layout=True, figsize=(7.5, 3.3))
    x = [[nb_layer*j+i+1 for i in range(nb_layer)] for j in range(nb_tile)]
    y1 = lines['W']
    y2 = lines['I']
    y3 = lines['O']
    # y4 = lines['CI']
    # y5 = lines['CO']
    for i in range(len(x)-1):
        plt.plot(x[i], y1[i], '-gD', alpha=0.6)
        plt.plot(x[i], y2[i], '-r^', alpha=0.6)
        plt.plot(x[i], y3[i], '-b+', alpha=0.6)
        # plt.plot(x[i], y4[i], '--y.', linewidth=0.5)
        # plt.plot(x[i], y5[i], '--k.', alpha=0.5, linewidth=0.5)

    for i in range(len(x)-1, len(x)):
        plt.plot(x[i], y1[i], '-gD', label='W', alpha=0.6)
        plt.plot(x[i], y2[i], '-r^', label='I', alpha=0.6)
        plt.plot(x[i], y3[i], '-b+', label='O', alpha=0.6)
        # plt.plot(x[i], y4[i], '--y.', label='CI', linewidth=0.5)
        # plt.plot(x[i], y5[i], '--k.', label='CO', alpha=0.5, linewidth=0.5)

    plt.yticks(np.arange(1, 5), ['Reg', 'LB', 'GB', 'DRAM'])
    xlbls = [f'L{layer+1}' for tile_type in range(nb_tile) for layer in range(nb_layer)]
    plt.xticks(np.arange(1, 1+nb_layer*nb_tile), xlbls, rotation=45, fontsize=13.5)
    vline_pos = [nb_layer*j+0.5 for j in range(1+nb_tile)]
    for idx, pos in enumerate(vline_pos):
        plt.axvline(x=pos, color='k', linestyle=':')
        if idx > 0:
            if repetitive_time[idx-1] == 1:
                plt.text((vline_pos[idx]+vline_pos[idx-1])/2, 1.3, f'Tile type {idx}\n({repetitive_time[idx-1]} time)', dict(size=14), ha='center', va='center')
            else:
                plt.text((vline_pos[idx]+vline_pos[idx-1])/2, 1.3, f'Tile type {idx}\n({repetitive_time[idx-1]} times)', dict(size=14), ha='center', va='center')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, ncol=1, handlelength=0.8, handleheight=0.8)
    plt.xlabel("Tile type and Layer (L)", fontsize=14)
    plt.ylabel("Top Mem Level", fontsize=14)

    for item in (ax.get_yticklabels()):
        item.set_fontsize(14)

    plt.title('Fig9 Top Memory Level Visualization', fontsize=14)
    fig.tight_layout()
    plt.savefig('./result_plot/Fig9.pdf')
    plt.show(block=False)


def plot_Fig10_activation_data_size_visualization(result_saving_path, design_to_visualize):
    import pickle
    from copy import deepcopy
    from classes.depthfirst.data_copy_layer import DataCopyLayer

    with open(f'{result_saving_path}/{design_to_visualize}.pkl', 'rb') as f:
        loaded_data = pickle.load(f)

    size_all_tile_all_layer = {'W': [], 'I': [], 'O': []}
    for cme, extra_info in loaded_data:
        extra_info = extra_info[1]
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
                if tile_idx == 0:
                    continue
                bars[operand][tile_idx].append(size_all_tile_all_layer[operand][layer_idx][tile_idx])

    fig, ax = plt.subplots(constrained_layout=True, figsize=(7.5, 3.3))
    x = [[nb_layer*j+i+1 for i in range(nb_layer)] for j in range(nb_tile)]
    x = np.array(x)
    y1 = bars['W']
    y2 = bars['I']
    y3 = bars['O']

    y23 = deepcopy(y2)
    for id1, sub_li in enumerate(y3):
        for id2, elem in enumerate(sub_li):
            y23[id1][id2] += elem

    # for id1, sub_li in enumerate(y2):
    #     for id2, elem in enumerate(sub_li):
    #         y2[id1][id2] /= 1024
    # for id1, sub_li in enumerate(y3):
    #     for id2, elem in enumerate(sub_li):
    #         y2[id1][id2] /= 1024
    # for id1, sub_li in enumerate(y23):
    #     for id2, elem in enumerate(sub_li):
    #         y2[id1][id2] /= 1024
    #
    # y2_largest = max([max(y2_li) for y2_li in y2])
    # y3_largest = max([max(y3_li) for y3_li in y3])
    # y23_largest = max([max(y23_li) for y23_li in y23])
    # largest = max(y2_largest, y3_largest, y23_largest)
    largest = 0.5*1024*1024
    width = 0.2  # the width of the bars
    for i in range(len(x)-1):
        if i == 0:
            continue
        # ax.bar(x[i] - width, y1[i],  width, facecolor='g')

        ax.bar(x[i] - width, y2[i], width, facecolor='r', alpha=0.6)
        ax.bar(x[i]        , y3[i], width, facecolor='b', alpha=0.6)
        ax.bar(x[i] + width, y23[i], width, facecolor='#feb308', alpha=0.7)

    for i in range(len(x)-1, len(x)):
        # ax.bar(x[i] - width, y1[i], width, label='Weight', facecolor='g')
        ax.bar(x[i] - width, y2[i], width, label='I', facecolor='r', alpha=0.6)
        ax.bar(x[i],         y3[i], width, label='O', facecolor='b', alpha=0.6)
        ax.bar(x[i] + width, y23[i], width, label='I+O', facecolor='#feb308', alpha=0.7)

    # plt.yticks(np.arange(1, 5), ['Reg', 'LB', 'GB', 'DRAM'])
    xlbls = [f'L{layer+1}' for tile_type in range(nb_tile-1) for layer in range(nb_layer)]
    # plt.xticks(np.arange(1+nb_layer, 1+nb_layer*nb_tile), xlbls, rotation=45)
    plt.xticks(np.arange(1+nb_layer, 1+nb_layer*nb_tile), xlbls)
    vline_pos = [nb_layer*j+0.5 for j in range(1+nb_tile)]
    for idx, pos in enumerate(vline_pos):
        plt.axvline(x=pos, color='k', linestyle=':')
        if idx == 1:
            continue
        if idx > 0:
            if repetitive_time[idx-1] == 1:
                plt.text((vline_pos[idx]+vline_pos[idx-1])/2, largest*0.95, f'Tile type {idx}\n({repetitive_time[idx-1]} time)', dict(size=14), ha='center', va='center')
            else:
                plt.text((vline_pos[idx]+vline_pos[idx-1])/2, largest*0.95, f'Tile type {idx}\n({repetitive_time[idx-1]} times)', dict(size=14), ha='center', va='center')
    ax.set_yscale('log', base=2)
    # ax.set_ylim([2*1024, 64*1024*1024])
    ax.set_xlim([8, 25])
    # plt.yticks([4*1024, 16*1024, 64*1024, 256*1024, 1024*1024, 4*1024*1024, 16*1024*1024, 64*1024*1024],
    #            ['4K', '16K', 'LB:64K', '256K', 'GB:1M', '4M', '16M', '64M'])
    plt.yticks([4*1024, 16*1024, 64*1024, 256*1024, 1024*1024],
               ['4K', '16K', 'LB:64K', '256K', 'GB:1M'])
    for item in (ax.get_yticklabels()):
        item.set_fontsize(13)
    for item in (ax.get_xticklabels()):
        item.set_fontsize(13)
    plt.axhline(y=64*1024, color='k', linestyle='-', linewidth=0.5)
    plt.axhline(y=1024*1024, color='k', linestyle='-', linewidth=0.5)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, ncol=1, handlelength=0.8, handleheight=0.8)
    plt.xlabel("Tile type and Layer (L)", fontsize=14)
    plt.ylabel("Data size (Byte)", fontsize=14)

    plt.title('Fig10 Activation Data Size Visualization', fontsize=14)
    fig.tight_layout()
    plt.savefig('./result_plot/Fig10.pdf')
    plt.show(block=True)


if __name__ == '__main__':
    from main_cs1 import result_saving_path
    data_to_plot = data_collect(result_saving_path)
    plot_Fig13_MAC_Op_count(data_to_plot)
    plot_Fig14_a_mem_access_breakdown(data_to_plot)
    plot_Fig14_b_mem_access_breakdown(data_to_plot)
    plot_Fig14_c_mem_access_breakdown(data_to_plot)
    plot_Fig14_d_mem_access_breakdown(data_to_plot)
    plot_Fig15_total_en_and_la_barchart(data_to_plot)
    plot_Fig6_tile_type_count(data_to_plot)
    design_to_visualize = '60_72_False_False'
    plot_Fig9_top_mem_level_visualization(result_saving_path, design_to_visualize)
    plot_Fig10_activation_data_size_visualization(result_saving_path, design_to_visualize)