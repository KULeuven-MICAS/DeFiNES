from classes.hardware.architecture.accelerator import Accelerator
from classes.mapping.spatial.spatial_mapping import SpatialMapping
from classes.opt.temporal.loma.engine import LomaEngine
from classes.workload.layer_node import LayerNode
import classes.io.input_config as inputs
from typing import Generator, Callable, List, Tuple, Any
from classes.stages.Stage import Stage
from classes.cost_model.cost_model import CostModelEvaluation


class LomaStage(Stage):
    """
    Class that iterates through the different temporal mappings generated through
    the loop order based memory allocation (loma) engine
    """
    def __init__(self, list_of_callables: List[Callable], *, accelerator, layer, spatial_mapping, **kwargs):
        """
        Note: Initially the engine is set to None.
        When the stage is ran through the run() method, this will be set
        to the loma engine with parameters present in the inputs.
        """
        super().__init__(list_of_callables, **kwargs)
        self.accelerator, self.layer, self.spatial_mapping = accelerator, layer, spatial_mapping
        self.engine = None

    def run(self):
        self.engine = LomaEngine(accelerator=self.accelerator, layer=self.layer, spatial_mapping=self.spatial_mapping,
                                 **self.kwargs)

        for tm in self.engine.run():
            kwargs = self.kwargs.copy()
            kwargs['accelerator'] = self.accelerator
            kwargs['layer'] = self.layer
            kwargs['spatial_mapping'] = self.spatial_mapping
            kwargs['temporal_mapping'] = tm
            sub_stage = self.list_of_callables[0](self.list_of_callables[1:], **kwargs)
            for cme, extra_info in sub_stage.run():
                yield cme, (tm, extra_info)
