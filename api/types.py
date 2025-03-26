from typing import Dict, Tuple, BinaryIO, List

FileLike = str | bytes | BinaryIO
FileEntry = Tuple[str, FileLike, str]
FileDict = Dict[str, FileEntry | List[FileEntry]]