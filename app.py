from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
from PIL import Image
from process_image import process_image

app = Flask(__name__)

# Configurations
UPLOAD_FOLDER = 'uploads/'  # Folder to save uploaded images
PROCESSED_FOLDER = 'processed/'  # Folder to save processed images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
HTML_LOC = "index.html"

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def make_image_grayscale(image_path, filename, output_folder):
    processed_filename  = "grayscale_" + filename 
    output_path = os.path.join(output_folder, processed_filename)

    # Your image processing code here, as an example:
    img = Image.open(image_path)
    img = img.convert("L")  # Example: Convert the image to grayscale
    img.save(output_path)

    return processed_filename

# TODO: display uploaded image
# - display waiting message
# - display whether sets are found

# Add a route for the home page
@app.route('/')
def index():
    return render_template(HTML_LOC)

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'image' not in request.files:
            return "No image part in the request", 400
        file = request.files['image']

        if file and allowed_file(file.filename):
            # Save the file securely
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Process the image
            processed_folder = app.config['PROCESSED_FOLDER']
            processed_filenames = process_image(file_path, filename, processed_folder)

            # Redirect to display the processed image
            return redirect(url_for('display_processed_images', filenames=processed_filenames))

    
    return render_template(HTML_LOC)

@app.route('/processed/<filenames>')
def display_processed_images(filenames): 
    filenames = filenames.split(',')
    processed_image_urls = [url_for('processed_file', filename=filename) for filename in filenames]
    return render_template(HTML_LOC, processed_image_urls=processed_image_urls)

@app.route('/processed_files/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
