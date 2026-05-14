from pydantic import BaseModel, ConfigDict


class DTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
    )
