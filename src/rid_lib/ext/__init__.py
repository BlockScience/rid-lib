try:
    import pydantic
    
except ImportError:
    RID_EXT_ENABLED = False
    
    print("ERROR: To use the rid-lib extension module, optional dependencies be installed with `pip install rid-lib[ext]`.")

else:
    RID_EXT_ENABLED = True

    from .manifest import Manifest
    from .cache import Cache, CacheBundle
    from .event import Event, EventType
    from .effector import ActionType, Effector