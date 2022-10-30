from .ZigZagCostModelStage import ZigZagCostModelStage
from .DepthFirstStage import DepthFirstStage
from .DumpStage import DumpStage, StreamingDumpStage
from .GeneralParameterIteratorStage import GeneralParameterIteratorStage
from .LomaStage import LomaStage
from .MainInputParserStages import AcceleratorParserStage, WorkloadParserStage, WorkloadAndAcceleratorParserStage
from .ReduceStages import MinimalEnergyStage, MinimalLatencyStage, SumStage
from .RunOptStages import CacheBeforeYieldStage, RemoveExtraInfoStage, MultiProcessingGatherStage, MultiProcessingSpawnStage, SkipIfDumpExistsStage, YieldNothingStage
from .SpatialMappingConversionStage import SpatialMappingConversionStage
from .SpatialMappingGeneratorStage import SpatialMappingGeneratorStage
from .Stage import Stage, MainStage
from .TemporalOrderingConversionStage import TemporalOrderingConversionStage
from .WorkloadStage import WorkloadStage
from .DfStackCutIfWeightsOverflowStage import DfStackCutIfWeightsOverflowStage
from .MemOpRenameFor2LayerOpShareSameMemOpStage import MemOpRenameFor2LayerOpShareSameMemOpStage

"""
Parameter providers: these parameters are provided to substages by the following classes:
 - accelerator: AcceleratorParserStage, WorkloadAndAcceleratorParserStage, DepthFirstStage, MemOpRenameFor2LayerOpShareSameMemOpStage
 - workload: WorkloadParserStage, WorkloadAndAcceleratorParserStage, DepthFirstStage
 - temporal_mapping: LomaStage, TemporalMappingConversionStage
 - spatial_mapping: SpatialMappingGenerationStage, SpatialMappingConversionStage
 - layer: WorkloadStage, DepthFirstStage, MemOpRenameFor2LayerOpShareSameMemOpStage
 - multiprocessing_callback: MultiProcessingGatherStage
 - *:  GeneralParameterIteratorStage: can provide anything
 
Parameter consumers: these parameters are no longer provided to substages after the following classes
 - accelerator_path: AcceleratorParserStage, WorkloadAndAcceleratorParserStage
 - df_horizontal_caching: DepthFirstStage 
 - df_tilesize_x: DepthFirstStage
 - df_tilesize_y: DepthFirstStage
 - df_vertical_caching: DepthFirstStage
 - df_max_mls_to_skip: DepthFirstStage
 - dump_filename_pattern: DumpStage
 - general_parameter_iterations: GeneralParameterIteratorStage
 - multiprocessing_callback: MultiProcessingSpawnStage
 - workload: DepthFirstStage, WorkloadStage
 - workload_path: WorkloadParserStage, WorkloadAndAcceleratorParserStage
 
Parameters required: these stages require the following parameters:
 - ZigZagCostModelStage: accelerator, layer, spatial_mapping, temporal_mapping
 - WorkloadStage: workload
 - DepthFirstStage: accelerator, workload, df_tilesize_x, df_tilesize_y, df_horizontal_caching, df_vertical_caching
 - DumpStage: dump_filename_pattern
 - GeneralParameterIteratorStage: general_parameter_iterations
 - LomaStage: accelerator, layer, spatial_mapping
 - AcceleratorParserStage: accelerator_path
 - WorkloadParserStage: workload_path
 - WorkloadAndAcceleratorParserStage: workload_path, accelerator_path
 - MultiProcessingSpawnStage: multiprocessing_callback
 - SpatialMappingConversionStage: accelerator, layer
 - SpatialMappingGeneratorStage: accelerator, layer
 - TemporalOrderingConversionStage: accelerator, layer, spatial_mapping
 - SkipIfDumpExistStage: dump_filename_pattern
 - MemOpRenameFor2LayerOpShareSameMemOpStage: accelerator, layer
"""