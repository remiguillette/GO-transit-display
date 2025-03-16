#!/usr/bin/env python3
import os
import subprocess
import shutil
import re
from pathlib import Path

def clone_repository(repo_url, target_dir="repo_clone"):
    """Clone the GitHub repository to a local directory."""
    # Remove the directory if it already exists
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    
    # Make sure parent directory exists
    os.makedirs(target_dir, exist_ok=True)
    
    # Clone the repository
    print(f"Cloning repository {repo_url} to {target_dir}...")
    try:
        # First attempt with regular git clone
        subprocess.run(["git", "clone", repo_url, target_dir], check=True)
    except Exception as e:
        print(f"Standard git clone failed with error: {e}")
        # If that fails, try to use a different approach
        try:
            # Remove any partial clone that might exist
            shutil.rmtree(target_dir)
            os.makedirs(target_dir, exist_ok=True)
            
            # Use curl to download the repository as a zip file
            zip_path = f"{target_dir}.zip"
            github_zip_url = f"{repo_url[:-4]}/archive/refs/heads/main.zip"
            print(f"Attempting to download repository as ZIP from {github_zip_url}")
            subprocess.run(["curl", "-L", github_zip_url, "-o", zip_path], check=True)
            
            # Extract the zip file
            subprocess.run(["unzip", zip_path, "-d", "."], check=True)
            
            # Find the extracted directory
            extracted_dir = None
            for item in os.listdir("."):
                if os.path.isdir(item) and "GO-transit-display" in item:
                    extracted_dir = item
                    break
            
            if extracted_dir:
                # Rename the extracted directory to the target directory
                if os.path.exists(target_dir):
                    shutil.rmtree(target_dir)
                shutil.move(extracted_dir, target_dir)
                
                # Clean up the zip file
                os.remove(zip_path)
            else:
                raise Exception("Could not find extracted directory")
        except Exception as zip_error:
            print(f"ZIP download approach also failed: {zip_error}")
            # If both approaches fail, try a manual approach
            try:
                # Remove any partial directories
                if os.path.exists(target_dir):
                    shutil.rmtree(target_dir)
                os.makedirs(target_dir, exist_ok=True)
                
                # Use the GitHub API to download the repo contents
                print("Attempting to use GitHub API to download repository contents...")
                subprocess.run([
                    "bash", "-c", 
                    f"mkdir -p {target_dir} && cd {target_dir} && curl -s https://api.github.com/repos/remiguillette/GO-transit-display/git/trees/main?recursive=1 | grep -o '\"path\":\"[^\"]*\"' | sed 's/\"path\":\"//g' | sed 's/\"//g' | xargs -I {{}} -n 1 sh -c 'mkdir -p $(dirname \"{{}}\") && curl -s https://raw.githubusercontent.com/remiguillette/GO-transit-display/main/{{}} > {{}} || true'"
                ], check=True)
            except Exception as api_error:
                print(f"GitHub API approach also failed: {api_error}")
                raise Exception("All repository download methods failed")
    
    print("Repository download completed successfully.")
    return target_dir

def find_markdown_files(directory):
    """Find all markdown files in the repository."""
    markdown_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.md', '.markdown')):
                markdown_files.append(os.path.join(root, file))
    
    return markdown_files

def read_file_content(file_path):
    """Read the content of a file."""
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        return file.read()

def analyze_file_structure(directory):
    """Analyze the file structure of the repository."""
    file_types = {}
    total_files = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            total_files += 1
            _, ext = os.path.splitext(file)
            ext = ext.lower()
            
            if ext in file_types:
                file_types[ext] += 1
            else:
                file_types[ext] = 1
    
    return {
        "total_files": total_files,
        "file_types": file_types
    }

def find_dependencies(directory):
    """Find project dependencies by examining common dependency files."""
    dependency_files = {
        "package.json": "JavaScript/Node.js",
        "requirements.txt": "Python",
        "Gemfile": "Ruby",
        "pom.xml": "Java (Maven)",
        "build.gradle": "Java/Kotlin (Gradle)",
        "go.mod": "Go",
        "Cargo.toml": "Rust",
        "composer.json": "PHP"
    }
    
    found_dependencies = {}
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file in dependency_files:
                file_path = os.path.join(root, file)
                content = read_file_content(file_path)
                found_dependencies[file] = {
                    "type": dependency_files[file],
                    "path": file_path,
                    "content": content
                }
    
    return found_dependencies

def extract_setup_instructions(markdown_content):
    """Extract setup and installation instructions from markdown content."""
    setup_patterns = [
        r"(?i)## (installation|setup|getting started).*?(?=^##|\Z)",
        r"(?i)# (installation|setup|getting started).*?(?=^#|\Z)",
        r"(?i)### (installation|setup|getting started).*?(?=^###|\Z)",
    ]
    
    instructions = []
    
    for pattern in setup_patterns:
        matches = re.findall(pattern, markdown_content, re.MULTILINE | re.DOTALL)
        if matches:
            for match in matches:
                instructions.append(match.strip())
    
    return instructions

def generate_analysis_report(repo_url, clone_dir):
    """Generate a comprehensive analysis report of the repository."""
    # Find all markdown files
    markdown_files = find_markdown_files(clone_dir)
    
    # Read content of each markdown file
    markdown_contents = {}
    for file_path in markdown_files:
        relative_path = os.path.relpath(file_path, clone_dir)
        markdown_contents[relative_path] = read_file_content(file_path)
    
    # Analyze file structure
    structure_analysis = analyze_file_structure(clone_dir)
    
    # Find dependencies
    dependencies = find_dependencies(clone_dir)
    
    # Extract setup instructions from markdown files
    setup_instructions = {}
    for file_path, content in markdown_contents.items():
        instructions = extract_setup_instructions(content)
        if instructions:
            setup_instructions[file_path] = instructions
    
    # Generate the report
    report = "# GO-transit-display Repository Analysis\n\n"
    report += f"## Repository URL\n{repo_url}\n\n"
    
    report += "## Markdown Files Analysis\n"
    if markdown_contents:
        for file_path, content in markdown_contents.items():
            report += f"### {file_path}\n"
            
            # Extract title if available
            title_match = re.search(r"# ([^\n]+)", content)
            if title_match:
                report += f"**Title:** {title_match.group(1)}\n\n"
            
            # Extract first paragraph as summary if available
            summary_match = re.search(r"# [^\n]+\n+([^\n#]+)", content)
            if summary_match:
                report += f"**Summary:** {summary_match.group(1).strip()}\n\n"
            
            # Include full content for reference
            report += "**Content:**\n```markdown\n"
            report += content
            report += "\n```\n\n"
    else:
        report += "No markdown files found in the repository.\n\n"
    
    report += "## File Structure Analysis\n"
    report += f"Total files: {structure_analysis['total_files']}\n\n"
    report += "File types:\n"
    for ext, count in structure_analysis['file_types'].items():
        report += f"- {ext or 'No extension'}: {count} files\n"
    report += "\n"
    
    report += "## Dependencies\n"
    if dependencies:
        for file, info in dependencies.items():
            report += f"### {file} ({info['type']})\n"
            report += f"Path: {info['path']}\n"
            report += "Content preview:\n```\n"
            content_preview = info['content'][:500] + "..." if len(info['content']) > 500 else info['content']
            report += content_preview
            report += "\n```\n\n"
    else:
        report += "No standard dependency files found.\n\n"
    
    report += "## Setup Instructions\n"
    if setup_instructions:
        for file_path, instructions in setup_instructions.items():
            report += f"### From {file_path}\n"
            for instruction in instructions:
                report += instruction + "\n\n"
    else:
        report += "No explicit setup instructions found in markdown files.\n\n"
    
    report += "## Project Summary\n"
    readme_path = "README.md"
    if readme_path in markdown_contents:
        # Extract project purpose from README
        purpose_match = re.search(r"# [^\n]+\n+([^\n#]+)", markdown_contents[readme_path])
        if purpose_match:
            report += f"**Purpose:** {purpose_match.group(1).strip()}\n\n"
        
        # Try to identify features
        features_match = re.search(r"(?i)## features.*?(?=^##|\Z)", markdown_contents[readme_path], re.MULTILINE | re.DOTALL)
        if features_match:
            report += "**Features:**\n" + features_match.group(0) + "\n\n"
    else:
        report += "No README.md found to extract project summary.\n\n"
    
    report += "## Conclusion\n"
    report += "This analysis provides an overview of the GO-transit-display repository structure, "
    report += "documentation, and dependencies without modifying any code. For a more detailed understanding, "
    report += "it's recommended to review the actual code and functionality implementation.\n"
    
    return report

def main():
    """Main function to clone and analyze the repository."""
    repo_url = "https://github.com/remiguillette/GO-transit-display.git"
    clone_dir = clone_repository(repo_url)
    
    analysis_report = generate_analysis_report(repo_url, clone_dir)
    
    # Write the analysis report to a markdown file
    with open("analysis_results.md", "w", encoding="utf-8") as file:
        file.write(analysis_report)
    
    print(f"Analysis completed and saved to analysis_results.md")

if __name__ == "__main__":
    main()
