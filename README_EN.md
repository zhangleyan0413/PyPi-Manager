# PyPi Manager

Full name: Python Pip Manager

Version: 1.2.0

A powerful Python environment management tool that simplifies Python installation, dependency management, pip troubleshooting, and mirror source configuration.

## Features

### 📦 pip Package Management
- Show installed packages
- Search for packages and display version information
- Install specific version of packages
- Upgrade packages to latest version
- Uninstall unnecessary packages
- Install packages from wheel files

### 🔧 pip Repair
- Check pip status
- Fix pip using ensurepip
- Install pip using get-pip.py script
- Automatically detect pip errors and suggest fixes

### 🚀 Mirror Source Configuration
- Built-in 5 recommended mirror sources (Tsinghua, USTC, Alibaba Cloud, Douban, Official)
- Add custom mirror sources
- Delete custom mirror sources
- Set default mirror source

### ⚡ Batch Package Management
- Batch update all updatable packages
- Batch uninstall multiple packages
- Export installed packages list to requirements.txt
- Install packages from requirements.txt file

### 🐍 Python Version Management
- Get available Python version list
- Install specific Python version
- Check installed Python versions and their paths

### 💡 Smart Features
- Added progress bars and loading animations for all time-consuming operations
- Support domestic mirror source acceleration
- Detailed error prompts and solutions
- Multi-threaded execution of time-consuming operations to avoid interface freezing

## Installation

1. **Download the program**
   - Clone or download this repository to your local machine
   - Ensure the downloaded file structure is complete

2. **Run initialization script**
   - Double-click to run `setup.bat` file
   - The script will automatically check Python installation status
   - If Python is not installed, it will automatically download and install
   - If Python is already installed, it will check and install required dependencies

3. **Start using**
   - After initialization, the program will start automatically
   - Follow the menu prompts to operate

## Usage

### Main Menu

```
PyPi Manager
1. Manage pip packages
2. Check and fix pip
3. Configure mirror sources
4. Batch package management
5. Python version management
6. About author
7. Exit
```

### pip Package Management Menu

```
pip Package Management Menu
1. Show installed packages
2. Search for packages
3. Install packages
4. Upgrade packages
5. Uninstall packages
6. Install packages from wheel files
7. Return to main menu
```

### Mirror Source Configuration Menu

```
Mirror Source Management Menu
1. Show current mirror source
2. Select built-in mirror source
3. Add custom mirror source
4. Delete custom mirror source
5. Set default mirror source
6. Return to main menu
```

### Batch Package Management Menu

```
Batch Package Management Menu
1. Check updatable packages
2. Batch update all packages
3. Batch uninstall packages
4. Export installed packages list
5. Install packages from file
6. Return to main menu
```

### Python Version Management Menu

```
Python Version Management Menu
1. Get available Python versions
2. Install specific version
3. Check installed Python versions
4. Return to main menu
```

## FAQ

### Q: What to do if Python installation fails?
A: Check your network connection and ensure you can access the Python official website. If it continues to fail, try manually downloading the Python installer and installing it.

### Q: What to do if pip fails to install dependencies?
A: The program will automatically detect pip errors and suggest fix methods. You can choose to fix pip using ensurepip or reinstall it using the get-pip.py script.

### Q: How to speed up dependency downloads?
A: Select domestic mirror sources (such as Tsinghua source, Alibaba Cloud source) in settings to significantly improve download speed.

### Q: How to install a specific version of a dependency?
A: When installing dependencies, enter the version number, for example: `requests==2.31.0`.

### Q: How to view installed Python versions?
A: Select "3. Check installed Python versions" in the main menu, and the program will display all installed Python versions and their paths.

## Technical Notes

### Core Modules
- `main.py` - Main program entry, containing command-line interface and core logic
- `version_fetcher.py` - Get Python version information
- `installer.py` - Handle Python installation process
- `setup.bat` - Environment initialization script

### Dependencies
- Python 3.6+
- requests (for fetching Python version information)

### System Requirements
- Windows operating system
- Network connection (for downloading Python installers and dependencies)
- Administrator privileges (for installing Python)

## Example Usage

### Install Python 3.10.11

1. Run `setup.bat` to start the program
2. Select "1. Get available Python versions"
3. Select "2. Install specific version"
4. Enter the version number (corresponding to Python 3.10.11)
5. Confirm installation
6. Wait for installation to complete

### Install Dependencies

1. Run `setup.bat` to start the program
2. Select "4. Manage Python dependencies"
3. Select "3. Install dependencies"
4. Enter the dependency name (e.g., `requests`)
5. Choose whether to specify a version (press Enter to install the latest version)
6. Wait for installation to complete

### Fix Pip

1. Run `setup.bat` to start the program
2. Select "4. Manage Python dependencies"
3. Select "7. Install/Fix pip"
4. Select "1. Use ensurepip module to install/fix pip"
5. Wait for the fix to complete

## Notes

- Administrator privileges are required for installing Python
- It is recommended to use domestic mirror sources to improve download speed
- For pip-related issues, you can use the program's built-in pip fix function
- For environments with poor network conditions, it is recommended to use wheel files for offline installation

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Changelog

### v1.2.0
- Added automatic update functionality, supporting direct download of the latest version from GitHub repository
- Improved version number comparison logic, automatically detecting if it is the latest version
- Supported identification and comparison of multiple version number formats
- Optimized user experience during update process, added detailed progress prompts
- Enhanced network error handling, improved update process stability

### v1.1.0
- Redesigned program structure, shifting focus from Python version management to pip management
- Added batch package management functionality, supporting batch update, uninstall, export, and installation from files
- Added progress bars and loading animations for all time-consuming operations
- Optimized pip repair functionality, providing multiple repair methods
- Enhanced mirror source management functionality, supporting more built-in mirror sources
- Fixed f-string syntax errors and pip command parameter errors

### v1.0.0
- Initial release
- Support Python version selection and installation
- Support dependency management
- Support pip repair
- Support mirror source management

---

**Happy coding!** 🎉