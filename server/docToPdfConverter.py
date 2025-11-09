import subprocess
import os
import stat
import platform
import shutil
from PyPDF2 import PdfMerger
from werkzeug.utils import secure_filename

def doc_to_pdf(input_doc, output_dir):
    # Detect OS and set LibreOffice executable accordingly
    system_name = platform.system()
    if system_name == "Windows":
        libreoffice_cmd = r"C:\\Program Files\\LibreOffice\\program\\soffice.exe"  # adjust path if needed
    elif system_name == "Linux":
        libreoffice_cmd = "libreoffice"
    else:
        raise Exception(f"Unsupported OS: {system_name}")

    subprocess.run([
        libreoffice_cmd, '--headless', '--convert-to', 'pdf',
        '--outdir', output_dir, input_doc
    ], check=True)

def merge_pdfs(pdf_list, output_path):
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()

def convert_multiple_doc_to_pdf(file_storage_list, pdf_filename, output_pdf_path=None):
    
    os.makedirs(output_pdf_path, exist_ok=True)  # create output folder if not present
    current_path = os.getcwd()
    output_pdf_path = os.path.join(current_path, output_pdf_path)
    print("Current Working Directory:", current_path)
    print("output_pdf_path:", output_pdf_path)
    os.chmod(output_pdf_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    doc_files = []
    for file_storage in file_storage_list:
        filename = secure_filename(file_storage.filename)
        save_path = os.path.join(output_pdf_path, filename)
        print('-> '+save_path)
        doc_files.append(save_path)

    pdf_files = []
    for doc in doc_files:
        doc_to_pdf(doc, output_pdf_path)
        base_name = os.path.splitext(os.path.basename(doc))[0] + '.pdf'
        print('')
        print('base_name: ' +base_name)
        pdf_files.append(os.path.join(output_pdf_path, base_name))

    

    #first_file = pdf_files[0]
    #filename_without_ext = os.path.splitext(os.path.basename(first_file))[0]
    #print(filename_without_ext)
    #output_pdf_path = os.path.join(output_pdf_path, filename_without_ext+'_Merged.pdf')
    merge_pdfs(pdf_files, os.path.join(output_pdf_path,pdf_filename))

#pdfff_files = []
#convert_multiple_doc_to_pdf()

def convert_doc_to_pdf(input_doc_path, output_pdf_name, output_dir):
    os.makedirs(output_dir, exist_ok=True)  # create output folder if not present
    
    current_path = os.getcwd()
    output_dir = os.path.join(current_path, output_dir)
    print("Current Working Directory:", current_path)
    print("output_dir:", output_dir)
    os.chmod(output_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    doc_path = os.path.join(current_path, input_doc_path)
    
    print("doc_path:", doc_path)
    
    # Detect OS and set LibreOffice executable accordingly
    system_name = platform.system()
    if system_name == "Windows":
        libreoffice_cmd = r"C:\\Program Files\\LibreOffice\\program\\soffice.exe"  # adjust path if needed
    elif system_name == "Linux":
        libreoffice_cmd = "libreoffice"
    else:
        raise Exception(f"Unsupported OS: {system_name}")

    try:
        # Run LibreOffice headless to convert the DOC file
        subprocess.run([
            libreoffice_cmd,
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_dir,
            doc_path
        ], check=True)

        # LibreOffice names output file like input base name with .pdf extension
        base_name = os.path.splitext(os.path.basename(input_doc_path))[0]
        default_pdf_path = os.path.join(output_dir, base_name + ".pdf")
        
        # Rename/move to desired output PDF file name
        custom_pdf_path = os.path.join(output_dir, output_pdf_name)
        shutil.move(default_pdf_path, custom_pdf_path)

        print(f"Converted {default_pdf_path} to PDF in {custom_pdf_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting file: {e}")

# Example usage
#input_doc = "C_MATERIAL.doc"  # Path to your DOC file
#output_folder = "pdf_output"

#convert_doc_to_pdf(input_doc, output_folder)
