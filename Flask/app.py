import os

from PyPDF2 import PdfReader
from flask import Flask, render_template, request, jsonify
from docx import Document
import openai
from dotenv import load_dotenv

from flask_sqlalchemy import SQLAlchemy

# Инициализация Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель для хранения запросов и ответов
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10), nullable=False)  # user или assistant
    content = db.Column(db.Text, nullable=False)

# Создаем базу данных, если она еще не существует
with app.app_context():
    db.create_all()

# Проверка формата файла
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Створення каталогу uploads, якщо він не існує
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Функція для витягання тексту з файлів DOCX
def extract_text_from_docx(filepath):
    doc = Document(filepath)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

# Функція для аналізу тексту за допомогою GPT-4

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')



# Обробка завантаження файлів
# Обробка завантаження файлів
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request", 400
    file = request.files['file']
    user_request = request.form.get('user_request', '')  # Получаем пользовательский запрос
    if file.filename == '':
        return "No file selected", 400
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Витягаємо текст із завантаженого файлу
        if file.filename.endswith('.docx'):
            text = extract_text_from_docx(filepath)
        elif file.filename.endswith('.txt'):
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        elif file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(filepath)
        else:
            return "Unsupported file type", 400

        # Аналіз тексту через GPT-4
        try:
            analysis_result = analyze_text_with_llm(text, user_request)
        except Exception as e:
            return f"Error during LLM processing: {str(e)}", 500

        return render_template('result.html', result=analysis_result)

    return "Invalid file format", 400

# Функция для анализа текста с учетом пользовательского запроса
def analyze_text_with_llm(text, user_request):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for document validation."},
            {"role": "user", "content": f"User request: {user_request}\n\nDocument text:\n\n{text}"}
        ],
        temperature=0.2
    )
    # GPT повертає текст із HTML-тегами
    result_with_html = response['choices'][0]['message']['content']
    return result_with_html


if __name__ == 'main':
    app.run(debug=True)