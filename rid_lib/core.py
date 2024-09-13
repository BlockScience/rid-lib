import requests
from abc import ABCMeta, abstractmethod


ORI_SCHEME = "ori"

class MetaRID(ABCMeta):
    """Defines class properties for all RID types."""
    @property
    def obj_type(cls):
        if cls.scheme == ORI_SCHEME:
            return cls.space + "." + cls.form
        else:
            return None
        
    @property
    def context(cls):
        if cls.scheme == ORI_SCHEME:
            return cls.scheme + ":" + cls.obj_type
        else:
            return cls.scheme


class RID(metaclass=MetaRID):
    scheme: str = ORI_SCHEME
    space: str | None = None
    form: str | None = None
    
    # populated at runtime
    _context_table = {}
    _provisional_context = None
    
    def __new__(cls, *args, **kwargs):
        if cls.scheme == ORI_SCHEME:
            if not (cls.space and cls.form):
                print("space and form are required for an rid")
                
        else:
            if cls.space or cls.form:
                print("space and form can only be used if scheme is rid")
                
        
        return super().__new__(cls)
        
    @property
    def obj_type(self):
        return self.__class__.obj_type
    
    @property
    def context(self):
        return self.__class__.context
            
    def __str__(self):
        return self.context + ":" + self.reference
    
    def __repr__(self):
        return f"<{self.__class__.__name__} RID '{str(self)}'>"
    
    @classmethod
    def register_context(cls, Class):
        cls._context_table[Class.context] = Class
    
    @classmethod
    def _create_provisional_context(
        cls, 
        scheme: str = ORI_SCHEME, 
        space: str | None = None,
        form: str | None = None
    ):
        if cls._provisional_context is None:
            raise Exception("Provisional context not set")
        
        if scheme == ORI_SCHEME:
            if (space is None) or (form is None):
                raise Exception()
            
            context_name = space.capitalize() + form.capitalize()
        
        else:
            context_name = scheme.capitalize()
        
        return type(
            context_name, 
            (cls._provisional_context,), 
            dict(scheme=scheme, space=space, form=form)
        )
    
    @classmethod
    def from_string(cls, string: str, use_provisional_contexts=False):
        if not isinstance(string, str): raise Exception()
        
        i = string.find(":")
        
        if i < 0: raise Exception()
        
        scheme = string[0:i].lower()
        space, form = None, None
        
        if scheme == ORI_SCHEME:
            j = string.find(":", i+1)
            if j < 0: raise Exception()
            
            obj_type = string[i+1:j]
            if obj_type.count(".") != 1: raise Exception()
            space, form = obj_type.split(".")
            
            context = string[0:j].lower()
            reference = string[j+1:]
        
        else:
            context = string[0:i].lower()
            reference = string[i+1:]
        
        if context in cls._context_table:
            ContextClass = cls._context_table[context]
        
        else:            
            if use_provisional_contexts:
                if scheme == ORI_SCHEME:
                    ContextClass = cls._create_provisional_context(
                        space=space,
                        form=form
                    )
                else:
                    ContextClass = cls._create_provisional_context(
                        scheme=scheme
                    )
            else:
                raise Exception()
                
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

