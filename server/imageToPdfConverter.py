import img2pdf
import os
import stat
from pathlib import Path
from werkzeug.utils import secure_filename


def output_file_path(image_path):
    current_path = os.getcwd()
    print("Current Working Directory:", current_path)
    os.chmod(os.path.join(current_path, 'uploads'), 0o777)  # Safely join path
    print("image_path: ", image_path)
    
    # Get absolute image path if not already absolute
    if not os.path.isabs(image_path):
        image_path = os.path.join(current_path, image_path)
    
    # Validate input file
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    print("*** TAHA : " + image_path)
    
    # Create output PDF path
    image_name = Path(image_path).stem
    convertPdf = image_name + "Convert"
    output_pdf_path = os.path.join(current_path, 'uploads', f"{convertPdf}.pdf")
    print("Output PDF path:", output_pdf_path)
    return output_pdf_path
    
def convert_single_image_to_pdf(image_path, pdf_filename, output_pdf_path=None):
    current_path = os.getcwd()
    print("Current Working Directory:", current_path)
    folder_path = current_path+'\\'+output_pdf_path
    if not os.path.exists(folder_path):
        print('###### Folder not exist #######')
        os.makedirs(folder_path)
    os.chmod(folder_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    
    print("image_path: ", image_path)
    try:
        # Validate input file
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        print("*** TAHA : " +image_path)
        
        # Convert image to PDF
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        
        pdf_bytes = img2pdf.convert(image_data)
        # Save PDF
        with open(folder_path+'\\'+pdf_filename, "wb") as pdf_file:
            pdf_file.write(pdf_bytes)
        
        print(f"Successfully converted '{image_path}' to '{output_pdf_path}'")
        return output_pdf_path
        
    except Exception as e:
        print(f"Error converting single image: {str(e)}")
        return None

        
def convert_multiple_images_to_pdf(file_storage_list, pdf_filename, output_pdf_path=None):
    print('+++++++++++ convert_multiple_images_to_pdf +++++++++++')
    try:
        # Save all FileStorage to disk and get their paths
        current_path = os.getcwd()
        print("Current Working Directory:", current_path)
        folder_path = current_path+'\\'+output_pdf_path
        print('Folder path: '+folder_path)
        if not os.path.exists(folder_path):
            print('###### Folder not exist #######')
            os.makedirs(folder_path)
        os.chmod(folder_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        
        image_paths = []
        for file_storage in file_storage_list:
            filename = secure_filename(file_storage.filename)
            save_path = os.path.join(folder_path, filename)
            print('-> '+save_path)
            image_paths.append(save_path)
        
        print('Image saved in folder: '+folder_path)
        # Validate saved files
        for image_path in image_paths:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")

        print('Images are available in : '+folder_path)

        # Convert images to PDF using img2pdf with file paths
        with open(folder_path+'\\'+pdf_filename, "wb") as pdf_file:
            pdf_file.write(img2pdf.convert(image_paths))

        print(f"Successfully converted {len(image_paths)} images to '{output_pdf_path}'")
        return output_pdf_path

    except Exception as e:
        print(f"Error converting multiple images: {str(e)}")
        return None
