from typing import ClassVar, TypeVar
from pydantic import BaseModel
from rid_lib.core import RID, RIDType
from .manifest import Manifest


T = TypeVar("T", bound=BaseModel)

class Bundle(BaseModel):
    """A knowledge bundle composed of a manifest and contents associated with an RIDed object.

    Acts as a container for the data associated with an RID. It is written to and read from the cache.
    """
    manifest: Manifest
    contents: dict
    
    _model_table: ClassVar[dict[RIDType, type[BaseModel]]] = {}
    
    @classmethod
    def bind_schema(cls, rid_type: RIDType, model: type[BaseModel]):
        cls._model_table[rid_type] = model
    
    @classmethod
    def generate(cls, rid: RID, contents: dict) -> "Bundle":
        """Generates a bundle from provided RID and contents."""
        return cls(
            manifest=Manifest.generate(rid, contents),
            contents=contents
        )
    
    @property
    def rid(self):
        """This bundle's RID."""
        return self.manifest.rid
    
    @property
    def model(self):
        if type(self.rid) not in self._model_table:
            raise NotImplementedError(f"RID type {type(self.rid)} has no bound model")
        
        model = self._model_table[type(self.rid)]
        return model.model_validate(self.contents)
    
    def validate_contents(self, model: type[T]) -> T:
        """Attempts to validate contents against a Pydantic model."""
        return model.model_validate(self.contents)