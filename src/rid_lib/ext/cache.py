import os
import shutil
from rid_lib.core import RID
from .manifest import Manifest
from .bundle import Bundle
from .utils import b64_encode, b64_decode


class Cache:
    def __init__(self, directory_path: str):
        self.directory_path = directory_path
        
    def file_path_to(self, rid: RID) -> str:
        encoded_rid_str = b64_encode(str(rid))
        return f"{self.directory_path}/{encoded_rid_str}.json"

    def write(self, rid: RID, cache_bundle: Bundle) -> Bundle:
        """Writes bundle to cache, returns a Bundle."""
        if cache_bundle.manifest.rid != rid:
            raise ValueError("The provided Bundle's Manifest RID must be equivalent to the 'rid' param.")

        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path)
            
        with open(self.file_path_to(rid), "w") as f:
            f.write(cache_bundle.model_dump_json(indent=2))

        return cache_bundle
    
    def bundle_and_write(self, rid: RID, data: dict) -> Bundle:
        return self.write(
            rid,
            Bundle(
                manifest=Manifest.generate(rid, data),
                contents=data
            )
        )
        
    def write_manifest_only(self, rid: RID, manifest: Manifest) -> Bundle:
        return self.write(
            rid,
            Bundle(manifest=manifest)
        )
    
    def exists(self, rid: RID) -> bool:
        return os.path.exists(
            self.file_path_to(rid)
        )

    def read(self, rid: RID) -> Bundle | None:
        """Reads and returns CacheEntry from RID cache."""
        try:
            with open(self.file_path_to(rid), "r") as f:
                return Bundle.model_validate_json(f.read())
        except FileNotFoundError:
            return None
        
    def read_all_rids(self) -> list[RID]:
        if not os.path.exists(self.directory_path):
            return []
        
        rids = []
        for filename in os.listdir(self.directory_path):
            encoded_rid_str = filename.split(".")[0]
            rid_str = b64_decode(encoded_rid_str)
            rid = RID.from_string(rid_str, allow_prov_ctx=True)
            rids.append(rid)
            
        return rids
                
    def delete(self, rid: RID) -> None:
        """Deletes cache bundle."""
        try:
            os.remove(self.file_path_to(rid))
        except FileNotFoundError:
            return

    def drop(self) -> None:
        """Deletes all cache bundles."""
        try:
            shutil.rmtree(self.directory_path)
        except FileNotFoundError:
            return

