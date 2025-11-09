import fitz
from utils import zip_directory
import os
import stat

def pdf_to_jpg_pymupdf(pdf_path, zip_filename, output_pdf_path):
    
    current_path = os.getcwd()
    print("Current Working Directory:", current_path)
    folder_path = current_path+'\\'+output_pdf_path
    if not os.path.exists(folder_path):
        print('###### Folder not exist #######')
        os.makedirs(folder_path)
    os.chmod(folder_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
   
    dpi=150
    #os.makedirs(output_dir, exist_ok=True)
    
    doc = fitz.open(pdf_path)
    zoom = dpi / 72  # Calculate zoom factor
    matrix = fitz.Matrix(zoom, zoom)
    
    filename_without_ext = os.path.splitext(os.path.basename(zip_filename))[0]
    folder_path = folder_path+'//'+filename_without_ext
    os.makedirs(folder_path, exist_ok=True)

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # Get pixmap with RGB format for JPG
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        
        output_path = os.path.join(folder_path, f'page_{page_num+1:03d}.jpg')
        pix.save(output_path, output='jpeg', jpg_quality=95)
        print(f'Saved: {output_path}')
    
    doc.close()

    
    zip_directory(folder_path, folder_path+'.zip')
    print('Successfully converted pdf to image')
    return output_pdf_path
    #print(f"Conversion complete! {len(doc)} pages converted.")

# Usage
#pdf_to_jpg_pymupdf('eVisaTaha.pdf', dpi=300)
# Example usage
#convert_pdf_to_images('eVisaTaha.pdf')