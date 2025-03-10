from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os

app = Flask(__name__)

# Folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    try:
        # Get the list of filenames in the uploads folder
        filenames = os.listdir(app.config['UPLOAD_FOLDER'])
        return render_template('index.html', filenames=filenames)
    except Exception as e:
        return f"An error occurred: {e}", 500


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if the 'file' key exists in the form data
        if 'file' not in request.files:
            return "No file part", 400

        # Retrieve the file from the form
        file = request.files['file']

        # Check if the file has no name (i.e., no file selected)
        if file.filename == '':
            return "No selected file", 400

        # Save the file to the upload folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Redirect to the index route to display uploaded files
        return redirect(url_for('index'))

    except Exception as e:
        return f"An error occurred while uploading the file: {e}", 500


@app.route('/download/<filename>')
def download_file(filename):
    try:
        # Serve the requested file from the upload folder
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return f"An error occurred while downloading the file: {e}", 500


if __name__ == "__main__":
    app.run(debug=True)
