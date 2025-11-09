from PyPDF2 import PdfMerger
import os
import stat
from werkzeug.utils import secure_filename

# def merge_pdfs_safe(pdf_list, output_filename):
#     merger = PdfMerger()
    
#     try:
#         for pdf in pdf_list:
#             if os.path.exists(pdf):
#                 print(f"Adding {pdf}...")
#                 merger.append(pdf)
#             else:
#                 print(f"Warning: {pdf} not found, skipping...")
        
#         merger.write(output_filename)
#         print(f"Successfully merged {len(pdf_list)} files into {output_filename}")
        
#     except Exception as e:
#         print(f"Error occurred: {e}")
        
#     finally:
#         merger.close()

# Usage
#files_to_merge = ["output_1.pdf", "output_2.pdf", "output_3.pdf"]
#merge_pdfs_safe(files_to_merge, "combined_documents.pdf")

def merge_pdfs_safe(file_storage_list, output_filename, output_folder_path):
    current_path = os.getcwd()
    output_folder_path = os.path.join(current_path, output_folder_path)
    print("Current Working Directory:", current_path)
    print("output_folder_path:", output_folder_path)
    os.chmod(output_folder_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    pdf_list = []
    for file_storage in file_storage_list:
        filename = secure_filename(file_storage.filename)
        save_path = os.path.join(output_folder_path, filename)
        print('-> '+save_path)
        pdf_list.append(save_path)
        
    merger = PdfMerger()
    
    try:
        for pdf in pdf_list:
            if os.path.exists(pdf):
                print(f"Adding {pdf}...")
                merger.append(pdf)
            else:
                print(f"Warning: {pdf} not found, skipping...")
        
        merger.write(output_folder_path+'//'+output_filename)
        print(f"Successfully merged {len(pdf_list)} files into {output_filename}")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        
    finally:
        merger.close()