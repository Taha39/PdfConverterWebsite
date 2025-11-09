from fpdf import FPDF
import os
import stat

def txt_to_pdf(input_txt_path, output_pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    with open(input_txt_path, 'r', encoding='utf-8') as file:
        for line in file:
            pdf.cell(0, 10, txt=line.strip(), ln=True)

    pdf.output(output_pdf_path)
    print(f"PDF generated successfully: {output_pdf_path}")

def multiple_txt_to_single_pdf(txt_files, output_pdf_path):
    pdf = FPDF()
    pdf.set_font("Arial", size=12)
    
    for txt_file in txt_files:
        pdf.add_page()
        pdf.cell(0, 10, txt=os.path.basename(txt_file), ln=True)  # Optional: title with file name
        
        with open(txt_file, 'r', encoding='utf-8') as file:
            for line in file:
                pdf.cell(0, 10, txt=line.strip(), ln=True)
    
    pdf.output(output_pdf_path)
    print(f"Combined PDF generated successfully: {output_pdf_path}")
    
# Usage example
#txt_to_pdf('input.txt', 'output.pdf')

def convert_txt_to_pdf(input_txt_path, output_pdf_name, output_pdf_path):
    os.makedirs(output_pdf_path, exist_ok=True)  # create output folder if not present
    
    current_path = os.getcwd()
    output_pdf_path = os.path.join(current_path, output_pdf_path)
    print("Current Working Directory:", current_path)
    print("output_pdf_path:", output_pdf_path)
    os.chmod(output_pdf_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    txt_path = os.path.join(current_path, input_txt_path)

    print("input_txt_path: ", input_txt_path)
    try:
        # Validate input file
        if not os.path.exists(input_txt_path):
            raise FileNotFoundError(f"Image file not found: {input_txt_path}")
        print("*** TAHA : " +input_txt_path)
        
        # Convert image to PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        with open(input_txt_path, 'r', encoding='utf-8') as file:
            for line in file:
                pdf.cell(0, 10, txt=line.strip(), ln=True)

        output_pdf_file = os.path.join(output_pdf_path,output_pdf_name)
        pdf.output(output_pdf_file)
        print(f"PDF generated successfully: {output_pdf_file}")      
        
        return output_pdf_path
        
    except Exception as e:
        print(f"Error converting single image: {str(e)}")
        return None
    
