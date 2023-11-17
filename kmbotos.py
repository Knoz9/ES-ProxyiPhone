import sys
import subprocess


def restart_program():
    sys.exit(42)

def close_chrome_instances():
    try:
        if sys.platform == "darwin":  # macOS
            applescript = """
                tell application "Google Chrome"
                    quit
                end tell
            """
            subprocess.run(["osascript", "-e", applescript])
        elif sys.platform == "win32":  # Windows
            subprocess.run(["taskkill", "/IM", "chrome.exe", "/F"])
        print("Closed all Chrome instances")
    except Exception as e:
        print(f"Error while closing Chrome instances: {str(e)}")
