from classes.stages import *
import argparse

parser = argparse.ArgumentParser(description="Setup zigzag-v2 inputs")
parser.add_argument('--workload', metavar='path', required=True, help='module path to workload, e.g. inputs.examples.workload1')
parser.add_argument('--accelerator', metavar='path', required=True, help='module path to the accelerator, e.g. inputs.examples.accelerator1')
parser.add_argument('--tilex', type=int, required=True, help='depth first tilesize x')
parser.add_argument('--tiley', type=int, required=True, help='depth first tilesize y')
parser.add_argument('--headname', type=str, required=True, help='result head name')

args = parser.parse_args()
import logging as _logging

_logging_level = _logging.INFO
_logging_format = '%(asctime)s - %(name)s.%(funcName)s +%(lineno)s - %(levelname)s - %(message)s'
_logging.basicConfig(level=_logging_level,
                     format=_logging_format)

####### WHERE THE RESULT FILES WILL BE SAVED TO (USERS CAN CHANGE) #######
result_saving_path = './result_pickle_files'
##########################################################################

mainstage = MainStage([
    WorkloadAndAcceleratorParserStage,
    GeneralParameterIteratorStage,
    SkipIfDumpExistsStage,
    DumpStage,
    DfStackCutIfWeightsOverflowStage,
    DepthFirstStage,
    SpatialMappingConversionStage,
    RemoveExtraInfoStage,
    MinimalEnergyStage,
    LomaStage,
    ZigZagCostModelStage
],
    accelerator_path=args.accelerator,
    workload_path=args.workload,
    loma_lpf_limit=6,
    df_tilesize_x=args.tilex,
    df_tilesize_y=args.tiley,
    # df_max_mls_to_skip=1,
    headname=args.headname,
    general_parameter_iterations={('df_horizontal_caching', 'df_vertical_caching'): ((True, True), (True, False), (True, True))},
    dump_filename_pattern='{result_saving_path}/{headname}_{df_tilesize_x}_{df_tilesize_y}_{df_horizontal_caching}_{df_vertical_caching}.pkl'
)
mainstage.run()
