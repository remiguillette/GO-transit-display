
import os
import zipfile
from datetime import datetime

def create_project_archive():
    # Get current timestamp for the archive name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"go_transit_display_{timestamp}.zip"
    
    # Define project directories to include
    directories_to_archive = [
        'static',
        'templates',
        'attached_assets'
    ]
    
    # List of essential files to include
    files_to_archive = [
        # Python files
        'main.py',
        'scraper.py',
        'pyproject.toml',
        '.replit',
        'create_archive.py',
        
        # Documentation
        'UPDATE.md',
        'AI_GUIDELINES.md',
        'PROJECT_STRUCTURE.md',
    ]
    
    try:
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add individual files
            for file_path in files_to_archive:
                if os.path.exists(file_path):
                    zipf.write(file_path)
                    print(f"Added: {file_path}")
                else:
                    print(f"Warning: {file_path} not found")
            
            # Add entire directories
            for directory in directories_to_archive:
                if os.path.exists(directory):
                    for root, dirs, files in os.walk(directory):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path)
                            print(f"Added: {file_path}")
                else:
                    print(f"Warning: Directory {directory} not found")
        
        print(f"\nArchive created successfully: {archive_name}")
        print("The ZIP archive includes all essential project files:")
        print("- Python source files")
        print("- Documentation files")
        print("- Templates")
        print("- Static assets (CSS, fonts, icons)")
        print("\nTo extract the archive:")
        print(f"unzip {archive_name}")
        
        return archive_name
        
    except Exception as e:
        print(f"Error creating archive: {str(e)}")
        return None

if __name__ == "__main__":
    create_project_archive()
