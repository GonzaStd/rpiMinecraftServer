from types import UnionType
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined
from typing import Any, get_origin, Union, get_args


class PydanticFather(BaseModel):
    @classmethod
    def get_defaults(cls) -> dict[str, Any]:
        defaults: dict[str, Any] = {}
        for name, info in cls.model_fields.items():
            defaults[name] = cls.get_field_default(info)
        return defaults

    @classmethod
    def get_field_default(cls, field_info: FieldInfo) -> Any:
        if field_info.default_factory not in (PydanticUndefined, None):
            return field_info.default_factory

        if field_info.default not in (PydanticUndefined, None):
            return field_info.default

        # At this point the field seems to be another schema_class
        nested_schema = cls.get_nested_schema(field_info.annotation) # Passes the type hint
        if nested_schema is not None:
            return nested_schema.get_defaults()

        return None # There is no default value and it isn't another schema

    @staticmethod
    def get_nested_schema(annotation: type | None) -> type["PydanticFather"] | None:
        if isinstance(annotation, type) and issubclass(annotation, PydanticFather):
            # If type hint (annotation) is a type based on PydanticChild `type[PydanticChild]`
            return annotation # return the schema that inherited PydanticChild

        origin = get_origin(annotation) # ORIGIN is the father type hint.
                                        # Type hint: `ORIGIN[arg, arg]`
        unions = (Union, UnionType) # Union[member, member] or member | member

        if origin in unions: # If origin is a union
            for member in get_args(annotation): # ORIGIN[arg, arg], member = arg
                if member is type(None):
                    continue
                if isinstance(member, type) and issubclass(member, PydanticFather):
                    return member

        # We are only searching for PydanticChild inherited classes.
        return None