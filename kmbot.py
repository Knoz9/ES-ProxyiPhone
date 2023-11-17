import os
import threading
from queue import Queue
import time
import random
import shutil
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
import kmbotdriver as kmdriver
import kmbotfilemanager as filemanager
import kmbothumanize as humanfunctions
import kmbotos as kmos
import win32file
import win32con
import kmnames as kmnames


global passes, nonpasses, sleeptime12, sleeptime, sleeptime22, sleeptime2, sleeptimek1, sleeptimek2
passes, nonpasses = 0, 0
sleeptime12, sleeptime = 0.2, 1.5  # default 0.2, 1.5
sleeptime22, sleeptime2 = 0.5, 2  # default 1, 2
sleeptimek1, sleeptimek2 = 0.01, 0.1
threadcount = 1
feed_name = "ddd"
tickets_topic = "temperature"
passes_lock = threading.Lock()
nonpasses_lock = threading.Lock()

sleeptimecomp, sleeptimecomp2 = 4, 5  # (M2 4,5) (Air 2012 6,7)

# Example usage:
# driver = webdriver.Chrome()
# driver.get('https://example.com')
# smooth_scroll(driver)

# Example usage:
# smooth_scroll_to_element(driver_instance, some_element)
import os
import shutil
import win32api
import win32con


import subprocess

def delete_with_powershell(path):
    # Step 1: More Aggressive PowerShell Method
    command = [
        "powershell",
        "-Command",
        f"Get-ChildItem -Path '{path}' -Recurse | Remove-Item -Force -Recurse; Remove-Item -Force -Recurse '{path}'"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if result.returncode == 0:
            print(f"Successfully deleted {path}")
        else:
            print(f"Failed to delete {path} using PowerShell. Reason: {result.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Step 2: Python Fallback
    if os.path.exists(path):
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            print(f"Successfully deleted {path} using Python.")
        except Exception as e:
            print(f"Failed to delete {path} using Python. Reason: {e}")

def run_script_in_threads(num_threads=5):
    threads = []
    results = Queue()

    def worker():
        result1, result2, result3 = run_script()
        results.put((result1, result2, result3))

    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)
        time.sleep(random.uniform(sleeptime22, sleeptime2))

    for thread in threads:
        thread.join(timeout=60)

    # Get the last result
    last_result1, last_result2, last_result3 = None, None, None
    while not results.empty():
        last_result1, last_result2, last_result3 = results.get()

    return last_result1, last_result2, last_result3


screen_resolutions = [
    (1920, 1080),  # Full HD
    (1366, 768),
    (1280, 1024),
    (1440, 900),
    (1600, 900),
    (1280, 800),
    (1024, 768),
    (1680, 1050),
    (1280, 720),  # HD
]


def createNewAccount():
    # Add code here to create an account.
    return


def run_script():
    # Add code on what to do on the website.
    return