from classes.stages import *
import numpy as np
import logging as _logging
from plot_artifact import plot_Fig12_total_en_and_la_heatmap

_logging_level = _logging.INFO
_logging_format = '%(asctime)s - %(name)s.%(funcName)s +%(lineno)s - %(levelname)s - %(message)s'
_logging.basicConfig(level=_logging_level,
                     format=_logging_format)

####### WHERE THE RESULT FILES WILL BE SAVED TO (USERS CAN CHANGE) #######
result_saving_path = './result_pickle_files'
##########################################################################

# actual run settings:
df_modes = ((False, False), (True, False), (True, True))
df_x_tilesizes = (1, 4, 16, 60, 240, 960)
df_y_tilesizes = (1, 4, 18, 72, 270, 540)
plotinfo = np.empty((3, 2, 6, 6))  # 3 rows for different overlap-storing modes, 2 columns for energy and latency, and a 6x6 y by x tilesize grid

# fast testing settings:
# df_x_tilesizes = (1, )
# df_y_tilesizes = (1, )
# plotinfo = np.random.rand(3, 2, 6, 6)  # 3 rows for different overlap-storing modes, 2 columns for energy and latency, and a 6x6 y by x tilesize grid

class CS1_Result_Collector_Stage(Stage):
    """
    Collects the info required to the plot into the global plotinfo variable
    """

    def __init__(self, list_of_callables, **kwargs):
        """
        Initialize the compare stage.
        """
        super().__init__(list_of_callables, **kwargs)

    def run(self):
        """
        Runs this stage
        """
        sub_list_of_callables = self.list_of_callables[1:]
        substage = self.list_of_callables[0](sub_list_of_callables, **self.kwargs)

        for cme, extra_info in substage.run():
            pass
            i0 = df_modes.index((self.kwargs['df_horizontal_caching'], self.kwargs['df_vertical_caching']))
            i2 = df_y_tilesizes.index(self.kwargs['df_tilesize_y'])
            i3 = df_x_tilesizes.index(self.kwargs['df_tilesize_x'])
            plotinfo[i0, 0, i2, i3] += cme.energy_total
            plotinfo[i0, 1, i2, i3] += cme.latency_total1
        return  # these two line makes this a generator, as required per definition of Stage,
        # although an empty one (intended).
        # We don't care about the results anymore, the relevant metrics are already gathered by this stage
        yield None, None


mainstage = MainStage([
    WorkloadAndAcceleratorParserStage,
    GeneralParameterIteratorStage,
    CS1_Result_Collector_Stage,
    DumpStage,
    DfStackCutIfWeightsOverflowStage,
    DepthFirstStage,
    SpatialMappingConversionStage,
    RemoveExtraInfoStage,
    MinimalEnergyStage,
    LomaStage,
    ZigZagCostModelStage
],
    loma_lpf_limit=8,
    workload_path='inputs.WL.Meta_prototype.workload_fsrcnn',
    accelerator_path='inputs.HW.Meta_prototype_DF',
    result_saving_path=result_saving_path,
    dump_filename_pattern='{result_saving_path}/{df_tilesize_x}_{df_tilesize_y}_{df_horizontal_caching}_{df_vertical_caching}.pkl',
    general_parameter_iterations={('df_horizontal_caching', 'df_vertical_caching'): df_modes,
                                  'df_tilesize_x': df_x_tilesizes,
                                  'df_tilesize_y': df_y_tilesizes}
)

if __name__ == '__main__':
    mainstage.run()
    plot_Fig12_total_en_and_la_heatmap(plotinfo)
