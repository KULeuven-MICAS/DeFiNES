from classes.stages import *
import argparse

parser = argparse.ArgumentParser(description="Setup DeFiNES inputs")
parser.add_argument('--workload', metavar='path', required=True, help='module path to workload, e.g. inputs.WL.Meta_prototype.workload_fsrcnn')
parser.add_argument('--accelerator', metavar='path', required=True, help='module path to the accelerator, e.g. inputs.HW.Meta_prototype')
parser.add_argument('--dfmode', type=str, required=True, help='overlap data storing mode(s); possible options: 1,2,3,12,13,23,123 '
                                                              '(1 for fully recompute, 2 for H cached V recompute, 3 for fully cached), '
                                                              'putting multiple digits together means try multiple modes together')
parser.add_argument('--tilex', type=int, required=True, help='depth first tilesize x')
parser.add_argument('--tiley', type=int, required=True, help='depth first tilesize y')
# parser.add_argument('--headname', type=str, required=True, help='result head name')

args = parser.parse_args()
import logging as _logging

_logging_level = _logging.INFO
_logging_format = '%(asctime)s - %(name)s.%(funcName)s +%(lineno)s - %(levelname)s - %(message)s'
_logging.basicConfig(level=_logging_level,
                     format=_logging_format)

####### WHERE THE RESULT FILES WILL BE SAVED TO (USERS CAN CHANGE) #######
result_saving_path = './result_pickle_files_2'
##########################################################################

# parse dfmode: 1 for fully recompute, 2 for H cached V recompute, 3 for fully cached
dfmode_parsed = []
for mode in args.dfmode:
    if mode == '1':
        dfmode_parsed.append((False, False))
    elif mode == '2':
        dfmode_parsed.append((True, False))
    elif mode == '3':
        dfmode_parsed.append((True, True))

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
    headname=args.accelerator.split('.')[-1] + '___' + args.workload.split('.')[-1] + '__',
    result_saving_path=result_saving_path,
    general_parameter_iterations={('df_horizontal_caching', 'df_vertical_caching'): tuple(dfmode_parsed)},
    dump_filename_pattern='{result_saving_path}/{headname}_{df_tilesize_x}_{df_tilesize_y}_{df_horizontal_caching}_{df_vertical_caching}.pkl'
)
mainstage.run()
