from rid_lib.core import RID
from rid_lib.exceptions import RIDError

try:
    import pydantic
    
except ImportError:
    USING_PYDANTIC = False
    
    print("WARNING: You are using rid_lib extensions without additional dependencies, features will be limited. Install with `pip install rid_lib[ext]`.")
    
    from dataclasses import dataclass
    RIDFieldAnnotation = None
    
else:
    USING_PYDANTIC = True

    from typing import Any
    from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
    from pydantic.json_schema import JsonSchemaValue
    from pydantic_core import core_schema, CoreSchema

    from pydantic.dataclasses import dataclass

    class RIDFieldAnnotation:
        @classmethod
        def __get_pydantic_core_schema__(
            cls,
            _source_type: Any,
            _handler: GetCoreSchemaHandler
        ) -> CoreSchema:
            
            def validate_from_str(value: str) -> RID:
                result = RID.from_string(value)
                return result
            
            from_str_schema = core_schema.chain_schema(
                [
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(validate_from_str),
                ]
            )
            
            return core_schema.json_or_python_schema(
                json_schema=from_str_schema,
                python_schema=core_schema.union_schema(
                    [
                        core_schema.is_instance_schema(RID),
                        from_str_schema
                    ]
                ),
                serialization=core_schema.plain_serializer_function_ser_schema(
                    lambda instance: str(instance)
                )
            )
        
        @classmethod
        def __get_pydantic_json_schema__(
            cls, 
            _core_schema: CoreSchema, 
            handler: GetJsonSchemaHandler
        ) -> JsonSchemaValue:
            return handler(core_schema.str_schema())