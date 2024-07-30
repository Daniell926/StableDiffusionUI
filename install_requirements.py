import subprocess
import sys
import pkg_resources

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

install_requirements()
