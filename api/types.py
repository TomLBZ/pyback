from typing import Dict, Tuple, Union, BinaryIO

FileEntryData = Union[str, bytes, BinaryIO]
FileEntry = Tuple[str, FileEntryData, str]
FileDict = Dict[str, FileEntry]