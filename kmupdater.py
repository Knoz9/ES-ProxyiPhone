import os
import subprocess



def update_from_github():
    try:
        # Get the current working directory
        repo_path = os.getcwd()

        # Change to the directory where your repository is located
        os.chdir(repo_path)

        # Run git pull to fetch and merge updates
        result = subprocess.run(['git', 'pull'], capture_output=True, text=True)

        # Check the output for any issues
        if result.returncode != 0:
            print(f"Error pulling from GitHub: {result.stderr}")
        else:
            print(result.stdout)

    except Exception as e:
        print(f"An error occurred: {e}")
        
update_from_github()
