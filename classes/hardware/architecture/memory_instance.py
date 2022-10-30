from typing import Tuple


class MemoryInstance:
    def __init__(self, name: str, size: int, r_bw: int, w_bw: int, r_cost: float, w_cost: float, area: float,
                 bank: int, random_bank_access: bool, r_port: int, w_port: int, rw_port: int, latency: int,
                 min_r_granularity=None, min_w_granularity=None):
        """
        Collect all the basic information of a physical memory module.

        :param name: memory module name, e.g. 'SRAM_512KB_BW_16b', 'I_RF'.
        :param size: total memory capacity (unit: bit).
        :param r_bw/w_bw: memory bandwidth (or wordlength) (unit: bit/cycle).
        :param r_cost/w_cost: memory unit data access energy.
        :param area: memory area (unit can be whatever user-defined unit).
        :param bank: number of memory banks.
        :param random_bank_access: whether the memory support random bank access or not.
        :param r_port: number of memory read port.
        :param w_port: number of memory write port (rd_port and wr_port can work in parallel).
        :param rw_port: number of memory port for both read and write (read and write cannot happen in parallel).
        :param latency: memory access latency (unit: number of cycles).
        """
        # TODO: Add standard values for some parameters if the user quickly wants to define and doesn't care?
        # TODO: Make different child classes for RF, SRAM, ... that might not use some of these above parameters?
        # TODO: Add for which operands this memory is used?
        self.name = name
        self.size = size
        self.r_bw = r_bw
        self.w_bw = w_bw
        self.r_cost = r_cost
        self.w_cost = w_cost
        self.area = area
        self.bank = bank
        self.random_bank_access = random_bank_access
        self.r_port = r_port
        self.w_port = w_port
        self.rw_port = rw_port
        self.latency = latency
        if not min_r_granularity:
            self.r_bw_min = r_bw
        else:
            self.r_bw_min = min_r_granularity
        if not min_w_granularity:
            self.w_bw_min = w_bw
        else:
            self.w_bw_min = min_w_granularity

    def __jsonrepr__(self):
        """
        JSON Representation of this class to save it to a json file.
        """
        return self.__dict__
