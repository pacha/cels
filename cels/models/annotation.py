import re
from typing import List
from typing import Union
from dataclasses import dataclass

from cels import default
from cels.lib.show import show
from cels.exceptions import CelsInputError
from .operation import Operation


@dataclass
class Annotation:
    """An annotation of a key of the shape 'operation@index1,index2...'."""

    operation: Operation
    index_marker: str
    indices: List[Union[int, None]]

    def __init__(self, raw_annotation: str, index_marker: str = default.index_marker):
        # extract parts from the raw annotation string
        self.index_marker = re.escape(index_marker)
        operation_pattern = r"([a-z_]+)"
        index_pattern = r"((?: *_ *)|(?: *-?[0-9]+ *(?:, *-?[0-9]+ *)*(?:, *_ *)?))"
        pattern = f"^{operation_pattern}(?:{self.index_marker}{index_pattern})?$"
        regex = re.compile(pattern)
        result = regex.match(raw_annotation)
        if not result:
            raise CelsInputError(
                f"Annotation {raw_annotation} is invalid. "
                f"Annotations should follow the pattern 'operation[@index1[,index2[,index3[,...]]]'. "
                "Indices must be integers (positive and negative numbers are allowed). "
                "In the case of 'insert' and 'extend' operations, the rightmost index can be '_'"
            )

        # set operation
        operation_name = result.group(1)
        try:
            self.operation = Operation.get(operation_name)
        except KeyError:
            raise CelsInputError(
                f"Invalid operation {show(operation_name)}. "
                f"Valid operations are [{', '.join([str(operation) for operation in Operation.get_all()])}]"
            )

        # set indices
        index_str = result.group(2) or ""
        index_pattern = r"-?[0-9]+|_"
        indices_list = re.findall(index_pattern, index_str)
        self.indices = []
        if indices_list:
            # check that the operation takes indices
            if not self.operation.takes_indices:
                raise CelsInputError(
                    f"{show(self.operation)} operation cannot take any indices"
                )

            # convert indices to integer type
            underscore_present = False
            for index_str in indices_list:
                # if a underscore has been found, it should be the last element
                if underscore_present:
                    raise CelsInputError(
                        f"Invalid index {show(index_str)}: "
                        "underescore indices must always be in last position"
                    )
                try:
                    self.indices.append(int(index_str))
                except ValueError:
                    if index_str != "_":
                        raise CelsInputError(
                            f"Invalid index {show(index_str)}. Indices can only be integers or '_'"
                        )
                    if not self.operation.takes_underscore_index:
                        raise CelsInputError(
                            f"{show(self.operation)} operation cannot take a underscore index"
                        )
                    underscore_present = True
                    self.indices.append(None)
