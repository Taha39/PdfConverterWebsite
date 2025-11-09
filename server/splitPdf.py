from PyPDF2 import PdfReader, PdfWriter
import os
import stat
from utils import zip_directory
import shutil

# def split_pdf_pypdff2(input_pdf, output_prefix, pages_per_split):
#     reader = PdfReader(input_pdf)
#     total_pages = len(reader.pages)
    
#     for i in range(0, total_pages, pages_per_split):
#         print('i: ',i)
#         writer = PdfWriter()
        
#         # Add pages for this split
#         for page_num in range(i, min(i + pages_per_split, total_pages)):
#             writer.add_page(reader.pages[page_num])
        
#         # Save the split
#         output_filename = f"{output_prefix}_{i//pages_per_split + 1}.pdf"
#         with open(output_filename, 'wb') as output_file:
#             writer.write(output_file)
        
#         print(f"Created: {output_filename}")
        
#Usage
#split_pdf_pypdff2("Parents_Consent.pdf", "output", 1)  # Split every 1 pages


def split_pdf_pypdf2(input_pdf, output_prefix, output_pdf_path, pages_per_split):
    current_path = os.getcwd()
    print("Current Working Directory:", current_path)
    folder_path = current_path+'\\'+output_pdf_path
    if not os.path.exists(folder_path):
        print('###### Folder not exist #######')
        os.makedirs(folder_path)
    os.chmod(folder_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    
    print("input_pdf: ", input_pdf)
    try:
        # Validate input file
        if not os.path.exists(input_pdf):
            raise FileNotFoundError(f"PDF file not found: {input_pdf}")
        print("*** TAHA : " +input_pdf)
    
        reader = PdfReader(input_pdf)
        total_pages = len(reader.pages)
        print("*** total_pages : ", total_pages)
        output_prefix = folder_path+'\\'+output_prefix
        for i in range(0, total_pages, pages_per_split):
            print('i: ',i)
            writer = PdfWriter()
            
            # Add pages for this split
            for page_num in range(i, min(i + pages_per_split, total_pages)):
                writer.add_page(reader.pages[page_num])
            
            # Save the split
            output_filename = f"{output_prefix}_{i//pages_per_split + 1}.pdf"
            with open(output_filename, 'wb') as output_file:
                writer.write(output_file)
            
            print(f"Created: {output_filename}")

        os.remove(input_pdf)  
        zip_directory(folder_path, '.\SplitPdf.zip')
        shutil.copy('SplitPdf.zip', folder_path)
        os.remove('SplitPdf.zip') 

        return output_pdf_path
    except Exception as e:
        print(f"Error spliting pdf: {str(e)}")
        return None