from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from classifier import classify_document
from utils import extract_text_from_file, extract_all_documents, search_in_documents, extract_title
import joblib
import time
from dropbox_uploader import upload_to_dropbox
from database import init_db, insert_file
from datetime import datetime



app = Flask(__name__)
upload_history = []  # تأكد من وجود هذا في أعلى الملف (أو حسب مكان تخزينك للتاريخ)
app.secret_key = 'supersecretkey123'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = joblib.load('document_classifier.joblib')



# دعم أكثر من صيغة ملف
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or request.files['file'].filename == '':
        flash('لم يتم اختيار ملف')
        return redirect("/")
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        original_filename = file.filename  # هذا هو الاسم الكامل مع الامتداد مثل: "myfile.pdf"
        filename = secure_filename(original_filename)  # نحفظ اسم آمن للملف
        print("اسم الملف الأصلي (مع الامتداد):", original_filename)

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # استخراج عنوان الوثيقة من محتواها (إذا عندك دالة extract_title)
        title = extract_title(filepath)

        # رفع الملف إلى Dropbox (لو تستخدم)
        dropbox_link = upload_to_dropbox(filepath, f"/{filename}")

        # استخراج النص مع التعامل مع الترميزات
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='latin1') as f:
                text = f.read()

        prediction = model.predict([text])[0]

        # إضافة إلى السجل (التاريخ)
        upload_history.append({
            "filename": original_filename,
            "dropbox_link": dropbox_link,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prediction": prediction
        })

        # حفظ في قاعدة البيانات
        insert_file(original_filename, prediction, dropbox_link, title)

        alert_message = None
        if prediction.lower() in ['unknown', '', 'غير معروف', 'غير محدد']:
            alert_message = "تم رفع الملف بنجاح ولكن لم يتم تحديد تصنيف واضح."

        return render_template('result.html', prediction=prediction, filename=original_filename, text=text, alert_message=alert_message)
    else:
        flash('الرجاء رفع ملف بصيغة txt أو pdf أو docx')
        return redirect('/')



@app.route('/preview')
def preview_documents():
    previews = {}
    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(filepath):
            text = extract_text_from_file(filepath)
            previews[filename] = text[:1000]
    return render_template('preview.html', previews=previews)



@app.route('/search', methods=['POST'])
def search():
    search_text = request.form.get('search_text')
    results = []

    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(filepath):
            text = extract_text_from_file(filepath)

            if search_text.lower() in text.lower():
                # تظليل الكلمة في النص
                highlighted = text.replace(
                    search_text, f"<mark>{search_text}</mark>"
                )
                results.append({
                    'filename': filename,
                    'highlighted_text': highlighted[:1500]  # عرض أول 1500 حرف فقط
                })

    return render_template('result.html', results=results, search_text=search_text)



@app.route('/documents')
def documents_list():
    documents = []
    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(filepath):
            title = filename
            documents.append({'filename': filename, 'title': title})
    documents.sort(key=lambda d: d['title'])
    return render_template('documents.html', documents=documents)



@app.route('/stats')
def system_stats():
    total_files = 0
    total_size = 0
    search_time = None
    sort_time = None
    classify_time = None

    # عدد الملفات وحجمها
    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(filepath):
            total_files += 1
            total_size += os.path.getsize(filepath)

    # قياس الزمن لكل عملية
    start = time.time()
    search_in_documents("test")  # بحث تجريبي
    search_time = time.time() - start

    start = time.time()
    docs = [{'filename': f, 'title': f} for f in os.listdir(UPLOAD_FOLDER)]
    docs.sort(key=lambda d: d['title'])
    sort_time = time.time() - start

    start = time.time()
    for filename in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(path):
            text = extract_text_from_file(path)
            model.predict([text])
    classify_time = time.time() - start

    return render_template('stats.html', 
        total_files=total_files,
        total_size=round(total_size / 1024, 2),  # بالكيلوبايت
        search_time=round(search_time, 3),
        sort_time=round(sort_time, 3),
        classify_time=round(classify_time, 3))


@app.route('/about')
def about_page():
    return render_template('about.html')


if __name__ == '__main__': 
    init_db()
    app.run(debug=True)
