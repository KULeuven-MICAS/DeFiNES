import logging

from typing import Generator, Callable, List, Tuple, Any

from classes.hardware.architecture.memory_hierarchy import MemoryHierarchy
from classes.stages.Stage import Stage
from classes.cost_model.cost_model import CostModelEvaluation
logger = logging.getLogger(__name__)


class DfStackCutIfWeightsOverflowStage(Stage):
    def __init__(self, list_of_callables, *, accelerator, workload, **kwargs):
        """
        Initialize the compare stage.
        """
        super().__init__(list_of_callables, **kwargs)
        self.workload = workload
        self.accelerator = accelerator

    def run(self):


        branches = 1
        nodes = list(self.workload.topological_sort())
        undividable_units = [[nodes[0]]]
        for node in nodes[1:]:  # skip inputlayernode
            branches -= self.workload.in_degree(node) - 1
            undividable_units[-1].append(node)
            if branches == 1:
                undividable_units.append([])
            branches += self.workload.out_degree(node) - 1
        assert len(undividable_units[-1]) == 0
        del undividable_units[-1]

        test_l = next(l for l in self.workload.nodes() if l.constant_operands)
        w_mem_op = test_l.memory_operand_links[test_l.constant_operands[0]]

        core = self.accelerator.get_core(next(l for l in self.workload.nodes() if hasattr(l, 'core_allocation')).core_allocation)
        max_s = core.memory_hierarchy.get_memory_levels(w_mem_op)[-2].memory_instance.size

        undividable_units_sizes = [sum(l.operand_size_bit[w] for l in d for w in l.constant_operands) for d in undividable_units]

        stack_cuts = []
        running_sum = 0
        last_layer = None
        for i, (du, ws) in enumerate(zip(undividable_units, undividable_units_sizes)):
            if ws > max_s:  # the unit itself does not fit => break down completely (we either do full units or none of it depth-first)
                if not stack_cuts or stack_cuts[-1] != last_layer:
                    if last_layer is not None:
                        stack_cuts.append(last_layer)
                stack_cuts.extend(du)
                running_sum = 0
            elif running_sum + ws > max_s:
                    stack_cuts.append(last_layer)
                    running_sum = ws
            else:
                running_sum += ws
            last_layer = du[-1]

        stack_cuts = [l.id for l in stack_cuts]
        sub_list_of_callables = self.list_of_callables[1:]
        substage = self.list_of_callables[0](sub_list_of_callables, accelerator=self.accelerator, workload=self.workload, df_stack_cuts=stack_cuts, **self.kwargs)
        for cme, extra in substage.run():
            yield cme, (stack_cuts, extra)