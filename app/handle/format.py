from pydantic import BaseModel

def dump(input: BaseModel,exclude: set[str] = None, include: set[str] = None):
    
    return input.model_dump(
        mode = 'json',
        exclude_unset = True,
        exclude = exclude,
        include = include
    )