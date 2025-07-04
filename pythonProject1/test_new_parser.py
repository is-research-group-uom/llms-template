import pymupdf4llm
import re
import pprint  # For pretty printing the output


def _clean_greek_text(text: str) -> str:
    """
    Corrects common character mapping errors in Greek text extracted from PDFs.
    """
    # This dictionary handles direct, one-to-one character replacements.
    # Add more mappings here if you discover other errors.
    correction_map = {
        'ΣΣ': 'ΣΤ',
        'Σσ': 'Τσ',
        '΢': 'Σ',
        'ΟΤ': 'ΟΥ',
        'ΕΤ': 'ΕΥ',
        'ΣΤ': 'ΣΥ',
        'ΝΤ':'ΝΥ',
        'ϊ':'ω',
        'μζ':'με',
        'ζγγ':'εγγ',
        'ζξ':'εξ',
        'αριιμ':'αριθμ',
        'ΛΤΓ':'ΛΥΓ',
        'ΕΥΗ':'ΕΤΗ',
        'ΓΤ':'ΓΥ',
        'ΣΠΤΡ':'ΣΠΥΡ',
        'ΘΤΜ':'ΘΥΜ',
        'ιήι':'ιθι',
        'Τπ':'Υπ',
        'άιμ':'άθμ',
        'χφε':'χυε'
    }

    for wrong, right in correction_map.items():
        text = text.replace(wrong, right)

    text = re.sub(r'ς(?!\b)', 'σ', text)

    text = re.sub(r'σ\b', 'ς', text)

    return text



def extract_data_from_pdf(pdf_path: str):
    """
    Extracts introductory text and all tables from a PDF file, handling multi-line rows.

    The function converts the PDF to Markdown and then parses it.
    It identifies the introductory text as all content appearing before the
    first table. It then dynamically parses all tables, reading headers
    and merging multi-line rows into single data records.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        tuple: A tuple containing:
            - intro_text (str): The introductory text before any tables.
            - all_tables_data (list): A list of dictionaries, where each
                                      dictionary represents a row from a table.
                                      All tables are merged into this single list.
    """
    try:
        # Convert the entire PDF to a single Markdown string
        print(pdf_path)
        md_text = pymupdf4llm.to_markdown(pdf_path)
        md_text = _clean_greek_text(md_text)
        print(md_text)
    except Exception as e:
        print(f"Error processing {pdf_path} with pymupdf4llm: {e}")
        return "", []

    # --- Extract Introductory Text ---
    # The introductory text is everything before the first table's header separator.
    table_header_separator_match = re.search(r"\n\|-+[| -]+", md_text)

    if table_header_separator_match:
        # Find the start of the table header line (the line just before the separator)
        table_start_pos = md_text.rfind('\n', 0, table_header_separator_match.start())
        intro_text = md_text[:table_start_pos].strip()
    else:
        # If no tables are found, the whole text is introductory
        intro_text = md_text.strip()
        return intro_text, []

    # --- Extract and Parse Tables ---
    # Extract tables
    tables = re.findall(r"(?:\|.*\n)+", md_text)

    # print("paragraph_match:\n", paragraph_match)
    print("\nNumber of tables found:", len(tables))

    if (pdf_path == "data/diorismos_monimwn.pdf"):
        column_headers = [
            "Α/Α", "Επώνυμο", "Όνομα", "Πατρώνυμο", "Κλάδος",
            "Μόρια", "Σειρά", "Περιφέρεια", "Δ.Υ.Π.Ε.",
            "Αριθμός Βεβαίωσης ΔΙΠΑΑΔ", "Αριθμός Βεβαίωσης"
        ]
    elif (pdf_path == "data/proslipsi_anaplhrwtwn.pdf"):
        column_headers = [
            "A/A", "A/A ΡΟΗΣ", "Επώνυμο", "Όνομα", "Πατρώνυμο",
            "Ειδικότητα", "Κλάδος", "Τριτεκνος", "Πίνακας",
            "Σείρα Πίνακα", "Μορια Πίνακα", "Περιοχή Τοποθέτησης"
        ]
    elif (pdf_path == "data/anaplhrwtes_eep_ebp.pdf"):
        column_headers = [
            "A/A", "A/A ΡΟΗΣ", "Τύπος", "Επώνυμο", "Όνομα", "Πατρώνυμο",
            "Κλάδος", "Σείρα Πίνακα", "Περιοχή Πρόσληψης", "Διευθυνση Εκπαίδευσης"
        ]
    elif (pdf_path == "data/monimos_eep_ebp.pdf"):
        column_headers = [
            "A/A", "Σειρά Διορισμού", "Επώνυμο", "Όνομα",
            "Πατρώνυυμο", "Κλάδος Διορισμού", "Σειρά Πίνακα",
            "Περιοχή/ΣΔΕΥ Διορισμού", "ΔΠΕ/ΔΔΕ/ΠΔΕ", "Τυπος Κενου",
            "Αρ. Βεβ. Εγγραφής στο Μητρώο Ανθρώπινου Δυναμικού Ελληνικού Δημοσίου",
            "Αρ. βεβ. ΔΙΠΑΑΔ/Υπουργείου Εσωτερικών"
        ]
    elif (pdf_path == "data/topothethisi_monimou.pdf"):
        column_headers = [
            "A/A", "Αριθμός Μητρώου", "Επώνυμο", "Όνομα", "Όνομα Πατρός",
            "Οργανικι θέση", "Σύνολο Μορίων", "Δήμος ή Κοινότητα εντοπιότητας", "Μόρια Εντοπ",
            "Δήμος ή Κοινώτητα Εργασίας Συζύγου", "Μόρια Συνθπ", "Ειδική Κατηγορία",
            "Σχολείο Οριστικής Τοποθέτησης"
        ]
    elif (pdf_path == "data/tpothetisi_anaplhrwtwn.pdf"):
        column_headers = [
            "Επώνυμο", "Όνομα", "Κλάδος", "Μόρια Πίνακα", 'ΣΧΟΛΕΙΟ Τοποθέτησης',
            "ΣΧΟΛΕΙΟ 1ης Διαθεσης", "ΣΧΟΛΕΙΟ 2ης Διαθεσης"
        ]
    elif (pdf_path == "data/topothetisi_monimou_ksanthis.pdf"):
        column_headers = [
            "A/A", "ΕΠΩΝΥΜΟ","ΟΝΟΜΑ" , "ΠΑΤΡΩΝΥΜΟ", "ΚΛΑΔΟΥ", "ΣΧΟΛΕΙΟ ΝΕΑΣ ΟΡΓΑΝΙΚΗΣ"
        ]
    elif (pdf_path == "data/diathesi.pdf"):
        column_headers = [
            "A/A", "ΕΠΩΝΥΜΟ","ΟΝΟΜΑ", "ΚΛΑΔΟΣ", "ΣΧΟΛΕΙΟ ΟΡΓΑΝΙΚΗΣ/ΠΡΟΣΩΡΙΝΗΣ ΤΟΠΟΘΕΤΗΣΗΣ", "ΣΧΟΛΕΙΟ ΔΙΑΘΕΣΗΣ ΓΙΑ ΣΥΜΠΛΗΡΩΣΗ ΩΡΑΡΙΟΥ",
            "ΩΡΕΣ ΣΥΜΠΛΗΡΩΣΗΣ"
        ]



    data = []
    for i, table in enumerate(tables, 1):
        cleaned_content = re.sub(
            r"\|Α/Α\|.*?\|Αριθμός<br>Βεβαίωσης<br>ΔΙΠΑΑΔ\|\n\|---\|.*?\|---\|\n",
            "",
            table,
            flags=re.DOTALL
        )
        # print(cleaned_content)

        # Split the content into lines and process each line
        lines = cleaned_content.strip().split('\n')

        for line in lines:
            if line.strip() and line.startswith('|') and line.endswith('|'):
                # Remove leading and trailing pipes, then split by pipe
                columns = line[1:-1].split('|')

                # Create a row dictionary
                if len(columns) >= len(column_headers):
                    row = {}
                    for j, header in enumerate(column_headers):
                        if j < len(columns):
                            row[header] = columns[j].strip()
                    data.append(row)
                else:
                    print(f"Warning: Line has {len(columns)} columns, expected at least {len(column_headers)}")
                    print(f"Line: {line}")

    return md_text