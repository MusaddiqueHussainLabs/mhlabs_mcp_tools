import json
import traceback
import logging
# from handlers.logger_config import configure_logger
from handlers.custom_exceptions import CustomJSONError
from handlers.output_generator import generate_output

from mhlabs_mcp_tools.nlp_components import register_tools
from mhlabs_mcp_tools.text_preprocessing import preprocess_text, preprocess_operations
# from musaddiquehussainlabs.text_preprocessing import to_lower, remove_email, remove_url, remove_punctuation, lemmatize_word

from mhlabs_mcp_tools.document_analysis import DocumentAnalysis

logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

# logger.disabled = True

def process_data(data):
    try:
        if not isinstance(data, dict):
            raise CustomJSONError(400, "Invalid data format. Expecting a dictionary.")

        # Processing the data (dummy example: adding a prefix to each value)
        logger.info("processed_data started...")
        processed_data = {key: f"Processed: {value}" for key, value in data.items()}
        logger.info("processed_data ended...")
        return generate_output(True, data=processed_data)
    
    except CustomJSONError as e:
        logger.error(f"Custom JSON Error: {e.to_json()}")
        return e.to_json()
    
    except Exception as e:
        error_message = traceback.format_exc()
        logger.error(f"Unexpected error: {error_message}")
        return generate_output(False, error_code=500, message="Unexpected error occurred. Check logs for details.")

# Example usage with dictionary data
if __name__ == "__main__":
    input_data = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3"
    }

    data_to_process = """The employee's SSN is 859-98-0987. The employee's phone number is 555-555-5555."""

    # output = process_data(input_data)
    # print("Output:", output)
    # nlp = nlp()
    # result = nlp.predict(component_type="ner", input_text=data_to_process)
    # print(result)

    # text_to_process = ""
    # preprocessed_text = preprocess_text(data_to_process)
    # print(preprocessed_text)

    # preprocess_functions = [preprocess_operations.expand_contraction]
    # preprocessed_text = preprocess_text(data_to_process, preprocess_functions)
    # print(preprocessed_text)

    document_analysis = DocumentAnalysis()
    # result = document_analysis.full_analysis(data_to_process)
    result = document_analysis.pii_anonymization(data_to_process)
    print(result)
