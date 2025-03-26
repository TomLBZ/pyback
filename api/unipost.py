# from api.funcmap_template import funcMap
from api.funcmap import funcMap
from starlette.datastructures import UploadFile
from typing import Any, List
from api.types import FileDict, FileEntry, FileEntryData

def uniPostJson(body: dict = {}):
    op: str = body.get("op", None)
    data: dict = body.get("data", None)
    if op in funcMap:
        return funcMap[op](data) if data else funcMap[op]()
    return funcMap["error"]("Invalid operation: " + op)

def readFile(file: Any) -> FileEntryData:
    if isinstance(file, UploadFile):
        return file.file.read() # synchronous read
    return None # other file types not supported

def fileToParams(file: Any) -> FileDict:
    fname: str = getattr(file, "filename", "uploaded_file")
    content_type: str = getattr(file, "content_type", "application/octet-stream")
    fbytes: FileEntryData = readFile(file)
    fentry: FileEntry = (fname, fbytes, content_type)
    return { "file": fentry }

def uniPostMultipart(body: dict = {}, file: Any = None, files: List[Any] | Any = None):
    op: str = body.get("op", None)
    data: dict = body.get("data", None)
    if op in funcMap: # op is valid
        if file: # single file
            fparams: FileDict = fileToParams(file)
            return funcMap[op](data, fparams) if data else funcMap[op](fparams)
        elif files: # multiple files
            fparams: List[FileDict] = [fileToParams(f) for f in files]
            return funcMap[op](data, fparams) if data else funcMap[op](fparams)
        else: # no file
            return funcMap[op](data) if data else funcMap[op]()
    return funcMap["error"]("Invalid operation: " + op)

def uniPostOptions():
    return {"message": "Options"}