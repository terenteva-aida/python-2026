import os
import json
from flask import Flask, render_template, request, jsonify

# Для работы с PDF
try:
    from pypdf import PdfReader
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("Установите pypdf: pip install pypdf")

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB лимит

def extract_text_from_file(file_storage):
    """
    Извлекает текстовое содержимое из загруженного файла в зависимости от расширения.
    Возвращает кортеж (имя_файла, извлечённый_текст, тип_файла)
    """
    filename = file_storage.filename
    if not filename:
        return None, "Ошибка: файл без имени", "unknown"

    ext = os.path.splitext(filename)[1].lower()
    content = ""

    try:
        if ext == '.txt':
            # Обычный текстовый файл
            content = file_storage.read().decode('utf-8', errors='replace')
            file_type = "text/plain"
        elif ext == '.csv':
            # Для CSV отдаём содержимое как текст
            content = file_storage.read().decode('utf-8', errors='replace')
            file_type = "text/csv"
        elif ext == '.json':
            # Пытаемся красиво отформатировать JSON
            data = json.load(file_storage)
            content = json.dumps(data, indent=2, ensure_ascii=False)
            file_type = "application/json"
        elif ext == '.pdf':
            if not PDF_SUPPORT:
                content = "PDF обработка недоступна (установите pypdf)"
            else:
                reader = PdfReader(file_storage)
                text_pages = []
                for page in reader.pages:
                    text_pages.append(page.extract_text())
                content = "\n".join(text_pages)
                if not content.strip():
                    content = "(PDF не содержит извлекаемого текста)"
            file_type = "application/pdf"
        else:
            content = f"Неподдерживаемый тип файла: {ext}"
            file_type = "unknown"
    except Exception as e:
        content = f"Ошибка обработки файла: {str(e)}"
        file_type = "error"

    return filename, content[:5000] + ("..." if len(content) > 5000 else ""), file_type  # ограничим длину для демонстрации

@app.route('/')
def index():
    """Главная страница с формой."""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    """
    Эндпоинт для обработки промпта и загруженных файлов (заглушка).
    Возвращает JSON с извлечённым содержимым.
    """
    prompt = request.form.get('prompt', '').strip()
    uploaded_files = request.files.getlist('files')  # поле с именем 'files'

    if not uploaded_files or all(f.filename == '' for f in uploaded_files):
        return jsonify({"error": "Не загружено ни одного файла"}), 400

    results = []
    for file in uploaded_files:
        if file and file.filename:
            name, content, ftype = extract_text_from_file(file)
            if name:
                results.append({
                    "filename": name,
                    "type": ftype,
                    "content_preview": content
                })

    # Здесь могла бы быть основная логика обработки (заглушка)
    # Например, передача prompt и всех текстов в LLM или другой анализатор.

    response = {
        "status": "success",
        "prompt": prompt,
        "processed_files": results,
        "message": "Обработка завершена (заглушка)"
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)