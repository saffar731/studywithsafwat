import os
from flask import Flask, render_template, request, redirect, url_for
from vercel_blob import upload

app = Flask(__name__)

# Note: You must set the BLOB_READ_WRITE_TOKEN in your Vercel Dashboard Environment Variables
# The 'upload' function from vercel_blob automatically looks for this token.

@app.route('/')
def index():
    # In a real production app, you would store the URLs in a database like Vercel KV or Postgres.
    # For now, we will focus on the upload and display logic.
    return render_template('index.html')

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/submit-homework', methods=['POST'])
def submit_homework():
    if 'homework_image' not in request.files:
        return "No file selected"
    
    file = request.files['homework_image']
    student_name = request.form.get('student_name')
    subject = request.form.get('subject')

    if file:
        # Create a unique filename
        filename = f"{subject}_{student_name}_{file.filename}"
        
        # Read the file content
        file_content = file.read()
        
        # Upload directly to Vercel Blob
        # This returns a dictionary containing the 'url' of the uploaded file
        blob_details = upload(filename, file_content)
        
        # Redirect to home or a success page
        # In a full setup, you'd save blob_details['url'] to a list to show on index.html
        return f"<h1>Uploaded to Cloud!</h1><p>URL: {blob_details['url']}</p><a href='/'>Go Home</a>"
    
    return "Upload failed."

if __name__ == '__main__':
    app.run(debug=True)