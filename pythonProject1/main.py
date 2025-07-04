from test_new_parser import extract_data_from_pdf
from llms.claude3_7 import claude3_7
from llms.claude3_5 import claude3_5
from llms.claude4_sonnet import claude4_sonnet
from llms.llama import llama
from llms.deepseek import deepseek

pdf_path = "data/perilipsi_anaplirwth_meiwmenou.pdf"

try:
    first_paragraph, data = extract_data_from_pdf(pdf_path)

    if not first_paragraph.strip():
        print("Warning: No text extracted from PDF. It might be image-based.")
        exit(1)

except Exception as e:
    print(f"Error extracting text from PDF: {e}")
    exit(1)

print("15 Data", data)

print("Select the model you want by typing: 'claude3.7', 'claude3.5', 'claude4', 'llama', or 'deepseek'.")
valid_models = ['claude3.7', 'claude3.5', 'claude4', 'llama', 'deepseek']
model = input()

while True:

    while model not in valid_models:
        print("Invalid model. Please type again: 'claude3.7', 'claude3.5', 'claude4', 'llama', or 'deepseek'.")
        model = input()

    if model == 'claude3.7':
        claude3_7_response = claude3_7(first_paragraph, data[2:16])
        with open("outputs/claude3_7.txt", "w", encoding="utf-8") as f:
            f.write(claude3_7_response)
        print("Claude 3.7 Done")
    elif model == 'claude3.5':
        claude3_5_response = claude3_5(first_paragraph, data[2:16])
        with open("outputs/claude3_5.txt", "w", encoding="utf-8") as f:
            f.write(claude3_5_response)
        print("Claude 3.5 Done")
    elif model == 'claude4':
        claude_4_response = claude4_sonnet(first_paragraph, data[2:16])
        with open("outputs/claude4_sonnet.txt", "w", encoding="utf-8") as f:
            f.write(claude_4_response)
        print("Claude 4 Done")
    elif model == 'deepseek':
        deepseek_response = deepseek(first_paragraph, data[2:16])
        with open("outputs/deepseek.txt", "w", encoding="utf-8") as f:
            f.write(deepseek_response)
        print("Deepseek Done")
    elif model == 'llama':
        llama_response = llama(first_paragraph, data[2:16])
        with open("outputs/llama.txt", "w", encoding="utf-8") as f:
            f.write(llama_response)
        print("Llama Done")

    print("Would you like to continue with another model? yes/no")
    answer = input().strip().lower()
    if answer == 'yes':
        print("Select the model you want by typing: 'claude3.7', 'claude3.5', 'claude4', 'llama', or 'deepseek'.")
        model = input()
    else:
        print("Bye")
        break