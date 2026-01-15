import os
from flask import Flask, render_template, request, redirect, url_for
from vercel_blob import put # Use 'put' instead of 'upload'

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    # For now, we return the gallery page
    return render_template('index.html')

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/submit-homework', methods=['POST'])
def submit_homework():
    if 'homework_image' not in request.files:
        return "No file selected"
    
    file = request.files['homework_image']
    student_name = request.form.get('student_name', 'Student')
    subject = request.form.get('subject', 'General')

    if file:
        filename = f"{subject}_{student_name}_{file.filename}"
        file_content = file.read()
        
        # Use put() to send to Vercel Blob
        # 'content_type' helps the browser display the image correctly
        blob = put(filename, file_content, {"content_type": file.content_type})
        
        # This 'blob' object contains the new 'url'
        return f"<h1>Success!</h1><p>View here: <a href='{blob['url']}'>{blob['url']}</a></p>"
    
    return "Failed to upload."
