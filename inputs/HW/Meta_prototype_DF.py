import os
from classes.hardware.architecture.memory_hierarchy import MemoryHierarchy
from classes.hardware.architecture.memory_level import MemoryLevel
from classes.hardware.architecture.operational_unit import Multiplier
from classes.hardware.architecture.operational_array import MultiplierArray
from classes.hardware.architecture.memory_instance import MemoryInstance
from classes.hardware.architecture.accelerator import Accelerator
from classes.hardware.architecture.core import Core


def memory_hierarchy_dut(multiplier_array):
    """Memory hierarchy variables"""
    ''' size=#bit, bw=(read bw, write bw), cost=(read word energy, write work energy) '''

    reg_IW1 = MemoryInstance(name="rf_1B", size=8, r_bw=8, w_bw=8, r_cost=0.01, w_cost=0.01, area=0, bank=1,
                             random_bank_access=False, r_port=1, w_port=1, rw_port=0, latency=1)

    reg_O1 = MemoryInstance(name="rf_2B", size=16, r_bw=16, w_bw=16, r_cost=0.02, w_cost=0.02, area=0, bank=1,
                            random_bank_access=False, r_port=2, w_port=2, rw_port=0, latency=1)

    reg_IW4 = MemoryInstance(name="rf_4B", size=32, r_bw=8, w_bw=8, r_cost=0.012, w_cost=0.012, area=0, bank=1,
                             random_bank_access=False, r_port=1, w_port=1, rw_port=0, latency=1)

    reg_O4 = MemoryInstance(name="rf_8B", size=64, r_bw=16, w_bw=16, r_cost=0.024, w_cost=0.024, area=0, bank=1,
                            random_bank_access=False, r_port=2, w_port=2, rw_port=0, latency=1)

    reg_IW8 = MemoryInstance(name="rf_16B", size=128, r_bw=8, w_bw=8, r_cost=0.0225, w_cost=0.0225, area=0, bank=1,
                             random_bank_access=False, r_port=1, w_port=1, rw_port=0, latency=1)

    reg_O8 = MemoryInstance(name="rf_32B", size=256, r_bw=16, w_bw=16, r_cost=0.045, w_cost=0.045, area=0, bank=1,
                            random_bank_access=False, r_port=2, w_port=2, rw_port=0, latency=1)

    ##################################### on-chip memory hierarchy building blocks #####################################

    sram_64KB_with_8_8K_64_1r_1w = \
        MemoryInstance(name="sram_64KB", size=8192 * 8 * 8, r_bw=64 * 8, w_bw=64 * 8, r_cost=3.32 * 8, w_cost=3.85 * 8, area=0, bank=1,
                       random_bank_access=True, r_port=1, w_port=1, rw_port=0, latency=1, min_r_granularity=64, min_w_granularity=64)

    sram_32KB_with_4_8K_128_1r_1w = \
        MemoryInstance(name="sram_32KB", size=8192 * 4 * 8, r_bw=128 * 4, w_bw=128 * 4, r_cost=4.3 * 4, w_cost=7.1 * 4, area=0, bank=1,
                       random_bank_access=True, r_port=1, w_port=1, rw_port=0, latency=1, min_r_granularity=64, min_w_granularity=64)

    sram_1M_with_8_128K_bank_128_1r_1w_A = \
        MemoryInstance(name="sram_1MB_A", size=131072 * 8 * 8, r_bw=128 * 8, w_bw=128 * 8, r_cost=26.01 * 8, w_cost=23.65 * 8, area=0, bank=1,
                       random_bank_access=True, r_port=1, w_port=1, rw_port=0, latency=1, min_r_granularity=64, min_w_granularity=64)

    sram_1M_with_8_128K_bank_128_1r_1w_W = \
        MemoryInstance(name="sram_1MB_W", size=131072 * 8 * 8, r_bw=128 * 8, w_bw=128 * 8, r_cost=26.01 * 8, w_cost=23.65 * 8, area=0, bank=1,
                       random_bank_access=True, r_port=1, w_port=1, rw_port=0, latency=1, min_r_granularity=64, min_w_granularity=64)

    #######################################################################################################################

    dram = MemoryInstance(name="dram", size=10000000000, r_bw=64, w_bw=64, r_cost=700, w_cost=750, area=0, bank=1,
                          random_bank_access=False, r_port=0, w_port=0, rw_port=1, latency=1)

    memory_hierarchy_graph = MemoryHierarchy(operational_array=multiplier_array)

    '''
    fh: from high = wr_in_by_high 
    fl: from low = wr_in_by_low 
    th: to high = rd_out_to_high
    tl: to low = rd_out_to_low
    '''
    # we don't have unrolled I-Reg to better support G unrolling
    # memory_hierarchy_graph.add_memory(memory_instance=reg_IW1, operands=('I1',),
    #                                   port_alloc=({'fh': 'w_port_1', 'tl': 'r_port_1', 'fl': None, 'th': None},),
    #                                   served_dimensions={(0, 0, 0, 0)})
    memory_hierarchy_graph.add_memory(memory_instance=reg_IW1, operands=('I2',),
                                      port_alloc=({'fh': 'w_port_1', 'tl': 'r_port_1', 'fl': None, 'th': None},),
                                      served_dimensions={(0, 0, 1, 0), (0, 0, 0, 1)})
    memory_hierarchy_graph.add_memory(memory_instance=reg_O1, operands=('O',),
                                      port_alloc=({'fh': 'w_port_1', 'tl': 'r_port_1', 'fl': 'w_port_2', 'th': 'r_port_2'},),
                                      served_dimensions={(0, 1, 0, 0)})

    ##################################### on-chip highest memory hierarchy initialization #####################################

    memory_hierarchy_graph.add_memory(memory_instance=sram_32KB_with_4_8K_128_1r_1w, operands=('I2',),
                                      port_alloc=({'fh': 'w_port_1', 'tl': 'r_port_1', 'fl': None, 'th': None},),
                                      served_dimensions='all')
    memory_hierarchy_graph.add_memory(memory_instance=sram_1M_with_8_128K_bank_128_1r_1w_W, operands=('I2',),
                                      port_alloc=({'fh': 'w_port_1', 'tl': 'r_port_1', 'fl': None, 'th': None},),
                                      served_dimensions='all')

    memory_hierarchy_graph.add_memory(memory_instance=sram_64KB_with_8_8K_64_1r_1w, operands=('I1', 'O'),
                                      port_alloc=({'fh': 'w_port_1', 'tl': 'r_port_1', 'fl': None, 'th': None},
                                                  {'fh': 'w_port_1', 'tl': 'r_port_1', 'fl': 'w_port_1', 'th': 'r_port_1'},),
                                      served_dimensions='all')
    memory_hierarchy_graph.add_memory(memory_instance=sram_1M_with_8_128K_bank_128_1r_1w_A, operands=('I1', 'O'),
                                      port_alloc=({'fh': 'w_port_1', 'tl': 'r_port_1', 'fl': None, 'th': None},
                                                  {'fh': 'w_port_1', 'tl': 'r_port_1', 'fl': 'w_port_1', 'th': 'r_port_1'},),
                                      served_dimensions='all')

    ####################################################################################################################

    memory_hierarchy_graph.add_memory(memory_instance=dram, operands=('I1', 'I2', 'O'),
                                      port_alloc=({'fh': 'rw_port_1', 'tl': 'rw_port_1', 'fl': None, 'th': None},
                                                  {'fh': 'rw_port_1', 'tl': 'rw_port_1', 'fl': None, 'th': None},
                                                  {'fh': 'rw_port_1', 'tl': 'rw_port_1', 'fl': 'rw_port_1', 'th': 'rw_port_1'},),
                                      served_dimensions='all')

    return memory_hierarchy_graph


def multiplier_array_dut():
    """ Multiplier array variables """
    multiplier_input_precision = [8, 8]
    multiplier_energy = 0.04
    multiplier_area = 1
    dimensions = {'D1': 32, 'D2': 2, 'D3': 4, 'D4': 4}  # {'D1': ('K', 32), 'D2': ('C', 2), 'D3': ('OX', 4), 'D4': ('OY', 4),}
    operand_spatial_sharing = {'I1': {(1, 0, 0, 0)},  # {'O': 'O', 'W': 'I2', 'I': 'I1'}
                               'I2': {(0, 0, 1, 1)},
                               'O': {(0, 1, 0, 0)},
                               }
    multiplier = Multiplier(multiplier_input_precision, multiplier_energy, multiplier_area)
    multiplier_array = MultiplierArray(multiplier, dimensions)

    return multiplier_array


def cores():
    multiplier_array1 = multiplier_array_dut()
    memory_hierarchy1 = memory_hierarchy_dut(multiplier_array1)

    core1 = Core(1, multiplier_array1, memory_hierarchy1)

    return {core1}


cores = cores()
global_buffer = None
acc_name = os.path.basename(__file__)[:-3]
accelerator = Accelerator(acc_name, cores, global_buffer)

a = 1
