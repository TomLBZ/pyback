# from api.funcmap_template import funcMap
from api.funcmap import funcMap
from api.utils import fileToParams, dataToFileDict, combineFileDicts
from typing import Any, List

def uniPostJson(body: dict = {}):
    op: str = body.get("op", None)
    data: dict = body.get("data", None)
    if op in funcMap:
        return funcMap[op](data) if data else funcMap[op]()
    return funcMap["error"]("Invalid operation: " + op)

def uniPostMultipart(body: dict = {}, file: Any = None, files: List[Any] | Any = None):
    op: str = body.get("op", None)
    data: Any = body.get("data", None)
    if op in funcMap: # op is valid
        fparams = fileToParams(file) if file else fileToParams(files) # prefer file over files
        if not fparams: # no file
            return funcMap[op](data) if data else funcMap[op]()
        if not data or len(data) == 0: # no data
            return funcMap[op](fparams)
        fparams = combineFileDicts(fparams, dataToFileDict(data))
        return funcMap[op](fparams)
    return funcMap["error"]("Invalid operation: " + op)

def uniPostOptions():
    return {"message": "Options"}