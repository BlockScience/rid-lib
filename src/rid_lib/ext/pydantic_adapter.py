from typing import Any, Annotated, Iterable
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema, CoreSchema
from rid_lib.core import RID, RIDType


class RIDFieldAnnotation:
    expected_types: tuple
    
    def __init__(self, expected_types: Iterable[RIDType | str] | None = None):
        if expected_types is None:
            self.expected_types = tuple()

        else:
            self.expected_types = tuple(
                RIDType.from_string(t) if isinstance(t, str) else t 
                for t in expected_types
            )
    
    def __get_pydantic_core_schema__(
        self,
        _source_type: Any,
        _handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        
        def validate_from_str(value: str) -> RID:
            # str -> RID validator
            rid = RID.from_string(value)
            if self.expected_types and type(rid) not in self.expected_types:
                raise ValueError(f"Expected RID of type one of {self.expected_types}, got {repr(type(rid))}")
            return rid
        
        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )
        
        return core_schema.json_or_python_schema(
            # str is valid type for JSON objects
            json_schema=from_str_schema, 
            # str or RID are valid types for Python dicts
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(RID),
                    from_str_schema
                ]
            ),
            # RIDs serialized with __str__ function
            serialization=core_schema.plain_serializer_function_ser_schema(str)
        )
    
    def __get_pydantic_json_schema__(
        self, 
        _core_schema: CoreSchema, 
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())
    

class RIDTypeFieldAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        
        def validate_from_str(value: str) -> RIDType:
            # str -> RID validator
            return RIDType.from_string(value)
        
        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )
        
        return core_schema.json_or_python_schema(
            # str is valid type for JSON objects
            json_schema=from_str_schema, 
            # str or RID are valid types for Python dicts
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(RIDType),
                    from_str_schema
                ]
            ),
            # RIDs serialized with __str__ function
            serialization=core_schema.plain_serializer_function_ser_schema(str)
        )
    
    @classmethod
    def __get_pydantic_json_schema__(
        cls, 
        _core_schema: CoreSchema, 
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())

# use these type aliases in place of RID and RIDType in Pydantic models

# usage: `Annotated[RID, allowed_types(SlackMessage, ...)]`
def allowed_types(*args) -> RIDFieldAnnotation:
    return RIDFieldAnnotation(args)

type RIDField = Annotated[RID, RIDFieldAnnotation()]
type RIDTypeField = Annotated[RIDType, RIDTypeFieldAnnotation]