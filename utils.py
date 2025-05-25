import os
import joblib


UPLOAD_FOLDER = 'uploads'

def extract_text_from_file(filepath):
    try:
        ext = os.path.splitext(filepath)[1].lower()
        if ext == '.txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        elif ext == '.pdf':
            from PyPDF2 import PdfReader
            reader = PdfReader(filepath)
            return "\n".join(page.extract_text() or '' for page in reader.pages)
        elif ext == '.docx':
            import docx
            doc = docx.Document(filepath)
            return "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        print(f"خطأ أثناء قراءة الملف: {e}")
    return ""


def extract_title(filepath):
    """تحاول استخراج أول سطر أو جملة كعنوان من محتوى المستند"""
    text = extract_text_from_file(filepath)
    if not text:
        return "عنوان غير معروف"
    
    # نحاول أخذ أول 100 حرف أو أول سطر
    lines = text.strip().split('\n')
    for line in lines:
        if line.strip():
            return line.strip()[:100]
    
    return "عنوان غير معروف"



def extract_all_documents():
    documents = []
    if not os.path.exists(UPLOAD_FOLDER):
        return documents

    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(filepath):  # نعرض كل الملفات الموجودة
            title = os.path.splitext(filename)[0]
            documents.append({'title': title, 'filename': filename})
    return documents


def search_in_documents(search_text):
    results = []
    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(filepath):
            content = extract_text_from_file(filepath)
            if search_text.lower() in content.lower():
                results.append({'filename': filename, 'snippet': get_snippet(content, search_text)})
    return results
    


def get_snippet(text, search_text, length=100):
    index = text.lower().find(search_text.lower())
    if index == -1:
        return ''
    start = max(index - length//2, 0)
    end = min(index + length//2, len(text))
    return text[start:end].replace('\n', ' ')

# تحميل النموذج المدرب مرة واحدة
model = joblib.load('document_classifier.joblib')

def classify_document(text):
    """تستخدم النموذج لتصنيف المستند"""
    return model.predict([text])[0]


