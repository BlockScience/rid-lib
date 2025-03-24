from typing import TypeVar
from pydantic import BaseModel
from rid_lib.core import RID
from .manifest import Manifest


T = TypeVar("T", bound=BaseModel)

class Bundle(BaseModel):
    """A Knowledge Bundle composed of a manifest and optional contents associated with an RIDed object.

    A container object for the cached data associated with an RID. It is 
    returned by the read function of Cache.
    """
    manifest: Manifest
    contents: dict
    
    @classmethod
    def generate(cls, rid: RID, contents: dict):
        return cls(
            manifest=Manifest.generate(rid, contents),
            contents=contents
        )
    
    @property
    def rid(self):
        return self.manifest.rid
    
    def validate_contents(self, model: type[T]) -> T:
        return model.model_validate(self.contents)