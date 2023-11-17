import threading
import tempfile
import kmbotos as kmos
import shutil

write_lock = threading.Lock()


def read_proxies_from_file(file_path):
    with open(file_path, "r") as file:
        proxies = [line.strip() for line in file.readlines()]
    return proxies


def create_temporary_directory():
    return tempfile.mkdtemp()


def urls_to_create_count(file_path, required_count=8):
    low_count_urls = 0
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if not line:  # Check if the line is not empty
                    continue  # Skip to the next iteration if the line is empty
                _, _, count = line.split(",")
                if int(count) < 380:
                    low_count_urls += 1
    except FileNotFoundError:
        pass  # File doesn't exist, so consider it as having 0 low count URLs.
    except Exception as e:
        print(f"An error occurred: {e}")
    return (
        required_count - low_count_urls
    )  # Return the number of new accounts to create


def update_url_data(file_path, chosenurl):
    with write_lock:  # Acquire the lock
        found = False
        temp_file_path = file_path + ".tmp"

        with open(file_path, "r") as original:
            with open(temp_file_path, "w") as temp:
                for line in original:
                    email, url, count = line.strip().split(",")
                    if url == chosenurl:
                        count = str(int(count) + 20)
                        found = True
                    temp.write(f"{email},{url},{count}\n")

                if not found:
                    temp.write(f"unknown@email.com,{chosenurl},1\n")

            # Rename the temporary file to replace the original file
            shutil.move(temp_file_path, file_path)


def extract_urls_from_file(file_path):
    urls = []
    url_data = []
    totalcount = 0

    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if not line:  # Check if the line is not empty
                    continue

                # Split each line by the comma
                parts = line.split(",")

                # Ensure that there are enough parts in the line
                if len(parts) >= 3:
                    # Extract the email, url, and count from each line
                    email, url, count = parts[0], parts[1], int(parts[2])
                    url_data.append((email, url, count))
                    totalcount += count

                    # Check if the count is less than 380
                    if count < 380:
                        # If it is, add the URL to the list
                        urls.append(url)

    except FileNotFoundError:
        pass  # Handle the case where the file doesn't exist
    except Exception as e:
        print(f"An error occurred: {e}")
        kmos.restart_program()

    return urls, totalcount
