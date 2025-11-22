# from dataclasses import dataclass
# import os

# @dataclass
# class Settings:

#     LOG_FILE_PATH : str=os.path.join('app.log')
#     LOG_FILE_FORMAT: str='%(asctime)s - %(name)s - %(levelname)s - %(message)s'

#     SPACY_MODEL: str='en_core_web_lg'

#     _CUSTOM_SUB_CSV_FILE_PATH : str=os.path.join('data\\raw',"custom_substitutions.csv")

# settings = Settings()

"""
Configuration settings for the MCP server.
"""

import os
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings


class MCPServerConfig(BaseSettings):
    """MCP Server configuration."""
    
    # Server settings
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=9000)
    debug: bool = Field(default=False)

    # Authentication settings
    tenant_id: Optional[str] = Field(default=None)
    client_id: Optional[str] = Field(default=None)
    jwks_uri: Optional[str] = Field(default=None)
    issuer: Optional[str] = Field(default=None)
    audience: Optional[str] = Field(default=None)

    # MCP specific settings
    server_name: str = Field(default="MhlabsMcpServer")
    enable_auth: bool = Field(default=False)
    
    # Dataset path - added to handle the environment variable
    dataset_path: str = Field(default="./datasets")
    _CUSTOM_SUB_CSV_FILE_PATH : str=os.path.join('data\\raw',"custom_substitutions.csv")

    # Logging settings
    LOG_FILE_PATH : str=os.path.join('app.log')
    LOG_FILE_FORMAT: str='%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # NLP settings
    SPACY_MODEL: str='en_core_web_lg'


# Global configuration instance
config = MCPServerConfig()


def get_auth_config():
    """Get authentication configuration for Azure."""
    if not config.enable_auth:
        return None

    return {
        "tenant_id": config.tenant_id,
        "client_id": config.client_id,
        "jwks_uri": config.jwks_uri,
        "issuer": config.issuer,
        "audience": config.audience,
    }


def get_server_config():
    """Get server configuration."""
    return {"host": config.host, "port": config.port, "debug": config.debug}