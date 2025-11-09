from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pathlib import Path
from imageToPdfConverter import convert_single_image_to_pdf, convert_multiple_images_to_pdf, output_file_path
from docToPdfConverter import convert_doc_to_pdf, convert_multiple_doc_to_pdf
from txtFileToPdfConverter import convert_txt_to_pdf
from pdfToImageConverter import pdf_to_jpg_pymupdf
from pdfToWordConverter import pdf_to_doc_pdf2docx
from splitPdf import split_pdf_pypdf2
from mergePdf import merge_pdfs_safe
from pdfCompression import compress_pdf_ghostscript
from utils import create_random_upload_folder
import os
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)
#CORS(app, origins=["http://127.0.0.1:3000", "http://localhost:3000"])
CORS(app)
    
# Define upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/image_to_pdf', methods=['POST'])
def upload_files():
    files = request.files.getlist('files[]')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files provided'}), 400

    new_folder_name = create_random_upload_folder()
    for file in files:
        filename = secure_filename(file.filename)
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], new_folder_name)
        save_path = os.path.join(folder_path, filename)
        file.save(save_path)
    
    filename = secure_filename(files[0].filename)
    
    image_name = Path(save_path).stem
    pdf_filename = image_name + "Convert.pdf"
    pdf_path = output_file_path(save_path)
    if len(files) > 1:
        convert_multiple_images_to_pdf(files, pdf_filename, folder_path)
    else: 
        convert_single_image_to_pdf(save_path, pdf_filename, folder_path)
    # Respond with filename!
    return jsonify({"pdf_filename": pdf_filename, "folder_name": new_folder_name})  # <--- IMPORTANT
    
@app.route('/doc_to_pdf', methods=['POST'])
def upload_files_doc():
    files = request.files.getlist('files[]')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files provided'}), 400

    new_folder_name = create_random_upload_folder()
    for file in files:
        filename = secure_filename(file.filename)
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], new_folder_name)
        save_path = os.path.join(folder_path, filename)
        file.save(save_path)
    
    filename = secure_filename(files[0].filename)
    
    image_name = Path(save_path).stem
    pdf_filename = image_name + "Convert.pdf"
    print('pdf_filename : ' +pdf_filename)
    print('+++++++++++++++++++++++++')
    pdf_path = output_file_path(save_path)
    if len(files) > 1:
        convert_multiple_doc_to_pdf(files, pdf_filename, folder_path)
    else: 
        convert_doc_to_pdf(save_path, pdf_filename, folder_path)
    # Respond with filename!
    return jsonify({"doc_filename": pdf_filename, "folder_name": new_folder_name})  # <--- IMPORTANT

@app.route('/txt_to_pdf', methods=['POST'])
def upload_txt_files():
    files = request.files.getlist('files[]')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files provided'}), 400

    new_folder_name = create_random_upload_folder()
    for file in files:
        filename = secure_filename(file.filename)
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], new_folder_name)
        save_path = os.path.join(folder_path, filename)
        file.save(save_path)
    
    filename = secure_filename(files[0].filename)
    
    file_name = Path(save_path).stem
    pdf_filename = file_name + "Convert.pdf"
    pdf_path = output_file_path(save_path)
    if len(files) > 1:
        convert_multiple_images_to_pdf(files, pdf_filename, folder_path)
    else: 
        convert_txt_to_pdf(save_path, pdf_filename, folder_path)
    # Respond with filename!
    return jsonify({"txt_filename": pdf_filename, "folder_name": new_folder_name})

@app.route('/pdf_to_img', methods=['POST'])
def upload_pdf_files():
    files = request.files.getlist('files[]')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files provided'}), 400

    new_folder_name = create_random_upload_folder()
    for file in files:
        filename = secure_filename(file.filename)
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], new_folder_name)
        save_path = os.path.join(folder_path, filename)
        file.save(save_path)
    
    filename = secure_filename(files[0].filename)
    
    file_name = Path(save_path).stem
    img_zip_filename = file_name + "Convert.zip"
    pdf_path = output_file_path(save_path)
    if len(files) > 1:
        pdf_to_jpg_pymupdf(files, img_zip_filename, folder_path)
    else: 
        pdf_to_jpg_pymupdf(save_path, img_zip_filename, folder_path)
    # Respond with filename!
    return jsonify({"pdf_filename": img_zip_filename, "folder_name": new_folder_name})


@app.route('/pdf_to_doc', methods=['POST'])
def upload_pdf_to_doc_files():
    files = request.files.getlist('files[]')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files provided'}), 400

    new_folder_name = create_random_upload_folder()
    for file in files:
        filename = secure_filename(file.filename)
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], new_folder_name)
        save_path = os.path.join(folder_path, filename)
        file.save(save_path)
    
    filename = secure_filename(files[0].filename)
    
    file_name = Path(save_path).stem
    doc_filename = file_name + "Convert.docx"
    pdf_path = output_file_path(save_path)
    if len(files) > 1:
        pdf_to_doc_pdf2docx(files, doc_filename, folder_path)
    else: 
        pdf_to_doc_pdf2docx(save_path, doc_filename, folder_path)
    # Respond with filename!
    return jsonify({"doc_filename": doc_filename, "folder_name": new_folder_name})


@app.route('/split_pdf', methods=['POST'])
def split_pdf_pdf2():
    files = request.files.getlist('files[]')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files provided'}), 400

    new_folder_name = create_random_upload_folder()
    for file in files:
        filename = secure_filename(file.filename)
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], new_folder_name)
        save_path = os.path.join(folder_path, filename)
        file.save(save_path)
    
    filename = secure_filename(files[0].filename)
    file_name = Path(save_path).stem
    pdf_file_start_name = "SplitPdf"
    pdf_path = output_file_path(save_path)

    if len(files) > 1:
        split_pdf_pypdf2(files, pdf_file_start_name, folder_path, 1)
    else: 
        split_pdf_pypdf2(save_path, pdf_file_start_name, folder_path, 1)
    # Respond with filename!
    return jsonify({"split_filename": "SplitPdf.zip", "folder_name": new_folder_name})


@app.route('/merge_pdf', methods=['POST'])
def merge_pdf():
    files = request.files.getlist('files[]')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files provided'}), 400

    new_folder_name = create_random_upload_folder()
    for file in files:
        filename = secure_filename(file.filename)
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], new_folder_name)
        save_path = os.path.join(folder_path, filename)
        file.save(save_path)
    
    filename = secure_filename(files[0].filename)
    file_name = Path(save_path).stem
    pdf_file_name = "MergedPdf.pdf"
    pdf_path = output_file_path(save_path)

    if len(files) > 1:
        merge_pdfs_safe(files, pdf_file_name, folder_path)
    else: 
        merge_pdfs_safe(save_path, pdf_file_name, folder_path)
    # Respond with filename!
    return jsonify({"merged_filename": pdf_file_name, "folder_name": new_folder_name})

@app.route('/compress_pdf', methods=['POST'])
def upload_pdf_to_compress():
    files = request.files.getlist('files[]')
    compression_level = request.form.get('compressionLevel')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files provided'}), 400

    new_folder_name = create_random_upload_folder()
    for file in files:
        filename = secure_filename(file.filename)
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], new_folder_name)
        save_path = os.path.join(folder_path, filename)
        file.save(save_path)
    
    filename = secure_filename(files[0].filename)
    
    file_name = Path(save_path).stem
    compress_pdf_filename = file_name + "Compressed.pdf"
    pdf_path = output_file_path(save_path)
    compress_pdf_ghostscript(save_path, compress_pdf_filename, folder_path, compression_level=compression_level)
    # Respond with filename!
    return jsonify({"pdf_filename": compress_pdf_filename, "folder_name": new_folder_name})


@app.route('/download_pdf', methods=['GET'])
def download_pdf():
    print('++++++++++++ download_pdf ++++++++++++++')
    fileName = request.args.get('fileName')     # gets 'example.pdf'
    folderName = request.args.get('folderName') # gets 'randomfolder'
    print('++++++++++++ download_pdf ++++++++++++++')
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folderName)
    pdf_path = os.path.join(folder_path, fileName)
    
    print('pdf_path: '+pdf_path)
    return send_file(pdf_path, as_attachment=True, download_name=fileName, mimetype='application/pdf')


@app.route('/delete_file', methods=['POST'])
def delete_file():
    data = request.get_json()
    folderName = data.get('folderName')
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folderName)
    
    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
        print(f"Deleted folder and all contents: {folder_path}")
        return jsonify({'message': f'Deleted files starting with {folder_path}.'})
    else:
        print(f"Folder not found: {folder_path}")
        jsonify({'message': 'Partial deletion.', 'deleted_files': deleted_files, 'errors': error_files}), 500
        
        
if __name__ == '__main__':
    app.run(port=5000)
