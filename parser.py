from storage import get_file_path
import os
import pdfplumber
import docx

def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_file(file_id):
    filepath = get_file_path(file_id)
    if not filepath or not os.path.exists(filepath):
        return {"error": "File not found"}

    ext = filepath.rsplit('.', 1)[1].lower()
    try:
        if ext == 'pdf':
            content = extract_text_from_pdf(filepath)
        elif ext == 'docx':
            content = extract_text_from_docx(filepath)
        else:
            return {"error": "Unsupported file type"}

        return {
            'word_count': len(content.split()),
            'preview': content[:200]
        }
    except Exception as e:
        return {"error": f"Failed to parse file: {str(e)}"}
