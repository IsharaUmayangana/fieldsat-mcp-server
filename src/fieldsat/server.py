"""Build the MCP server: one FastMCP object with our tools, resources and prompts."""

from fastmcp import FastMCP

from . import __version__
from .domain.fields import (
    REGISTERED_FIELDS,
    FieldLookup,
    RegisteredField,
    find_registered_field,
)
from .providers.base import SatelliteEvidenceProvider, WeatherEvidenceProvider
from .tools import register_field_tools, register_weather_tools, register_satellite_tools
from .resources import register_resources
from .prompts import register_prompts


INSTRUCTIONS = (
    "Read-only field-level satellite and weather evidence for Sri Lankan agricultural fields. "
    "Call list_fields to find a field ID. Measurements describe the field; they do not "
    "diagnose a cause."
)


def create_server(
    satellite_provider: SatelliteEvidenceProvider,
    weather_provider: WeatherEvidenceProvider,
    fields: tuple[RegisteredField, ...] = REGISTERED_FIELDS,
    find_field: FieldLookup = find_registered_field,
) -> FastMCP:
    mcp = FastMCP(
        name="STEM Link Satellite MCP",
        instructions=INSTRUCTIONS,
        version=__version__,
    )

    # Tools, resources and prompts are registered here from step 01 onwards.
    register_field_tools(mcp, fields)
    register_weather_tools(mcp, weather_provider, find_field)
    register_satellite_tools(mcp, satellite_provider, find_field)
    register_resources(mcp, fields, find_field)
    register_prompts(mcp)
    return mcp