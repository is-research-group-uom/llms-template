# LLMs Template - Greek Document Processing with Multiple Language Models

## Overview of Repository

This repository provides a comprehensive template for processing Greek PDF documents using multiple Large Language Models (LLMs) through AWS Bedrock. The primary purpose is to extract and analyze structured information from Greek hiring and employment decision documents, leveraging various state-of-the-art language models to perform text analysis and data extraction.

The system is specifically designed to handle Greek text with proper character encoding and correction, making it suitable for processing official government documents, hiring decisions, and other Greek-language PDFs that require structured data extraction.

## Detailed Description of Contents

### Directories

#### `.idea`
Contains IDE configuration files (primarily for PyCharm or IntelliJ IDEA). These files store project-specific settings, code style preferences, and debugging configurations.

#### `__pycache__`
Contains compiled Python bytecode files (`.pyc`) that are automatically generated when Python modules are imported. This improves performance by avoiding recompilation of unchanged modules.

#### `data`
Contains sample PDF files used for testing and demonstration purposes. These are primarily Greek documents related to:
- Hiring decisions (`diorismos_*.pdf`)
- Employment assignments (`proslipsi_*.pdf`, `anaplhrwtes_*.pdf`)
- Position placements (`topothethisi_*.pdf`, `topothetisi_*.pdf`)
- Summary documents (`perilipsi_*.pdf`)

#### `llms`
Contains individual modules for different Large Language Models, each implementing specific model interfaces and prompting strategies:
- `claude3_5.py` - Claude 3.5 Sonnet model
- `claude3_7.py` - Claude 3.7 Sonnet model
- `claude4_sonnet.py` - Claude 4 Sonnet model
- `deepseek.py` - DeepSeek R1 model
- `llama.py` - Llama model
- `pixtral.py` - Pixtral model (for multimodal tasks)

### Key Files

#### `credentials.py`
Manages AWS credentials and client configuration for accessing AWS Bedrock services. Contains:
- AWS credentials dictionary with access keys and region configuration
- `get_bedrock_client()` function for creating authenticated Bedrock runtime clients
- `get_credentials()` function for retrieving credential information

#### `main.py`
The main entry point script that orchestrates the entire document processing workflow:
- Extracts text and data from PDF files using the parser
- Provides interactive model selection interface
- Processes documents through selected LLM models
- Saves model responses to output files
- Supports multiple model execution in sequence

#### `test_new_parser.py`
Specialized PDF parsing script optimized for Greek text extraction and cleaning:
- Converts PDFs to Markdown format using pymupdf4llm
- Implements Greek text correction algorithms
- Extracts structured data from tables
- Handles various document formats and layouts
- Provides robust error handling for PDF processing

## Setup Guide

### Prerequisites
- Python 3.7 or higher
- AWS account with Bedrock access
- Required Python packages:
  ```bash
  pip install pymupdf4llm boto3 botocore
  ```

### Setting up AWS Credentials

1. **Configure AWS Credentials in `credentials.py`:**
   ```python
   AWS_CREDENTIALS = {
       'aws_access_key_id': 'YOUR_ACCESS_KEY_ID',
       'aws_secret_access_key': 'YOUR_SECRET_ACCESS_KEY',
       'aws_session_token': 'YOUR_SESSION_TOKEN',  # Optional for temporary credentials
       'region_name': 'us-east-1'
   }
   ```

2. **AWS Bedrock Setup:**
   - Ensure you have access to AWS Bedrock service
   - Request access to the required model families (Claude, Llama, DeepSeek)
   - Verify your AWS region supports the models you want to use

3. **Create outputs directory:**
   ```bash
   mkdir pythonProject1/outputs
   ```

## Language Models

The repository supports multiple state-of-the-art language models through AWS Bedrock:

### Claude Models
- **Claude 3.5 Sonnet**: Balanced performance and efficiency, excellent for structured data extraction
- **Claude 3.7 Sonnet**: Latest version with improved reasoning capabilities
- **Claude 4 Sonnet**: Advanced model with superior understanding of complex documents

### Llama
- **Llama**: Meta's large language model, optimized for instruction following and text analysis

### DeepSeek
- **DeepSeek R1**: Reasoning-focused model with strong analytical capabilities

### Pixtral
- **Pixtral Large**: Multimodal model capable of processing both text and images

Each model is configured with specific parameters optimized for Greek text processing and structured data extraction tasks.

## Usage Instructions

### Using the Main Script (`main.py`)

1. **Navigate to the project directory:**
   ```bash
   cd pythonProject1
   ```

2. **Run the main script:**
   ```bash
   python main.py
   ```

3. **Follow the interactive prompts:**
   - The script will automatically extract data from the default PDF
   - Select your preferred model by typing: `claude3.7`, `claude3.5`, `claude4`, `llama`, or `deepseek`
   - Choose whether to process with additional models
   - Results will be saved in the `outputs/` directory

### Using the PDF Parser (`test_new_parser.py`)

The parser can be used independently for text extraction:

```python
from test_new_parser import extract_data_from_pdf

# Extract data from a PDF file
pdf_path = "data/your_document.pdf"
first_paragraph, data = extract_data_from_pdf(pdf_path)

print("Introductory text:", first_paragraph)
print("Extracted data:", data)
```

## Key Functions Explanation

### `credentials.py` Functions

#### `get_bedrock_client()`
```python
def get_bedrock_client():
    """
    Returns a configured boto3 bedrock-runtime client using the stored credentials.
    
    Returns:
        boto3.client: Configured bedrock-runtime client
    """
    import boto3
    return boto3.client('bedrock-runtime', **AWS_CREDENTIALS)
```
Creates and returns an authenticated AWS Bedrock client using the configured credentials.

#### `get_credentials()`
```python
def get_credentials():
    """
    Returns the AWS credentials dictionary.
    
    Returns:
        dict: AWS credentials
    """
    return AWS_CREDENTIALS.copy()
```
Provides access to the AWS credentials configuration.

### `test_new_parser.py` Functions

#### `_clean_greek_text(text: str) -> str`
```python
def _clean_greek_text(text: str) -> str:
    """
    Corrects common character mapping errors in Greek text extracted from PDFs.
    """
    correction_map = {
        'ΣΣ': 'ΣΤ',
        'Σσ': 'Τσ',
        '΢': 'Σ',
        'ΟΤ': 'ΟΥ',
        'ΕΤ': 'ΕΥ',
        # ... additional mappings
    }
    
    for wrong, right in correction_map.items():
        text = text.replace(wrong, right)
    
    return text
```
Corrects common OCR errors and character encoding issues specific to Greek text.

#### `extract_data_from_pdf(pdf_path: str)`
```python
def extract_data_from_pdf(pdf_path: str):
    """
    Extracts introductory text and all tables from a PDF file.
    
    Args:
        pdf_path (str): The path to the PDF file.
        
    Returns:
        tuple: (intro_text, all_tables_data)
    """
    # Convert PDF to Markdown
    md_text = pymupdf4llm.to_markdown(pdf_path)
    md_text = _clean_greek_text(md_text)
    
    # Extract introductory text and tables
    # ... processing logic
    
    return intro_text, data
```
Main function for extracting structured data from Greek PDF documents.

## Examples

### Example 1: Basic Usage
```python
from test_new_parser import extract_data_from_pdf
from llms.claude3_5 import claude3_5

# Extract data from PDF
pdf_path = "data/diorismos.pdf"
intro_text, extracted_data = extract_data_from_pdf(pdf_path)

# Process with Claude 3.5
response = claude3_5(intro_text, extracted_data[2:16])

# Save results
with open("outputs/claude3_5_results.txt", "w", encoding="utf-8") as f:
    f.write(response)
```

### Example 2: Multiple Model Processing
```python
from llms.claude3_5 import claude3_5
from llms.deepseek import deepseek
from llms.llama import llama

# Extract data
intro_text, data = extract_data_from_pdf("data/proslipsi_anaplhrwtwn.pdf")

# Process with multiple models
models = {
    'claude3.5': claude3_5,
    'deepseek': deepseek,
    'llama': llama
}

for model_name, model_func in models.items():
    response = model_func(intro_text, data[2:16])
    
    with open(f"outputs/{model_name}_results.txt", "w", encoding="utf-8") as f:
        f.write(response)
    
    print(f"{model_name} processing complete")
```

### Example 3: Custom PDF Processing
```python
# Process a custom PDF with specific requirements
def process_custom_pdf(pdf_path, model_choice='claude3.5'):
    try:
        # Extract text and data
        intro_text, data = extract_data_from_pdf(pdf_path)
        
        if not intro_text.strip():
            print("Warning: No text extracted. PDF might be image-based.")
            return None
        
        # Select model
        if model_choice == 'claude3.5':
            from llms.claude3_5 import claude3_5
            response = claude3_5(intro_text, data)
        elif model_choice == 'deepseek':
            from llms.deepseek import deepseek
            response = deepseek(intro_text, data)
        
        return response
        
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

# Usage
result = process_custom_pdf("data/your_document.pdf", "claude3.5")
```

## Code Snippets

### Model Selection Logic from `main.py`
```python
print("Select the model you want by typing: 'claude3.7', 'claude3.5', 'claude4', 'llama', or 'deepseek'.")
valid_models = ['claude3.7', 'claude3.5', 'claude4', 'llama', 'deepseek']
model = input()

while model not in valid_models:
    print("Invalid model. Please type again: 'claude3.7', 'claude3.5', 'claude4', 'llama', or 'deepseek'.")
    model = input()

if model == 'claude3.7':
    claude3_7_response = claude3_7(first_paragraph, data[2:16])
    with open("outputs/claude3_7.txt", "w", encoding="utf-8") as f:
        f.write(claude3_7_response)
    print("Claude 3.7 Done")
```

### Greek Text Correction from `test_new_parser.py`
```python
# Greek text correction mappings
correction_map = {
    'ΣΣ': 'ΣΤ',
    'Σσ': 'Τσ',
    '΢': 'Σ',
    'ΟΤ': 'ΟΥ',
    'ΕΤ': 'ΕΥ',
    'ΣΤ': 'ΣΥ',
    'ΝΤ': 'ΝΥ',
    'ϊ': 'ω',
    'μζ': 'με',
    'ζγγ': 'εγγ',
    'ζξ': 'εξ'
}

for wrong, right in correction_map.items():
    text = text.replace(wrong, right)

# Handle final sigma corrections
text = re.sub(r'ς(?!\b)', 'σ', text)  # Replace ς with σ when not at word end
text = re.sub(r'σ\b', 'ς', text)      # Replace σ with ς at word end
```

### AWS Bedrock Client Setup
```python
def get_bedrock_client():
    """
    Returns a configured boto3 bedrock-runtime client using the stored credentials.
    """
    import boto3
    
    return boto3.client('bedrock-runtime', **AWS_CREDENTIALS)

# Usage in LLM modules
client = get_bedrock_client()
model_id = "arn:aws:bedrock:us-east-1:043309345392:inference-profile/us.anthropic.claude-3-5-sonnet-20240620-v1:0"

response = client.invoke_model(
    modelId=model_id,
    body=json.dumps(request_body)
)
```

## Output

The system generates structured output files in the `outputs/` directory:
- `claude3_5.txt` - Results from Claude 3.5 Sonnet
- `claude3_7.txt` - Results from Claude 3.7 Sonnet
- `claude4_sonnet.txt` - Results from Claude 4 Sonnet
- `deepseek.txt` - Results from DeepSeek model
- `llama.txt` - Results from Llama model

Each output file contains the structured extraction results formatted according to the specified schema for Greek hiring decision documents.

## Contributing

When contributing to this repository:
1. Ensure AWS credentials are not committed to version control
2. Test with various Greek PDF documents
3. Validate model outputs for accuracy
4. Follow the existing code structure and naming conventions
5. Update documentation for any new features or models

## License

This project is available under the terms specified by the repository owners. Please refer to the license file or contact the maintainers for usage permissions.