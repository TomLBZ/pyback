from api.types import FileDict, FileEntry, FileLike
from typing import Any, List
from starlette.datastructures import UploadFile
import json

def readFile(file: Any) -> FileLike:
    if isinstance(file, UploadFile):
        return file.file.read() # synchronous read
    return None # other file types not supported

def fileToEntry(file: Any) -> FileEntry:
    fname: str = getattr(file, "filename", "uploaded_file")
    content_type: str = getattr(file, "content_type", "application/octet-stream")
    fbytes: FileLike = readFile(file)
    return (fname, fbytes, content_type)

def fileToParams(file: Any | List[Any] | None) -> FileDict | None:
    if file:
        if not isinstance(file, list): # single file
            entry: FileEntry = fileToEntry(file)
            return {"file": entry}
        entries: List[FileEntry] = [fileToEntry(f) for f in file]
        return {"files": entries}
    return None

def dataToFileDict(data: dict | Any) -> FileDict:
    if not isinstance(data, dict): # other data type, make it a dict
        data: dict = {"data": data} # by this point data becomes a dict
    res: FileDict = {}
    for key in data.keys():
        res[key] = (None, json.dumps(data[key]), "application/json")
    return res

def combineFileDicts(*dicts: FileDict) -> FileDict:
    res: FileDict = {}
    for d in dicts:
        res.update(d)
    return res