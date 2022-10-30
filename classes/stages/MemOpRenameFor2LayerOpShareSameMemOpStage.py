from typing import Generator, Callable, List, Tuple, Any
from classes.stages.Stage import Stage

import numpy as np
import logging
from utils import pickle_deepcopy
from classes.cost_model.cost_model import CostModelEvaluation
from classes.hardware.architecture.accelerator import Accelerator
from classes.mapping.spatial.spatial_mapping import SpatialMapping
from classes.mapping.temporal.temporal_mapping import TemporalMapping
from classes.workload.layer_node import LayerNode
import classes.io.input_config as inputs
logger = logging.getLogger(__name__)


class MemOpRenameFor2LayerOpShareSameMemOpStage(Stage):
    """
    Rename memory's operand if 2 input operands share the same memory levels,
    e.g. 'memory_operand_links': {'O': 'O', 'X': 'I1', 'Y': 'I1'}
    - First, remove all the I2 operand in memory hierarchy.
      (If a memory level is used by I2 and other mem op, remove I2;
       If a memory is only used for I2, then remove that memory level.)
    - Second, add the I2 to all the locations where the first mem op operand (I1) are,
      link the new 2nd mem_op (I2) to the 2nd layer_op (Y).
    """
    def __init__(self, list_of_callables: List[Callable], *, accelerator, layer, **kwargs):
        """
        Initializes the memory operand renaming stage given main inputs
        """
        super().__init__(list_of_callables, **kwargs)
        self.accelerator = accelerator
        self.layer = layer

    def run(self):
        """
        Run the stage: update the accelerator and layer's operand definition for a single run
        """
        kwargs = self.kwargs.copy()
        mem_op_count = len(set(self.layer.memory_operand_links.values()))
        layer_op_count = len((self.layer.memory_operand_links.keys()))

        if mem_op_count == layer_op_count:
            kwargs['accelerator'] = self.accelerator
            kwargs['layer'] = self.layer
        else:
            accelerator_new, layer_new = self.mem_op_rename()
            kwargs['accelerator'] = accelerator_new
            kwargs['layer'] = layer_new

        sub_stage = self.list_of_callables[0](self.list_of_callables[1:], **kwargs)
        for cme, extra_info in sub_stage.run():
            yield cme, extra_info

    def mem_op_rename(self):
        accelerator_mem_level_removed = pickle_deepcopy(self.accelerator)
        layer_new = pickle_deepcopy(self.layer)
        memhier = accelerator_mem_level_removed.get_core(self.layer.core_allocation).memory_hierarchy

        if [layer_new.memory_operand_links[I] for I in layer_new.input_operands] == ['I1', 'I1']:
            while memhier.remove_operator_top_level('I2')[0]:
                pass
            for ml in memhier.nodes:
                if 'I1' in ml.operands:
                    ml.operands.append('I2')
                    ml.mem_level_of_operands['I2'] = ml.mem_level_of_operands['I1']
                    l = list(ml.port_alloc_raw)
                    l.append(ml.port_alloc_raw[ml.operands.index('I1')].copy())
                    ml.port_alloc_raw = tuple(l)
                    for p in (ml.port_list):
                        for sold in p.served_op_lv_dir[:]:
                            if sold[0] == 'I1':
                                p.add_port_function(tuple(['I2'] + list(sold[1:])))
            memhier.nb_levels['I2'] = memhier.nb_levels['I1']
            layer_new.memory_operand_links[layer_new.input_operands[1]] = 'I2'
            accelerator_mem_level_removed.get_core(layer_new.core_allocation).recalculate_memory_hierarchy_information()

        return accelerator_mem_level_removed, layer_new