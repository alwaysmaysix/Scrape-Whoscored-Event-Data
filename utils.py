import os
import re
import subprocess

def extract_version_registry(output):
    try:
        google_version = ''
        for letter in output[output.rindex('DisplayVersion    REG_SZ') + 24:]:
            if letter != '\n':
                google_version += letter
            else:
                break
        return google_version.strip()
    except (TypeError, ValueError) as e:
        return None

def extract_version_folder():
    possible_paths = [
        '/usr/bin/google-chrome',                    # Default path on many Linux distros
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # Default path on macOS
        '/usr/local/bin/google-chrome',              # Another common path on Linux
    ]

    for path in possible_paths:
        if os.path.exists(path):
            version = os.popen(f"{path} --version").read().strip('Google Chrome ').strip()
            return version
    return None

def get_chrome_version():
    version = None

    if platform.startswith("linux"):
        # Assuming Chrome is installed in the typical location in Colab.
        version = extract_version_folder()

    elif platform == "darwin":
        # OS X
        version = extract_version_folder()

    elif platform == "win32":
        # Windows - Note: Colab doesn't natively support Windows, so this is for reference.
        try:
            # Try registry key.
            stream = os.popen('reg query "HKLM\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Google Chrome"')
            output = stream.read()
            version = extract_version_registry(output)
        except Exception as ex:
            # Try folder path.
            version = extract_version_folder()

    if not version:
        version = "Google Chrome not found or couldn't determine the version."

    return version


