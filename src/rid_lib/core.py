from abc import ABCMeta, abstractmethod
from .exceptions import *


ORN_SCHEME = "orn"

class MetaRID(ABCMeta):
    """Defines class properties for all RID types."""
        
    @property
    def context(cls):
        if cls.scheme is None:
            raise RIDTypeError(f"Scheme undefined for RID type {repr(cls)}")
        
        elif cls.scheme == ORN_SCHEME:
            if cls.namespace is None:
                raise RIDTypeError(f"Namespace undefined for ORN based RID type {repr(cls)}") 
            
            return cls.scheme + ":" + cls.namespace
        else:
            return cls.scheme


class RID(metaclass=MetaRID):
    scheme: str = None
    namespace: str | None = None
    
    # populated at runtime
    _context_table = {}
    _provisional_context = None
    
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
        cls._context_table[Class.context] = Class
    
    @classmethod
    def _create_provisional_context(
        cls, 
        scheme: str, 
        namespace: str | None = None
    ):
        if cls._provisional_context is None:
            raise Exception("Provisional context not set")
        
        if scheme == ORN_SCHEME:
            context_name = "".join([
                s.capitalize() for s in namespace.split(".")
            ])
        
        else:
            context_name = scheme.capitalize()
        
        return type(
            context_name, 
            (cls._provisional_context,), 
            dict(scheme=scheme, namespace=namespace)
        )
    
    @classmethod
    def from_string(cls, rid_string: str, allow_prov_ctx=False):
        if not isinstance(rid_string, str): raise Exception()
        
        i = rid_string.find(":")
        
        if i < 0: 
            raise InvalidRIDError(f"Failed to parse RID string '{rid_string}', missing context delimeter ':'")
        
        scheme = rid_string[0:i].lower()
        
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
        
        else:            
            if allow_prov_ctx:
                if scheme == ORN_SCHEME:
                    ContextClass = cls._create_provisional_context(
                        scheme=scheme,
                        namespace=namespace
                    )
                else:
                    ContextClass = cls._create_provisional_context(
                        scheme=scheme
                    )
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
    def __init__(self, reference):
        self._reference = reference
        
    @property
    def reference(self):
        return self._reference
    
    @classmethod
    def from_reference(cls, reference):
        return cls(reference)

RID._provisional_context = ProvisionalContext


class ORN(RID):
    scheme = ORN_SCHEME