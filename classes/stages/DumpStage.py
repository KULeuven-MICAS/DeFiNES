import pickle
from typing import Generator, Any, Tuple
from classes.stages.Stage import Stage
from classes.cost_model.cost_model import CostModelEvaluation
import os
import gzip
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DumpStage(Stage):
    """
    Class that passes through all results yielded by substages, but dumps the results as a pickled list to a file
    at the end of the iteration
    """

    def __init__(self, list_of_callables, *, dump_filename_pattern, **kwargs):
        """

        :param list_of_callables: see Stage
        :param dump_filename_pattern: filename string formatting pattern, which can use named field whose values will be
        in kwargs (thus supplied by higher level runnables)
        :param kwargs: any kwargs, passed on to substages and can be used in dump_filename_pattern
        """
        super().__init__(list_of_callables, **kwargs)
        self.dump_filename_pattern = dump_filename_pattern

    def run(self) -> Generator[Tuple[CostModelEvaluation, Any], None, None]:

        substage = self.list_of_callables[0](self.list_of_callables[1:], **self.kwargs)
        list = []
        filename = self.dump_filename_pattern.format(**self.kwargs)
        for cme, extra_info in substage.run():
            list.append((cme, extra_info))
            yield cme, extra_info
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            pickle.dump(list, f, -1)

class StreamingDumpStage(Stage):
    """
    Class that passes through all results yielded by substages, but dumps the results as a pickled list to a file
    at the end of the iteration.
    Where DumpStage dumps a list of all results to a pickle file after complete iteration,
    this StreamingDumpStage opens the file before iteration and writes the results one by one to the file.
    This means that incomplete results will have been written if the program is killed,
    and that it is easier on the system memory as no list of results is cached to be written later.
    Furthermore, this one also writes compressed if the filename ends with gz
    """

    def __init__(self, list_of_callables, *, dump_filename_pattern, **kwargs):
        """

        :param list_of_callables: see Stage
        :param dump_filename_pattern: filename string formatting pattern, which can use named field whose values will be
        in kwargs (thus supplied by higher level runnables)
        :param kwargs: any kwargs, passed on to substages and can be used in dump_filename_pattern
        """
        super().__init__(list_of_callables, **kwargs)
        self.dump_filename_pattern = dump_filename_pattern

    def run(self) -> Generator[Tuple[CostModelEvaluation, Any], None, None]:

        substage = self.list_of_callables[0](self.list_of_callables[1:], **self.kwargs)
        filename = self.dump_filename_pattern.format(**self.kwargs)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        count = 0
        with gzip.open(filename, 'wb') if filename.endswith('.gz') else open(filename, 'wb') as f:
            for cme, extra_info in substage.run():
                pickle.dump((cme, extra_info), f, -1)
                count +=1
                yield cme, extra_info
        logger.debug(f"Wrote {count} objects")
