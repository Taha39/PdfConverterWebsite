from pdf2docx import Converter
import os
import stat
###############################################################
#NOTE : To fix get_area() error, we need to use this version:
#          pip install pymupdf==1.26.4
################################################################

def pdf_to_doc_pdf2docx(pdf_path, doc_filename, output_pdf_path):

    current_path = os.getcwd()
    print("Current Working Directory:", current_path)
    folder_path = current_path+'\\'+output_pdf_path
    if not os.path.exists(folder_path):
        print('###### Folder not exist #######')
        os.makedirs(folder_path)
    os.chmod(folder_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    print("pdf_path: ", pdf_path)
    try:
        # Validate input file
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Image file not found: {pdf_path}")
        print("*** TAHA : " +pdf_path)
        
        # Convert PDF to DOC
        cv = Converter(pdf_path)
        cv.convert(folder_path+'\\'+doc_filename)
        cv.close()
       
        print(f"Successfully converted '{pdf_path}' to '{output_pdf_path}'")
        return output_pdf_path
        
    except Exception as e:
        print(f"Error converting single image: {str(e)}")
        return None


# Simplest conversion
#Converter('TahaResumeLonConvert.pdf').convert('output.docx')
# cv = Converter('Parents_Consent.pdf')
# cv.convert('output.docx')
# cv.close()
#pdf_to_docx_advanced('TahaResumeLonConvert.pdf', 'output.docx')