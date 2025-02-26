from typing import Type, Callable
from enum import StrEnum
from rid_lib import RID
from rid_lib.exceptions import RIDError
from .bundle import Bundle
from .cache import Cache
from .manifest import Manifest


class RIDEffectorError(RIDError):
    pass


class ActionType(StrEnum):
    dereference = "dereference"
    
class ProxyHandler:
    def __init__(self, effector):
        self.effector = effector
        
    def __getattr__(self, action_type):
        # shortcut to execute actions, use action type as function name
        def execute(rid: RID, *args, **kwargs):
            return self.effector.execute(action_type, rid, *args, **kwargs)
        return execute

class Effector:
    def __init__(self, cache: Cache | None = None):
        self.cache = cache
        self._action_table = {}
        self.run = ProxyHandler(self)
        
    def register(
        self, 
        action_type: ActionType, 
        rid_type: Type[RID] | str | tuple[Type[RID] | str]
    ):
        def decorator(func: Callable[[RID], Bundle | dict | None]):
            # accept type or list of types to register
            if isinstance(rid_type, (list, tuple)):
                rid_types = rid_type
            else:
                rid_types = (rid_type,)
            
            # retrieve context from RID objects, or use str directly
            for _rid_type in rid_types:
                if isinstance(_rid_type, type) and issubclass(_rid_type, RID):
                    context = _rid_type.context
                else:
                    context = _rid_type         
            
                self._action_table[(action_type, context)] = func
            
            return func
        return decorator
    
    def execute(self, action_type: str, rid: RID, *args, **kwargs):
        action_pair = (action_type, rid.context)
        if action_pair in self._action_table:
            func = self._action_table[action_pair]
            return func(rid, *args, **kwargs)
        else:
            raise RIDEffectorError(f"Failed to execute, no action found for action pair '{action_pair}'")
        
    def register_dereference(self, rid_type: Type[RID] | str | tuple[Type[RID] | str]):
        return self.register(ActionType.dereference, rid_type)
        
    def deref(
        self, 
        rid: RID, 
        hit_cache=True, # tries to read cache first, writes to cache if there is a miss
        refresh=False   # refreshes cache even if there was a hit
    ) -> Bundle | None:
        if (
            self.cache is not None and 
            hit_cache is True and 
            refresh is False
        ):
            bundle = self.cache.read(rid)
            if (
                bundle is not None and 
                bundle.contents is not None
            ):
                return bundle
        
        raw_data = self.execute(ActionType.dereference, rid)
        
        if raw_data is None: 
            return
        elif isinstance(raw_data, Bundle):
            bundle = raw_data
        else:            
            manifest = Manifest.generate(rid, raw_data)
            bundle = Bundle(manifest, raw_data)
        
        if (
            self.cache is not None and 
            hit_cache is True
        ):
            self.cache.write(rid, bundle)
        
        return bundle
