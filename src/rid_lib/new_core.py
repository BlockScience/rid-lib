from abc import ABC, ABCMeta, abstractmethod
from os import name
from typing import Type

ORN_SCHEME = "orn"
URN_SCHEME = "urn"
NAMESPACE_SCHEMES = (ORN_SCHEME, URN_SCHEME)
BUILT_IN_TYPES = ("RID", "ORN", "URN")


class RIDType(ABCMeta):
    scheme: str | None = None
    namespace: str | None = None
    
    # maps RID type strings to their classes
    type_table: dict[str, Type] = dict() 
    
    def __new__(mcls, name, bases, dct):
        print(name, bases, dct)
        
        cls = super().__new__(mcls, name, bases, dct)
        
        # ignores built in RID types which aren't directly instantiated
        if name in BUILT_IN_TYPES:
            return cls
            
        if not getattr(cls, "scheme", None):
            raise TypeError(f"RID type '{name}' is missing 'scheme' definition")
        
        if not isinstance(cls.scheme, str):
            raise TypeError(f"RID type '{name}' 'scheme' must be of type 'str'")
        
        if cls.scheme in NAMESPACE_SCHEMES:
            if not getattr(cls, "namespace", None): 
                raise TypeError(f"RID type '{name}' is using namespace scheme but missing 'namespace' definition")
            if not isinstance(cls.namespace, str):
                raise TypeError(f"RID type '{name}' is using namespace scheme but 'namespace' is not of type 'str'")
                
        # check for abstract method implementation
        if cls.__abstractmethods__:
            raise TypeError(f"RID type '{name}' is missing implemenation(s) for abstract method(s) {set(cls.__abstractmethods__)}")
        
        mcls.type_table[str(cls)] = cls
        return cls
    
    def __str__(cls) -> str:
        if cls.scheme in NAMESPACE_SCHEMES:
            return cls.scheme + ":" + cls.namespace
        else:
            return cls.scheme
        
    # backwards compatibility
    @property
    def context(cls) -> str:
        return str(cls)
    
    @classmethod
    def from_string(mcls, rid_type_string: str) -> Type["RID"]:
        if not isinstance(rid_type_string, str):
            raise TypeError(f"RID type string '{rid_type_string}' must be of type 'str'")
            
        if rid_type_string in mcls.type_table:
            return mcls.type_table[rid_type_string]
        
        i = rid_type_string.find(":")
        
        if i < 0:
            scheme = rid_type_string
            namespace = None
            
            if scheme in NAMESPACE_SCHEMES:
                raise TypeError(f"RID type string '{rid_type_string}' is a namespace scheme but is missing a namespace component")
            
        else:
            scheme = rid_type_string[:i]
            
            if scheme not in NAMESPACE_SCHEMES:
                raise TypeError(f"RID type string '{rid_type_string}' contains a ':'-separated namespace component, but scheme doesn't support namespaces")
                
            j = rid_type_string.find(":", i+1)
            
            if j < 0:
                namespace = rid_type_string[i+1:]
            else:
                raise TypeError(f"RID type string '{rid_type_string}' should contain a maximum of two ':'-separated components") 
        
        if scheme == "":
            raise TypeError(f"RID type string '{rid_type_string}' cannot have an empty scheme")
        
        if namespace == "":
            raise TypeError(f"RID type string '{rid_type_string}' cannot have an empty namespace")
     
        if namespace:
            name = "".join([s.capitalize() for s in namespace.split(".")])
        else:
            name = scheme.capitalize()
            
        cls = type(
            name=name, 
            bases=(RID,),
            dict=dict(scheme=scheme, namespace=namespace)
        )
        
        mcls.type_table[rid_type_string] = cls
        return cls
        
class RID(metaclass=RIDType):
    @property
    def type(self):
        return self.__class__
    
    @property
    def context(self):
        return str(self.type)
    
    def __str__(self) -> str:
        return str(self.type) + ":" + self.reference
    
    def __repr__(self) -> str:
        return f"<{self.type.__name__} RID '{str(self)}'>"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return str(self) == str(other)
        else:
            return False
    
    def __hash__(self):
        return hash(str(self))
    
    @classmethod
    def from_string(cls, rid_string: str) -> "RID":
        if not isinstance(rid_string, str):
            raise TypeError(f"RID string '{rid_string}' must be of type 'str'")
        
        i = rid_string.find(":")
        
        if i < 0:
            raise TypeError(f"RID string '{rid_string}' should contain a ':'-separated type and reference")
        
        scheme = rid_string[0:i]
        namespace = None
        
        if scheme == ORN_SCHEME:
            j = rid_string.find(":", i+1)
            if j < 0:
                raise TypeError(f"Failed to parse ORN RID string '{rid_string}', missing namespace delimeter ':'")
            
            namespace = rid_string[i+1:j]
            
            context = rid_string[0:j].lower()
            reference = rid_string[j+1:]
        
        else:
            context = rid_string[0:i].lower()
            reference = rid_string[i+1:]
        
        return
        
        components = rid_string.split(":", 2)
        
        if len(components) < 2:
            raise TypeError(f"RID string '{rid_string}' should contain at least two ':'-separated component")
        elif len(components) == 2:
            scheme, reference = components
            rid_type_string = scheme
        elif len(components) == 3:
            scheme, namespace, reference = components
            rid_type_string = ":".join(scheme, namespace)
            
        return RIDType.from_string(rid_type_string).from_reference(reference)
    
    @abstractmethod
    def __init__(self, *args, **kwargs):
        ...
    
    @classmethod
    @abstractmethod
    def from_reference(cls, reference: str):
        ...
    
    @property
    @abstractmethod
    def reference(self) -> str:
        ...


class ORN(RID):
    scheme = ORN_SCHEME
    
class URN(RID):
    scheme = URN_SCHEME