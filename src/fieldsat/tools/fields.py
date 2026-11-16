from fastmcp import FastMCP
from pydantic import BaseModel
from mcp.types import ToolAnnotations

from fieldsat.domain.fields import RegisteredField, Crop


class FieldSummary(BaseModel):
    id: str
    name: str
    crop: Crop


class FieldList(BaseModel):
    fields: list[FieldSummary]



def register_field_tools(mcp: FastMCP, fields: tuple[RegisteredField, ...]) -> None:

    @mcp.tool(
        name="list_fields",
        title="List registered fields",
        annotations=ToolAnnotations(read_only_hint=True, open_world_hint=True)
    )
    def list_fields() -> FieldList:
        return FieldList(
            fields=[FieldSummary(
                id=field.id,
                name=field.name,
                crop=field.crop
            )
                for field in fields]
        )