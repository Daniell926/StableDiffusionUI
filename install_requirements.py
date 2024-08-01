import subprocess
import sys
import pkg_resources
import os

def run_command(command):
    """Run a command and check for errors."""
    result = subprocess.run(command, check=True)
    return result.returncode

def install_requirements():
    try:
        # Check if all packages are already installed
        with open('requirements.txt', 'r') as f:
            requirements = f.readlines()

        pkg_resources.require(requirements)
        print("All packages are already installed.")
    except pkg_resources.DistributionNotFound:
        print("Some packages are missing. Installing them now...")
        # Install the requirements using pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Installation complete.")
    except pkg_resources.VersionConflict:
        print("Some packages have version conflicts. Installing them now...")
        # Install the requirements using pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Installation complete.")

def clone_repo(repo_url, target_dir):
    # Check if the directory already exists
    item = os.path.join(target_dir, "stable-diffusion-v1-5")
    if not os.path.exists(item):
        print(f"{item} does not exist. Cloning repository...")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        try:
            # Ensure Git LFS is installed and initialized
            run_command(['git', 'lfs', 'install'])
            
            # Run the git clone command
            run_command(['git', 'clone', repo_url, target_dir])
            print("Repository successfully cloned.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to run command: {e}")
    else:
        print(f"{item} already exists. Skipping clone.")

repo_url = "https://huggingface.co/runwayml/stable-diffusion-v1-5"
target_dir = "models/Stable-Diffusion"

clone_repo(repo_url, target_dir)

install_requirements()
