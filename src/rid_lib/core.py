from abc import ABCMeta, abstractmethod
from .exceptions import *


ORN_SCHEME = "orn"

class MetaRID(ABCMeta):
    """Defines class properties for all RID types."""
    
    @staticmethod
    def validate_rid_type_definition(RIDType):
        if RIDType.scheme is None:
            raise RIDTypeError(f"Scheme undefined for RID type {repr(RIDType)}")
        
        elif RIDType.scheme == ORN_SCHEME:
            if RIDType.namespace is None:
                raise RIDTypeError(f"Namespace undefined for ORN based RID type {repr(RIDType)}") 
        
    @property
    def context(cls):
        MetaRID.validate_rid_type_definition(cls)
        
        if cls.scheme == ORN_SCHEME:
            return cls.scheme + ":" + cls.namespace
        else:
            return cls.scheme
        

class RID(metaclass=MetaRID):
    scheme: str = None
    namespace: str | None = None
    
    using_prov_ctx = False
    
    # populated at runtime
    _context_table = {}
    _provisional_context_table = {}
    
    _ProvisionalContext = None
    
    @property
    def context(self):
        return self.__class__.context
            
    def __str__(self):
        return self.context + ":" + self.reference
    
    def __repr__(self):
        return f"<{self.__class__.__name__} RID '{str(self)}'>"
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return str(self) == str(other)
        else:
            return False
    
    @classmethod
    def register_context(cls, Class):
        MetaRID.validate_rid_type_definition(Class)
        cls._context_table[Class.context] = Class
    
    @classmethod
    def from_string(cls, rid_string: str, allow_prov_ctx=True):
        if not isinstance(rid_string, str): raise InvalidRIDError("rid_string must be of type 'str'")
        
        i = rid_string.find(":")
        
        if i < 0: 
            raise InvalidRIDError(f"Failed to parse RID string '{rid_string}', missing context delimeter ':'")
        
        scheme = rid_string[0:i].lower()
        namespace = None
        
        if scheme == ORN_SCHEME:
            j = rid_string.find(":", i+1)
            if j < 0:
                raise InvalidRIDError(f"Failed to parse ORN RID string '{rid_string}', missing namespace delimeter ':'")
            
            namespace = rid_string[i+1:j]
            
            context = rid_string[0:j].lower()
            reference = rid_string[j+1:]
        
        else:
            context = rid_string[0:i].lower()
            reference = rid_string[i+1:]
        
        
        if context in cls._context_table:
            ContextClass = cls._context_table[context]
        
        elif allow_prov_ctx:
            if context in cls._provisional_context_table:
                # use existing provisional context class
                ContextClass = cls._provisional_context_table[context]
            
            else:
                # create new provisional context class
                if scheme == ORN_SCHEME:
                    prov_context_classname = "".join([
                        s.capitalize() for s in namespace.split(".")
                    ])
                else:
                    prov_context_classname = scheme.capitalize()
                
                ContextClass = type(
                    prov_context_classname, 
                    (cls._ProvisionalContext,), 
                    dict(scheme=scheme, namespace=namespace)
                )
                cls._provisional_context_table[context] = ContextClass
        else:
            raise InvalidRIDError(f"Context '{context}' undefined for RID string '{rid_string}' (enable provisional contexts to avoid this error with `allow_prov_ctx=True`)")
                
        return ContextClass.from_reference(reference)
    
    @classmethod
    @abstractmethod
    def from_reference(cls, reference):
        pass
    
    @property
    @abstractmethod
    def reference(self):
        pass


class ProvisionalContext(RID):
    using_prov_ctx = True
    
    def __repr__(self):
        return f"<{self.__class__.__name__} RID '{str(self)}' (Provisional Context)>"
    
    def __init__(self, reference):
        self._reference = reference
        
    @property
    def reference(self):
        return self._reference
    
    @classmethod
    def from_reference(cls, reference):
        return cls(reference)

RID._ProvisionalContext = ProvisionalContext


class ORN(RID):
    scheme = ORN_SCHEME