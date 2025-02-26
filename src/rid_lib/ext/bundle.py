from pydantic import BaseModel
from .manifest import Manifest


class Bundle(BaseModel):
    """A Knowledge Bundle composed of a manifest and optional contents associated with an RIDed object.

    A container object for the cached data associated with an RID. It is 
    returned by the read function of Cache.
    """
    manifest: Manifest
    contents: dict | None = None