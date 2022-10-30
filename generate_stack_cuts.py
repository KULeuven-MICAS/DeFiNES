from classes.stages import *
import pickle

general_parameter_iterations = {('accelerator_path', 'workload_path', 'accelerator_path_copy', 'workload_path_copy'):[]}
for accel in ['Ascend_like', 'Edge_TPU_like', 'Meta_prototype', 'Tesla_NPU_like', 'TPU_like']:
    for suffix in ['', '_DF']:
        for wl in ['dmcnnvd', 'fsrcnn', 'mccnn', 'mobilenetv1', 'resnet18']:
            general_parameter_iterations[('accelerator_path', 'workload_path', 'accelerator_path_copy', 'workload_path_copy')].append(
                (f'inputs.ASPLOS.HW.{accel}{suffix}',f'inputs.ASPLOS.WL.{accel}.workload_{wl}')*2)

results = {}

class Custom(Stage):
    def run(self):
        results[(self.kwargs['accelerator_path_copy'], self.kwargs['workload_path_copy'])] = self.kwargs['df_stack_cuts']
        return
        yield None, None
    def is_leaf(self) -> bool:
        return True

mainstage = MainStage([
    GeneralParameterIteratorStage,
    WorkloadAndAcceleratorParserStage,
    DfStackCutIfWeightsOverflowStage,
    Custom
],
    general_parameter_iterations=general_parameter_iterations,
)
mainstage.run()
with open('ASPLOS_stack_cuts', 'wb') as f:
    pickle.dump(results, f)