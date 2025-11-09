import fitz
import os
from PIL import Image
import io
import stat

###############################################################
#NOTE : To work with ghost script, we have to install Ghostscript
# from this site on windows: https://ghostscript.com/releases/gsdnld.html
################################################################
########################################################################
import subprocess
import os

def compress_pdf_ghostscript_bk(input_path, output_path, compression_level='medium'):
    """
    Compress PDF using Ghostscript - Most effective method
    """
    gs_settings = {
        'low': [
            '-dPDFSETTINGS=/printer',  # 300 DPI
            '-dColorImageResolution=150',
            '-dGrayImageResolution=150',
            '-dMonoImageResolution=300'
        ],
        'medium': [
            '-dPDFSETTINGS=/ebook',    # 150 DPI
            '-dColorImageResolution=150',
            '-dGrayImageResolution=150', 
            '-dMonoImageResolution=200'
        ],
        'high': [
            '-dPDFSETTINGS=/screen',   # 72 DPI
            '-dColorImageResolution=72',
            '-dGrayImageResolution=72',
            '-dMonoImageResolution=150'
        ]
    }
    
    gs_command = [
        'gswin64c',  # Use 'gswin64c' for 64-bit or 'gswin32c' for 32-bit installation
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
    ] + gs_settings[compression_level] + [
        f'-sOutputFile={output_path}',
        input_path
    ]
    
    try:
        result = subprocess.run(gs_command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Ghostscript error: {result.stderr}")
            return 0
        
        # Calculate compression ratio
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        return compression_ratio
        
    except Exception as e:
        print(f"Error running Ghostscript: {e}")
        return 0

#compress_pdf_ghostscript('input2.pdf', 'compressed_medium.pdf', compression_level='medium')
#compress_pdf_ghostscript('input2.pdf', 'compressed_low.pdf', compression_level='low')
#compress_pdf_ghostscript('input2.pdf', 'compressed_high.pdf', compression_level='high')

def compress_pdf_ghostscript(input_pdf, output_pdf, output_pdf_path, compression_level='medium'):
    current_path = os.getcwd()
    print("Current Working Directory:", current_path)
    folder_path = current_path+'\\'+output_pdf_path
    if not os.path.exists(folder_path):
        print('###### Folder not exist #######')
        os.makedirs(folder_path)
    os.chmod(folder_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    
    print("input_pdf: ", input_pdf)
    print("compression_level: ", compression_level)

    gs_settings = {
        'low': [
            '-dPDFSETTINGS=/printer',  # 300 DPI
            '-dColorImageResolution=150',
            '-dGrayImageResolution=150',
            '-dMonoImageResolution=300'
        ],
        'medium': [
            '-dPDFSETTINGS=/ebook',    # 150 DPI
            '-dColorImageResolution=150',
            '-dGrayImageResolution=150', 
            '-dMonoImageResolution=200'
        ],
        'high': [
            '-dPDFSETTINGS=/screen',   # 72 DPI
            '-dColorImageResolution=72',
            '-dGrayImageResolution=72',
            '-dMonoImageResolution=150'
        ]
    }
    
    gs_command = [
        'gswin64c',  # Use 'gswin64c' for 64-bit or 'gswin32c' for 32-bit installation
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
    ] + gs_settings[compression_level] + [
        f'-sOutputFile={folder_path+'\\'+output_pdf}',
        input_pdf
    ]

    try:
        result = subprocess.run(gs_command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Ghostscript error: {result.stderr}")
            return 0
        
        # Calculate compression ratio
        original_size = os.path.getsize(input_pdf)
        compressed_size = os.path.getsize(folder_path+'\\'+output_pdf)
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        return compression_ratio
        
    except Exception as e:
        print(f"Error running Ghostscript: {e}")
        return 0

########################################################################

def compress_pdf_images(input_pdf, output_pdf, max_image_quality=80, max_dpi=150):
    """
    Compress images inside PDF by lowering JPEG quality and DPI, then saving the PDF.
    """
    doc = fitz.open(input_pdf)
    # For each page
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            # Extract image
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]

            # Load image into Pillow
            try:
                image = Image.open(io.BytesIO(image_bytes))
            except Exception as e:
                print(f"Warning: Can't open image on page {page_num + 1}: {e}")
                continue

            # Resize if too high DPI (optional)
            if max_dpi and ('dpi' in base_image and base_image['dpi'][0] > max_dpi):
                factor = max_dpi / base_image['dpi'][0]
                new_size = (int(image.width * factor), int(image.height * factor))
                image = image.resize(new_size, Image.LANCZOS)

            # Re-compress image
            img_buf = io.BytesIO()
            if ext.lower() in ['jpg', 'jpeg']:
                image.save(img_buf, format='JPEG', quality=max_image_quality)
            else:
                image.save(img_buf, format=image.format)
            img_buf = img_buf.getvalue()

            # Get the area for re-insertion
            rects = page.get_image_rects(xref)
            if rects:
                page.add_redact_annot(rects[0])
                page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)
                page.insert_image(rects[0], stream=img_buf)
            else:
                print(f"Warning: No rect found for image {img_index} on page {page_num + 1}")

    doc.save(output_pdf, garbage=4, deflate=True)
    doc.close()
    print(f"Image compression completed: {output_pdf}")

# Usage
#compress_pdf_images("input.pdf", "compressed_images_high.pdf", max_image_quality=70)
#compress_pdf_images("input.pdf", "compressed_images_medium.pdf", max_image_quality=50)
#compress_pdf_images("input.pdf", "compressed_images_low.pdf", max_image_quality=10)


def compress_pdf(input_pdf, output_pdf, output_pdf_path, max_image_quality=80, max_dpi=150):
    current_path = os.getcwd()
    print("Current Working Directory:", current_path)
    folder_path = current_path+'\\'+output_pdf_path
    if not os.path.exists(folder_path):
        print('###### Folder not exist #######')
        os.makedirs(folder_path)
    os.chmod(folder_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    
    print("input_pdf: ", input_pdf)
    print("max_image_quality: ", max_image_quality)

    try:
        doc = fitz.open(input_pdf)
        # For each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                # Extract image
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                ext = base_image["ext"]

                # Load image into Pillow
                try:
                    image = Image.open(io.BytesIO(image_bytes))
                except Exception as e:
                    print(f"Warning: Can't open image on page {page_num + 1}: {e}")
                    continue

                # Resize if too high DPI (optional)
                if max_dpi and ('dpi' in base_image and base_image['dpi'][0] > max_dpi):
                    factor = max_dpi / base_image['dpi'][0]
                    new_size = (int(image.width * factor), int(image.height * factor))
                    image = image.resize(new_size, Image.LANCZOS)

                # Re-compress image
                img_buf = io.BytesIO()
                if ext.lower() in ['jpg', 'jpeg']:
                    image.save(img_buf, format='JPEG', quality=max_image_quality)
                else:
                    image.save(img_buf, format=image.format)
                img_buf = img_buf.getvalue()

                # Get the area for re-insertion
                rects = page.get_image_rects(xref)
                if rects:
                    page.add_redact_annot(rects[0])
                    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)
                    page.insert_image(rects[0], stream=img_buf)
                else:
                    print(f"Warning: No rect found for image {img_index} on page {page_num + 1}")

        doc.save(folder_path+'\\'+output_pdf, garbage=4, deflate=True)
        doc.close()
        print(f"Image compression completed: {output_pdf}")
        return output_pdf
    except Exception as e:
        print(f"Error compressing pdf: {str(e)}")
        return None
