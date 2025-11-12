# mhlabs-mcp-tools

mcp-name: io.github.MusaddiqueHussainLabs/mhlabs_mcp_tools

```markdown
# 🧠 mhlabs-mcp-tools

`mhlabs-mcp-tools` is a **Modular MCP Tools Server** built using [FastMCP](https://github.com/fastmcp/fastmcp).  
It provides an **extendable AI tool ecosystem** organized into functional categories (Text Preprocessing, NLP Components, Document Analysis, etc.) that can be dynamically loaded and served through **MCP (Model Context Protocol)** via **STDIO transport**.

This project is part of the **MHLabs AI Agentic Ecosystem**, designed to work with `mhlabs-mcp-server`, `mhlabs-mcp-agents`, and downstream A2A agent frameworks.

---

## 🚀 Key Features

- 🧩 **Category-based modular loading** — Load only desired tool categories (e.g., `textprep`, `nlp`, `document`).
- 🔍 **Automatic tool discovery** using `@mcp.tool` decorators.
- 📦 **Plug-and-play MCP tools** (standardized schema, metadata, versioning).
- 🧠 **Compositional tools** — Higher-level tools can invoke other MCP tools (e.g., `textprep.preprocess_text`).
- ⚙️ **STDIO transport** for integration with MCP-compatible clients.
- 🧾 **Rich metadata and tagging** for each tool (name, description, tags, version, author).
- 🧑‍💻 **Developer-friendly structure** to add or extend tools easily.

---

## ⚙️ Installation

```bash
# Clone and install locally
git clone https://github.com/YourOrg/mhlabs-mcp-tools.git
cd mhlabs-mcp-tools

# Create environment and install dependencies
python -m venv .venv
source .venv/bin/activate

pip install -e .
````

Or directly from PyPI (once published):

```bash
pip install mhlabs-mcp-tools
```

---

## 🧭 Quick Start (STDIO MCP Server)

Start the MCP server:

```bash
//export MHLABS_MCP_CATEGORY="textprep,nlp"
python -m mhlabs_mcp_tools.server
```

The server will:

* Initialize a shared `FastMCP` instance.
* Import and register tools from selected categories.
* Run as a **STDIO-based MCP service** (stdin/stdout communication).

### Example Output

```
Starting mhlabs-mcp-tools with categories: ['textprep', 'nlp']
✅ Loaded 24 tools (15 textprep, 9 nlp)
🚀 Running FastMCP STDIO server...
```

---

## 🧪 Example Client (Quick Test)

You can test your tools using the provided MCP client:

```python
# examples/example_client.py
from fastmcp import StdioClient, StdioServerParameters

server_params = StdioServerParameters(
    command="python",
    args=["-m", "mhlabs_mcp_tools.server"],
    //env={"MHLABS_MCP_CATEGORY": "textprep,nlp"}
)

client = StdioClient(server_params)
result = client.call_tool("textprep.remove_email", {"input_text": "Contact me at test@mail.com"})
print(result)
```

Run:

```bash
python examples/example_client.py
```

---

## 🧩 Example Tool Definitions

Each tool is declared using the `@mcp.tool` decorator and registered automatically at runtime.

### Example 1 — Basic Tool

```python
from fastmcp import tool
from .server import mcp
import re

@mcp.tool(
    name="textprep.remove_email",
    description="Remove email addresses from text.",
    tags={"textprep", "pii"},
    meta={"version": "0.1", "author": "mhlabs"}
)
def remove_email(input_text: str) -> dict:
    """Remove email addresses."""
    cleaned = re.sub(r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}', '', input_text)
    return {"succeeded": True, "data": cleaned}
```
---

## 🧠 Architecture Overview

### 1️⃣ Server Entry (`server.py`)

* Creates a single shared `FastMCP` instance.
* Loads category modules dynamically based on environment variables.
* Exposes STDIO transport for LLMs or other MCP clients.

### 2️⃣ Category Registries (`text_prep.registry`, etc.)

* Each category defines its own `registry.py` that imports tool functions.
* When imported, all decorated `@mcp.tool` functions self-register with the shared MCP instance.

### 3️⃣ Tools

* Lightweight functions with explicit metadata.
* Always return **dict-based responses** for schema safety.
* Grouped by domain for clarity.

---

## 🔧 Configurable Environment Variables

| Variable              | Description                                     | Example              |
| --------------------- | ----------------------------------------------- | -------------------- |
| `MHLABS_MCP_CATEGORY` | Comma-separated list of tool categories to load | `"textprep,nlp"`     |
| `MHLABS_MCP_NAME`     | Custom server name                              | `"mhlabs-mcp-tools"` |
| `MHLABS_LOG_LEVEL`    | Logging level                                   | `"DEBUG"`            |

---

## 🧰 Adding New Tools

1. Create a submodule folder under `src/mhlabs_mcp_tools/` (e.g., `image_analysis/`).
2. Add your functions in `functions.py`.
3. Decorate each function with `@mcp.tool(...)`.
4. Create a `registry.py` that imports `functions.py`.
5. Add your module path to `CATEGORY_MODULES` in `server.py`.

Example:

```python
CATEGORY_MODULES = {
    "textprep": "mhlabs_mcp_tools.text_prep.registry",
    "nlp": "mhlabs_mcp_tools.nlp_components.registry",
    "document": "mhlabs_mcp_tools.document.registry",
    "image": "mhlabs_mcp_tools.image_analysis.registry",
}
```

---

## 📜 Error Handling & Schema Rules

* All MCP tools must **return a dict** — never a JSON string.
* Typical return structure:

  ```python
  return {"succeeded": True, "data": "..."}
  ```
* Avoid returning non-serializable Python objects (e.g., custom classes).
* Set `arbitrary_types_allowed=True` in Pydantic models if using complex types.

---

## 🧩 Integration with A2A Agents (Future)

In future phases, `mhlabs-mcp-tools` will integrate seamlessly with:

* **A2A (Agent-to-Agent) frameworks** through `mhlabs-mcp-agents`
* **Agentic pipelines** orchestrated via LangGraph or Autogen
* **Dynamic tool registration** for runtime capability expansion

---

## 🧑‍💻 Development

Run tests:

```bash
pytest -v
```

Linting:

```bash
ruff check src/
```

Build and publish:

```bash
python -m build
twine upload dist/*
```

---

## 📄 License

MIT License © 2025 [MusaddiqueHussain Labs](https://github.com/MusaddiqueHussainLabs)

---

## 🤝 Contributing

Pull requests are welcome!
Please follow our contribution guide and code style conventions.

---

## 🪄 Example Use Cases

| Category     | Tool                    | Description                      |
| ------------ | ----------------------- | -------------------------------- |
| **textprep** | `remove_email`          | Strip emails from raw text       |
| **textprep** | `preprocess_text`       | Execute multi-step text cleanup  |
| **nlp**      | `nlp.predict_component` | Named entity recognition (spaCy) |
| **document** | `extract_metadata`      | Extract document metadata        |

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

**Developed with ❤️ by [Musaddique Hussain Labs](https://github.com/MusaddiqueHussainLabs)**

```
