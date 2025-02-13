import os
import subprocess
import sys

def check_python_version():
    """Ensure the correct Python version (3.10) is installed."""
    print("Checking Python 3.10 installation...")
    try:
        subprocess.run(["python3.10", "--version"], check=True, stdout=subprocess.PIPE)
        print("Python 3.10 is installed.")
    except subprocess.CalledProcessError:
        print("Python 3.10 is not installed. Installing via Homebrew...")
        subprocess.run(["brew", "install", "python@3.10"], check=True)
        print("Python 3.10 installed successfully.")

def create_virtual_environment():
    """Create a virtual environment with Python 3.10."""
    print("Setting up the virtual environment...")
    if os.path.exists("venv"):
        print("Removing existing virtual environment...")
        subprocess.run(["rm", "-rf", "venv"], check=True)
    subprocess.run(["python3.10", "-m", "venv", "venv"], check=True)
    print("Virtual environment created.")

def install_dependencies():
    """Activate the virtual environment and install dependencies."""
    print("Activating the virtual environment and installing dependencies...")
    venv_bin = os.path.join(os.getcwd(), "venv", "bin")
    activate_script = os.path.join(venv_bin, "activate")

    # Construct the command to install dependencies in the activated environment
    required_packages = [
        "sentence-transformers",
        "torch",
        "transformers",
        "selenium",
        "beautifulsoup4",
        "requests",
    ]

    # Run the commands in the activated environment
    commands = [
        f"source {activate_script}",
        f"{os.path.join(venv_bin, 'pip')} install --upgrade pip",
        f"{os.path.join(venv_bin, 'pip')} install " + " ".join(required_packages),
    ]

    # Execute the commands in a shell
    process = subprocess.run(" && ".join(commands), shell=True, executable="/bin/bash")
    if process.returncode == 0:
        print("Dependencies installed successfully within the virtual environment.")
    else:
        print("Failed to install dependencies. Please check the logs for more details.")

def main():
    check_python_version()
    create_virtual_environment()
    install_dependencies()
    print("\nSetup complete! The virtual environment is ready and dependencies are installed.")

if __name__ == "__main__":
    main()