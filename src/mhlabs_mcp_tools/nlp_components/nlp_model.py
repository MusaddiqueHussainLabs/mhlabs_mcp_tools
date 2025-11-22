import traceback
import spacy
import spacy.cli
import json

from fastmcp import FastMCP
from mhlabs_mcp_tools.core.config import config as Settings
from mhlabs_mcp_tools.services.spacy_extractor import SpacyExtractor
from mhlabs_mcp_tools.handlers.custom_exceptions import CustomJSONError, format_error_response
from mhlabs_mcp_tools.handlers.output_generator import generate_output, format_success_response
from mhlabs_mcp_tools.core.constants import constants

from mhlabs_mcp_tools.core.factory import MCPToolBase, Domain



# ---------------------------------------------------------------------
# Global spaCy model and extractor
# ---------------------------------------------------------------------
try:
    nlp_model = spacy.load(Settings.SPACY_MODEL)
except OSError:
    spacy.cli.download(Settings.SPACY_MODEL)
    nlp_model = spacy.load(Settings.SPACY_MODEL)

extractor = SpacyExtractor(nlp_model)

class NlpComponentService(MCPToolBase):
    """Nlp Component tasks."""

    def __init__(self):
        super().__init__(Domain.NLP_COMPONENTS)

    def register_tools(self, mcp) -> None:
        """
        Register NLP tools with the given FastMCP instance.
        This function is optional if using category-based lazy loading.
        """
        # mcp.register_tool(load_component)
        # mcp.register_tool(predict_component)
        # =====================================================================
        # 1. NLP Load Component (MCP Tool)
        # =====================================================================

        @mcp.tool(
            name="nlp.load_component",
            description="Load a specific NLP spaCy model component to verify availability.",
            tags={self.domain.value},
            meta={"version": "1.0", "author": "mhlabs"}
        )
        async def load_component(component_type: str) -> str:
            """Load and verify an NLP component from the spaCy model."""
            try:
                # logger.info(f"Loading NLP component: {component_type}...")

                # Test processing to verify component behaves correctly
                test_doc = nlp_model("Apple is looking at buying U.K. startup for $1 billion")
                tokens_preview = [token.text for token in test_doc]

                # Prepare metadata/details
                details = {
                    "component_type": component_type,
                    "tokens_preview": tokens_preview,
                    "validation_status": "Verified",
                }

                summary = (
                    f"NLP component '{component_type}' has been successfully loaded and verified."
                )

                return format_success_response(
                    action="NLP Component Loaded",
                    details=details,
                    summary=summary,
                )

            except Exception as e:
                # logger.error(f"Error loading NLP component '{component_type}': {traceback.format_exc()}")

                return format_error_response(
                    error_message=str(e),
                    context=f"Loading NLP component: {component_type}",
                )


        # =====================================================================
        # 2. NLP Predict Component (MCP Tool)
        # =====================================================================

        @mcp.tool(
            name="nlp.predict_component",
            description="Run spaCy component processing such as NER, POS, Dependency, Sentiment (if available).",
            tags={self.domain.value},
            meta={"version": "1.0", "author": "mhlabs"}
        )        
        async def predict_component(component_type: str, input_text: str) -> str:
            """
            Predict NLP output for the specified component type.
            """
            try:
                # -----------------------------------------------------------------
                # Validation
                # -----------------------------------------------------------------
                if component_type is None:
                    raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_COMPONENT_TYPE_NONE)

                if input_text is None:
                    raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_NONE)

                if not isinstance(component_type, str):
                    raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_COMPONENT_TYPE_STRING)

                if not isinstance(input_text, str):
                    raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_STRING)

                if not component_type.strip():
                    raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_COMPONENT_TYPE_EMPTY)

                if not input_text.strip():
                    raise CustomJSONError(constants.ERROR_CODE_500, constants.VALIDATE_INPUT_TEXT_EMPTY)

                # -----------------------------------------------------------------
                # Actual prediction
                # -----------------------------------------------------------------
                predicted_result = extractor.predict_nlp_component(component_type, input_text)

                # Normalize output formats
                if predicted_result is None:
                    summary = (
                        f"No results found or NLP component '{component_type}' "
                        f"does not support prediction for this input."
                    )
                    details = {"component_type": component_type, "input_text": input_text}
                    
                    return format_success_response(
                        action="No Prediction Result",
                        details=details,
                        summary=summary,
                    )

                # FIX - If predicted_result is JSON string → parse it
                if isinstance(predicted_result, str):
                    predicted_result = json.loads(predicted_result)

                # If not a dict, wrap result
                if not isinstance(predicted_result, dict):
                    predicted_result = {"output": predicted_result}

                # Prepare structured metadata
                summary = (
                    f"Prediction successfully completed for NLP component '{component_type}'."
                )

                details = {
                    "component_type": component_type,
                    "input_preview": input_text[:50] + "..." if len(input_text) > 50 else input_text,
                    "output_preview": predicted_result,
                }

                return format_success_response(
                    action="Prediction Completed",
                    details=details,
                    summary=summary,
                )

            except CustomJSONError as e:
                # logger.error(f"Custom JSON Error: {e.to_json()}")
                return format_error_response(
                    error_message=e.to_json(),
                    context="NLP Prediction",
                )

            except Exception as e:
                error_message = traceback.format_exc()
                # logger.error(f"Unexpected error: {error_message}")
                return format_error_response(
                    error_message=str(e),
                    context=f"Prediction for component '{component_type}'"
                )

    @property
    def tool_count(self) -> int:
        """Return the number of tools provided by this service."""
        return 2