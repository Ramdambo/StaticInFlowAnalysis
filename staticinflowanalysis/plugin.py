# Core Library modules
import ast
import sys
from typing import Any, Generator, Tuple, Type, Sequence

if sys.version_info < (3, 8):
    # Third party modules
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata

# First party modules
from staticinflowanalysis.hoare import analyse, extract_flow_config
from staticinflowanalysis.typedefs import FlowConfig


class Plugin:

    name = 'flake8_staticinflowanalysis'
    version = importlib_metadata.version(name)

    def __init__(self, tree: ast.AST, lines: Sequence[str]):
        self._tree = tree
        self._lines = lines

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        flow_config: FlowConfig = extract_flow_config(self._lines)
        errors = analyse(self._tree, flow_config)

        for line, col, msg in errors:
            yield line, col, msg, type(self)
