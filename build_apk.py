import os
import subprocess
import re
from datetime import datetime
import shutil
import sys

def get_pubspec_info():
    """Reads name and version from pubspec.yaml using regex to avoid dependencies."""
    if not os.path.exists("pubspec.yaml"):
        print("Error: pubspec.yaml not found in the current directory.")
        sys.exit(1)
        
    with open("pubspec.yaml", 'r') as f:
        content = f.read()
        name_match = re.search(r"^name:\s+([^\s#]+)", content, re.MULTILINE)
        version_match = re.search(r"^version:\s+([^\s#]+)", content, re.MULTILINE)
        
        name = name_match.group(1).strip() if name_match else "flutter_app"
        version = version_match.group(1).strip() if version_match else "1.0.0"
        
        # Replace characters that might be problematic in filenames
        version = version.replace("+", "_").replace(".", "-")
        return name, version

def run_flutter_build():
    """Runs the flutter build apk command."""
    print("Running Flutter build APK (release)...")
    try:
        # We use shell=True for Windows compatibility with flutter command
        # if it's in the user's path.
        result = subprocess.run(["flutter", "build", "apk", "--release"], 
                              check=True, 
                              capture_output=True, 
                              text=True)
        print("Build successful.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during Flutter build:\n{e.stderr}")
        return False
    except FileNotFoundError:
        print("Error: 'flutter' command not found. Make sure Flutter is installed and in your PATH.")
        return False

def rename_and_move_apk(name, version):
    """Locates the built APK and renames it with name, version, and timestamp."""
    # Default Flutter APK output path
    default_path = os.path.join("build", "app", "outputs", "flutter-apk", "app-release.apk")
    
    if not os.path.exists(default_path):
        print(f"Error: Could not find the built APK at {default_path}")
        return
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Construct new name
    new_filename = f"{name}_v{version}_{timestamp}.apk"
    output_dir = os.path.join("build", "app", "outputs", "flutter-apk")
    target_path = os.path.join(output_dir, new_filename)
    
    try:
        shutil.copy2(default_path, target_path)
        print(f"Success! APK saved as: {new_filename}")
        print(f"Location: {target_path}")
    except Exception as e:
        print(f"Error while renaming/copying APK: {e}")

def main():
    # 1. Get info from pubspec.yaml
    name, version = get_pubspec_info()
    print(f"App: {name}, Version: {version}")
    
    # 2. Build the APK
    if run_flutter_build():
        # 3. Rename and move
        rename_and_move_apk(name, version)

if __name__ == "__main__":
    main()
