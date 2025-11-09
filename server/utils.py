import os
import uuid
import zipfile

def create_random_upload_folder():
    current_path = os.getcwd()                   # Get current directory
    uploads_folder = os.path.join(current_path, 'uploads')
    os.makedirs(uploads_folder, exist_ok=True)  # Create 'uploads' if it doesn't exist

    random_folder_name = str(uuid.uuid4()).replace('-', '_')       # Generate a random folder name (UUID)
    random_folder_path = os.path.join(uploads_folder, random_folder_name)

    os.makedirs(random_folder_path)              # Create the random folder

    return random_folder_name


def zip_directory(folder_path, output_zip_path):
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Store relative path in zip (folder structure is preserved)
                arcname = os.path.relpath(file_path, start=folder_path)
                zipf.write(file_path, arcname)
    print(f"Created zip file: {output_zip_path}")

