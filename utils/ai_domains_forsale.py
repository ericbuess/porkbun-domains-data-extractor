import os
import shutil

def copy_domains_json(src_path, dest_path):
    try:
        # Create the destination directory if it doesn't exist
        dest_dir = os.path.dirname(dest_path)
        os.makedirs(dest_dir, exist_ok=True)

        shutil.copy(src_path, dest_path)
        print(f"domains.json copied successfully from {src_path} to {dest_path}")
        return True
    except IOError as e:
        print(f"Error copying domains.json: {str(e)}")
        return False