# 🧠 mhlabs-mcp-tools

`mhlabs-mcp-tools` is a **Modular MCP Tools Server** built using [FastMCP](https://github.com/fastmcp/fastmcp).  
It provides an **extendable AI tool ecosystem** organized into functional categories (Text Preprocessing, NLP Components, Document Analysis, etc.) that can be dynamically loaded and served through **MCP (Model Context Protocol)** via **STDIO transport**.

This project is part of the **MHLabs AI Agentic Ecosystem**, designed to work with `mhlabs-mcp-server`, `mhlabs-mcp-agents`, and downstream A2A agent frameworks.

---

## Features

- **FastMCP Server**: Pure FastMCP implementation supporting multiple transport protocols
- **Factory Pattern**: Reusable MCP tools factory for easy service management
- **Domain-Based Organization**: Services organized by business domains (HR, Tech Support, etc.)
- **Authentication**: Optional Azure AD authentication support
- **Multiple Transports**: STDIO, HTTP (Streamable), and SSE transport support
- **VS Code Integration**: Debug configurations and development settings
- **Comprehensive Testing**: Unit tests with pytest
- **Flexible Configuration**: Environment-based configuration management

## Architecture

```
mhlabs_mcp_tools/
├── .gitignore
├── .vscode/
│   └── settings.json
├── CHANGELOG.md
├── LICENSE
├── README.md
├── docs/
│   └── index.md
├── examples/
│   ├── example_client.py
│   └── example_client_http.py
├── mkdocs.yml
├── pyproject.toml
├── requirements.txt
├── server.json
└── src/
    ├── __init__.py
    ├── main.py
    └── mhlabs_mcp_tools/
        ├── __init__.py
        ├── core/
        │   ├── __init__.py
        │   ├── config.py
        │   ├── constants.py
        │   ├── factory.py
        │   └── prompts.py
        ├── data/
        │   ├── __init__.py
        │   ├── external/
        │   │   └── __init__.py
        │   ├── interim/
        │   │   └── __init__.py
        │   ├── processed/
        │   │   └── __init__.py
        │   └── raw/
        │       ├── __init__.py
        │       ├── contractions_dict.json
        │       ├── custom_substitutions.csv
        │       ├── leftovers_dict.json
        │       └── slang_dict.json
        ├── handlers/
        │   ├── __init__.py
        │   ├── custom_exceptions.py
        │   └── output_generator.py
        ├── mcp_server.py
        ├── models/
        │   └── __init__.py
        ├── nlp_components/
        │   ├── __init__.py
        │   └── nlp_model.py
        ├── services/
        │   ├── __init__.py
        │   ├── langchain_framework.py
        │   └── spacy_extractor.py
        └── text_preprocessing/
            ├── __init__.py
            ├── contractions.py
            ├── emo_unicode.py
            ├── slang_text.py
            └── text_preprocessing.py
```

## Available Services

Currently the package is organized into three primary modules:

### 1. NLP Components

| Component Type | Description                 |
|----------------|-----------------------------|
| tokenize       | Text tokenization           |
| pos            | Part-of-Speech tagging      |
| lemma          | Word lemmatization          |
| morphology     | Study of word forms         |
| dep            | Dependency parsing          |
| ner            | Named Entity Recognition    |
| norm           | Text normalization          |

### 2. Text Preprocessing

This module equips users with an extensive set of text preprocessing tools:

| Function                      | Description                                          |
|-------------------------------|------------------------------------------------------|
| to_lower                      | Convert text to lowercase                             |
| to_upper                      | Convert text to uppercase                             |
| remove_number                 | Remove numerical characters                           |
| remove_itemized_bullet_and_numbering | Eliminate itemized/bullet-point numbering |
| remove_url                    | Remove URLs from text                                 |
| remove_punctuation            | Remove punctuation marks                              |
| remove_special_character      | Remove special characters                             |
| keep_alpha_numeric            | Keep only alphanumeric characters                     |
| remove_whitespace             | Remove excess whitespace                              |
| normalize_unicode             | Normalize Unicode characters                          |
| remove_stopword               | Eliminate common stopwords                            |
| remove_freqwords              | Remove frequently occurring words                      |
| remove_rarewords              | Remove rare words                                     |
| remove_email                  | Remove email addresses                                |
| remove_phone_number           | Remove phone numbers                                  |
| remove_ssn                    | Remove Social Security Numbers (SSN)                  |
| remove_credit_card_number     | Remove credit card numbers                            |
| remove_emoji                  | Remove emojis                                         |
| remove_emoticons              | Remove emoticons                                      |
| convert_emoticons_to_words    | Convert emoticons to words                            |
| convert_emojis_to_words       | Convert emojis to words                               |
| remove_html                   | Remove HTML tags                                      |
| chat_words_conversion         | Convert chat language to standard English              |
| expand_contraction            | Expand contractions (e.g., "can't" to "cannot")        |
| tokenize_word                 | Tokenize words                                        |
| tokenize_sentence             | Tokenize sentences                                    |
| stem_word                     | Stem words                                            |
| lemmatize_word                | Lemmatize words                                       |
| preprocess_text               | Combine multiple preprocessing steps into one function|

## Quick Start

### Development Setup

1. **Clone and Navigate**:

   ```bash
   cd src/mhlabs_mcp_tools
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start the Server**:

   ```bash
   # Default STDIO transport (for local MCP clients)
   python mcp_server.py

   # HTTP transport (for web-based clients)
   python mcp_server.py --transport http --port 9000
   or
   after installed mhlabs-mcp-tools
   python -m mhlabs_mcp_tools.mcp_server --transport http --port 9000

   # Using FastMCP CLI (recommended)
   fastmcp run mcp_server.py -t streamable-http --port 9000 -l DEBUG

   # Debug mode with authentication disabled
   python mcp_server.py --transport http --debug --no-auth
   ```

### Transport Options

**1. STDIO Transport (default)**

- 🔧 Perfect for: Local tools, command-line integrations, Claude Desktop
- 🚀 Usage: `python mcp_server.py` or `python mcp_server.py --transport stdio`

**2. HTTP (Streamable) Transport**

- 🌐 Perfect for: Web-based deployments, microservices, remote access
- 🚀 Usage: `python mcp_server.py --transport http --port 9000`
- 🌐 URL: `http://127.0.0.1:9000/mcp/`

**3. SSE Transport (deprecated)**

- ⚠️ Legacy support only - use HTTP transport for new projects
- 🚀 Usage: `python mcp_server.py --transport sse --port 9000`

### FastMCP CLI Usage

```bash
# Standard HTTP server
fastmcp run mcp_server.py -t streamable-http --port 9000 -l DEBUG

# With custom host
fastmcp run mcp_server.py -t streamable-http --host 0.0.0.0 --port 9000 -l DEBUG

# STDIO transport (for local clients)
fastmcp run mcp_server.py -t stdio

# Development mode with MCP Inspector
fastmcp dev mcp_server.py -t streamable-http --port 9000
```

### VS Code Development

1. **Open in VS Code**:

   ```bash
   code .
   ```

2. **Use Debug Configurations**:
   - `Debug MCP Server (STDIO)`: Run with STDIO transport
   - `Debug MCP Server (HTTP)`: Run with HTTP transport
   - `Debug Tests`: Run the test suite

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Server Settings
MCP_HOST=0.0.0.0
MCP_PORT=9000
MCP_DEBUG=false
MCP_SERVER_NAME=MHLABS MCP Server

# Authentication Settings
MCP_ENABLE_AUTH=true
AZURE_TENANT_ID=your-tenant-id-here
AZURE_CLIENT_ID=your-client-id-here
AZURE_JWKS_URI=https://login.microsoftonline.com/your-tenant-id/discovery/v2.0/keys
AZURE_ISSUER=https://sts.windows.net/your-tenant-id/
AZURE_AUDIENCE=api://your-client-id
```

### Authentication

When `MCP_ENABLE_AUTH=true`, the server expects Azure AD Bearer tokens. Configure your Azure App Registration with the appropriate settings.

For development, set `MCP_ENABLE_AUTH=false` to disable authentication.

## Adding New Services

1. **Create Service Class**:

   ```python
   from core.factory import MCPToolBase, Domain

   class MyService(MCPToolBase):
       def __init__(self):
           super().__init__(Domain.MY_DOMAIN)

       def register_tools(self, mcp):
           @mcp.tool(tags={self.domain.value})
           async def my_tool(param: str) -> str:
               # Tool implementation
               pass

       @property
       def tool_count(self) -> int:
           return 1  # Number of tools
   ```

2. **Register in Server**:

   ```python
   # In mcp_server.py (gets registered automatically from services/ directory)
   factory.register_service(MyService())
   ```

3. **Add Domain** (if new):
   ```python
   # In core/factory.py
   class Domain(Enum):
       # ... existing domains
       MY_DOMAIN = "my_domain"
   ```

## MCP Client Usage

### Python Client

```python
import asyncio
from fastmcp import Client

client = Client("http://localhost:9000/mcp")

async def main():
    async with client:
        tools = await client.list_tools()
        # tools -> list[mcp.types.Tool]
        # print(tools)
        for tool in tools:
            print(f"Tool: {tool.name}")
        
        result = await client.call_tool("textprep.expand_contraction", {"input_text": "The must've SSN is 859-98-0987. The employee's phone number is 555-555-5555."})
        print("Result:", result)

asyncio.run(main())
```

### Command Line Testing

```bash
# Test the server is running
curl http://localhost:9000/mcp/

# With FastMCP CLI for testing
fastmcp dev mcp_server.py -t streamable-http --port 9000
```

## Quick Test

**Test STDIO Transport:**

```bash
# Start server in STDIO mode
python mcp_server.py --debug --no-auth

# Test with client_example.py
python client_example.py
```

**Test HTTP Transport:**

```bash
# Start HTTP server
python mcp_server.py --transport http --port 9000 --debug --no-auth

# Test with FastMCP client
python -c "
from fastmcp import Client
import asyncio
async def test():
    async with Client('http://localhost:9000/mcp') as client:
        result = await client.call_tool("textprep.expand_contraction", {"input_text": "The must've SSN is 859-98-0987. The employee's phone number is 555-555-5555."})
        print(result)
asyncio.run(test())
"
```

**Test with FastMCP CLI:**

```bash
# Start with FastMCP CLI
fastmcp run mcp_server.py -t streamable-http --port 9000 -l DEBUG

# Server will be available at: http://127.0.0.1:9000/mcp/
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're in the correct directory and dependencies are installed
2. **Authentication Errors**: Check your Azure AD configuration and tokens
3. **Port Conflicts**: Change the port in configuration if 9000 is already in use
4. **Missing fastmcp**: Install with `pip install fastmcp`

### Debug Mode

Enable debug mode for detailed logging:

```bash
python mcp_server.py --debug --no-auth
```

Or set in environment:

```env
MCP_DEBUG=true
```

## Server Arguments

```bash
usage: mcp_server.py [-h] [--transport {stdio,http,streamable-http,sse}]
                     [--host HOST] [--port PORT] [--debug] [--no-auth]

MHLABS MCP Server

options:
  -h, --help            show this help message and exit
  --transport, -t       Transport protocol (default: stdio)
  --host HOST           Host to bind to for HTTP transport (default: 127.0.0.1)
  --port, -p PORT       Port to bind to for HTTP transport (default: 9000)
  --debug               Enable debug mode
  --no-auth             Disable authentication
```

---

## 📄 License

MIT License © 2025 [MusaddiqueHussain Labs](https://github.com/MusaddiqueHussainLabs)

---

## 🤝 Contributing

1. Follow the existing code structure and patterns
2. Add tests for new functionality
3. Update documentation for new features
4. Use the provided VS Code configurations for development

---

## 🧠 Learn More

* **MCP Protocol**: [https://modelcontextprotocol.io](https://modelcontextprotocol.io)
* **FastMCP GitHub**: [https://github.com/fastmcp/fastmcp](https://github.com/fastmcp/fastmcp)
* **LangGraph Integration Guide** (coming soon)

---

### 💡 Tip

If you want to embed `mhlabs-mcp-tools` into a larger MCP-based orchestrator:

```python
from fastmcp import StdioServerParameters
server_params = StdioServerParameters(
    command="python",
    args=["-m", "mhlabs_mcp_tools.server"],
    //env={"MHLABS_MCP_CATEGORY": "textprep,nlp"}
)
```

---

**Developed with ❤️ by [MusaddiqueHussain Labs](https://github.com/MusaddiqueHussainLabs)**
