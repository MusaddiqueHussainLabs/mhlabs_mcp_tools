import json
from typing import Dict, Any, Optional

class CustomJSONError(Exception):
    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message
        super().__init__(self.message)

    def to_json(self):
        if hasattr(self, 'error_code'):
            error_dict = {
                "succeeded": False,
                "error": {
                    "error_code": self.error_code,
                    "message": self.message
                }
            }
            return json.dumps(error_dict)
        else:
            result_dict = {
                "succeeded": True,
                "data": self.message
            }
            return json.dumps(result_dict)
        

def format_error_response(error_message: str, context: Optional[str] = None) -> str:
    """
    Format an error response for MCP tools.

    Args:
        error_message: The error message to display
        context: Optional context about when the error occurred

    Returns:
        Formatted error response
    """
    response_parts = ["##### ❌ Error\n"]

    if context:
        response_parts.append(f"**Context:** {context}")

    response_parts.append(f"**Error:** {error_message}")
    response_parts.append("")
    response_parts.append(
        "AGENT SUMMARY: An error occurred while processing the request."
    )

    return "\n".join(response_parts)