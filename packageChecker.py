import argparse
import ast
import subprocess
import sys


def extract_required_packages(file_path):
    # Open the Python file and parse its contents into an abstract syntax tree (AST)
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    # Set to store the required packages
    required_packages = set()

    # Traverse the AST nodes to find import statements
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            # For regular imports, add the package name to the set
            for alias in node.names:
                required_packages.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            # For relative imports, add the module and package names to the set
            module_name = node.module.split('.')[0]
            for alias in node.names:
                required_packages.add(
                    module_name + '.' + alias.name.split('.')[0])

    # Convert the set of required packages to a list and return
    return list(required_packages)


def check_and_install_packages(package_list):
    # List to store missing packages
    missing_packages = []

    # Check if each package is installed
    for package in package_list:
        try:
            # Check if the package is installed using pip's show command
            subprocess.check_output(
                [sys.executable, '-m', 'pip', 'show', package])
        except subprocess.CalledProcessError:
            # Package is not installed, add it to the missing_packages list
            missing_packages.append(package)

    # If there are missing packages, install them
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        install_packages(missing_packages)
    else:
        print("All packages are installed!")


def install_packages(package_list):
    try:
        # Install packages using pip's install command
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', *package_list])
        print("Packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing packages: {e}")


def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description='Check and install required packages.')
    parser.add_argument('file_path', type=str,
                        help='Path to the Python file to analyze')
    args = parser.parse_args()

    # Extract required packages from the Python file
    required_packages = extract_required_packages(args.file_path)

    # Call the function to check and install packages
    check_and_install_packages(required_packages)


if __name__ == '__main__':
    # Call the main function when the script is executed directly
    main()
