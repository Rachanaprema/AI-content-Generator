
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from difflib import SequenceMatcher
from docx import Document
import PyPDF2
import os
import cohere
import pytesseract
import os

import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"




from dotenv import load_dotenv

from .algorithm import main, fileSimilarity

# Load environment variables or API keys securely in production
co = cohere.Client("YJDyRQPv7ZamJQy9Jxq29Qt5eJccWXKugY1U6GZu")

# ============================ Static Views ============================

def home(request):
    """Renders the landing homepage (index.html)"""
    return render(request, 'pc/index.html')

def documentUpload(request):
    return render(request, 'pc/documentUpload.html')

def textUpload(request):
    return render(request, 'pc/textUpload.html')

def comparetextCheck(request):
    return render(request, 'pc/comparetextCheck.html')

def comparefilecheck(request):
    return render(request, 'pc/comparefilecheck.html')

def helpus(request):
    return render(request, 'pc/help.html')

def contactus(request):
    return render(request, 'pc/contactus.html')

def document_ai_helper(request):
    return HttpResponse("Document AI Helper is working.")

# ============================ AI Chatbot with Cohere ============================

def test(request):
    if request.method == 'POST':
        user_input = request.POST.get('q')
        try:
            response = co.chat(
                chat_history=[],
                message=user_input,
                model='command-r'
            )
            return render(request, 'pc/test.html', {'chat_response': response.text})
        except Exception as e:
            return render(request, 'pc/test.html', {'error': str(e)})
    return render(request, 'pc/test.html')

# ======================= One File vs Web: AI Similarity =======================

def filetest(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('docfile')
        if not uploaded_file:
            return render(request, 'pc/documentUpload.html', {'error': 'No file uploaded.'})

        try:
            file_text = extract_text_from_file(uploaded_file)
            percent_list, link_list = main.findSimilarity(file_text)

            if not isinstance(percent_list, (list, tuple)) or not isinstance(link_list, (list, tuple)):
                raise TypeError("Expected lists or tuples for similarity results.")


            filtered_results = [
                (round(float(p) * 100, 2), l)
                for p, l in zip(percent_list, link_list)
                if isinstance(p, (float, int)) and 0 <= float(p) <= 1 and float(p) > 0.75
            ]

            if not filtered_results:
                return render(request, 'pc/documentUpload.html', {'message': 'No relevant content found.'})

            filtered_results.sort(key=lambda x: x[0], reverse=True)

            return render(request, 'pc/documentUpload.html', {'results': filtered_results})

        except Exception as e:
            return render(request, 'pc/documentUpload.html', {'error': f'Similarity check failed: {str(e)}'})

    return render(request, 'pc/documentUpload.html')

# ============================ Text vs Text ============================

def twofiletest1(request):
    if request.method == 'POST':
        text1 = request.POST.get('text1')
        text2 = request.POST.get('text2')

        if not text1 or not text2:
            return render(request, 'pc/comparetextCheck.html', {'error': 'Both text fields are required.'})

        ratio = SequenceMatcher(None, text1, text2).ratio()
        similarity_percentage = round(ratio * 100, 2)

        return render(request, 'pc/comparetextCheck.html', {'result': similarity_percentage})

    return render(request, 'pc/comparetextCheck.html')

# ============================ File vs File ============================

def twofilecompare1(request):
    if request.method == 'POST':
        doc1 = request.FILES.get('docfile1')
        doc2 = request.FILES.get('docfile2')

        if not doc1 or not doc2:
            return render(request, 'pc/comparefilecheck.html', {'error': 'Please upload both files.'})

        try:
            text1 = extract_text_from_file(doc1)
            text2 = extract_text_from_file(doc2)
            similarity_score = round(fileSimilarity.findFileSimilarity(text1, text2), 2)

            return render(request, 'pc/comparefilecheck.html', {'result': similarity_score})
        except Exception as e:
            return render(request, 'pc/comparefilecheck.html', {'error': f'Error comparing files: {str(e)}'})

    return render(request, 'pc/comparefilecheck.html')

# ============================ Utility ============================

def extract_text_from_file(file_obj):
    filename = file_obj.name.lower()
    try:
        if filename.endswith('.txt'):
            return file_obj.read().decode('utf-8', errors='ignore')
        elif filename.endswith('.docx'):
            document = Document(file_obj)
            return '\n'.join(para.text for para in document.paragraphs)
        elif filename.endswith('.pdf'):
            reader = PyPDF2.PdfReader(file_obj)
            return ''.join(page.extract_text() or '' for page in reader.pages)
        else:
            raise ValueError("Unsupported file type. Only .txt, .docx, and .pdf are allowed.")
    except Exception as e:
        raise ValueError(f"Failed to extract text from file: {str(e)}")

# ============================ Debug Utility (Optional) ============================

def test_template_lookup():
    try:
        get_template('pc/comparetextCheck.html')
    except TemplateDoesNotExist:
        print("TEMPLATE NOT FOUND: pc/comparetextCheck.html")
        from django.conf import settings
        print("Template DIRS:", settings.TEMPLATES[0]['DIRS'])
        for dirpath, dirnames, filenames in os.walk(settings.BASE_DIR):
            for filename in filenames:
                if filename == "comparetextCheck.html":
                    print("Found at:", os.path.join(dirpath, filename))

def twofiletest1(request):
    if request.method == 'POST':
        text1 = request.POST.get('text1')
        text2 = request.POST.get('text2')

        if not text1 or not text2:
            return render(request, 'pc/comparetextCheck.html', {'error': 'Both text fields are required.'})

        ratio = SequenceMatcher(None, text1, text2).ratio()
        similarity_percentage = round(ratio * 100, 2)

        return render(request, 'pc/comparetextCheck.html', {'result': similarity_percentage})

    return render(request, 'pc/comparetextCheck.html')


from django.shortcuts import render
def text_helper(request):
    api_key = os.environ.get('COHERE_API_KEY', 'YJDyRQPv7ZamJQy9Jxq29Qt5eJccWXKugY1U6GZu')
    co = cohere.Client(api_key)
    result = None
    if request.method == 'POST':
        user_text = request.POST.get('user_text')
        if user_text:
            try:
                response = co.generate(
                    model='command',
                    prompt=f"Improve grammar and rewrite: {user_text}",
                    max_tokens=100
                )
                result = response.generations[0].text.strip()
            except Exception as e:
                result = f"API Error: {e}"
        return render(request, 'pc/text_helper.html', {'result': result})
    return render(request, 'pc/text_helper.html')

def image_analysis(request):
    from PIL import Image
    import pytesseract

    # Ensure correct path to tesseract.exe
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    result = None
    summary = None
    error = None

    if request.method == 'POST':
        image_file = request.FILES.get('image_file')
        if image_file:
            try:
                # Load and process the image
                img = Image.open(image_file)
                extracted_text = pytesseract.image_to_string(img)

                # Check extracted text length
                if len(extracted_text.strip()) < 250:
                    error = "Extracted text is too short for summarization (minimum 250 characters required)."
                else:
                    # Call Cohere summarization (replace model if needed)
                    co = cohere.Client(os.environ.get('COHERE_API_KEY', 'YJDyRQPv7ZamJQy9Jxq29Qt5eJccWXKugY1U6GZu'))
                    response = co.summarize(text=extracted_text, model='summarize-medium')  # or 'summarize-v2'
                    summary = response.summary

                result = extracted_text

            except Exception as e:
                error = f"Image OCR or summarization failed: {str(e)}"

    return render(request, 'pc/image_analysis.html', {
        'result': result,
        'summary': summary,
        'error': error
    })


def summary_generator(request):
    api_key = os.environ.get('COHERE_API_KEY', 'YJDyRQPv7ZamJQy9Jxq29Qt5eJccWXKugY1U6GZu')
    co = cohere.Client(api_key)
    summary = None
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            try:
                response = co.summarize(text=text, model='summarize-xlarge')
                summary = response.summary
            except Exception as e:
                summary = f"API Error: {e}"
        return render(request, 'pc/summary_generator.html', {'summary': summary})
    return render(request, 'pc/summary_generator.html')

def websearch(request):
    api_key = os.environ.get('COHERE_API_KEY', 'YJDyRQPv7ZamJQy9Jxq29Qt5eJccWXKugY1U6GZu')
    co = cohere.Client(api_key)
    results = []
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            try:
                response = co.chat(
                    chat_history=[],
                    message=f"Search the web for: {query}",
                    model='command-r'
                )
                results = [response.text]
            except Exception as e:
                results = [f"API Error: {e}"]
        return render(request, 'pc/websearch.html', {'results': results})
    return render(request, 'pc/websearch.html')
