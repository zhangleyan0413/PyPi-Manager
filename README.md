# PyPi Manager - Python Pip Manager

A powerful Python environment management tool that simplifies Python installation, dependency management, pip troubleshooting, and mirror source configuration.

## Features

### 🐍 Python Version Management
- Get available Python version list
- Install specific Python versions
- Check installed Python versions and their paths

### 📦 Dependency Management
- Show installed dependencies
- Search dependencies and display version information
- Install dependencies with specific versions
- Upgrade dependencies to latest versions
- Uninstall unnecessary dependencies
- Install dependencies from wheel files

### 🔧 Pip Management
- Install/Fix pip
- Multiple pip repair methods
- Check pip status

### 🚀 Mirror Source Management
- Built-in 5 recommended mirror sources (Tsinghua, USTC, Alibaba Cloud, Douban, Official)
- Add custom mirror sources
- Set default mirror source

### 💡 Smart Features
- Auto-detect pip errors and suggest fixes
- Show download and installation progress
- Support domestic mirror sources for acceleration
- Detailed error messages and solutions

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
Python Version Selector
1. Get available Python versions
2. Install specific version
3. Check installed Python versions
4. Manage Python dependencies
5. Settings
6. Exit
```

### Dependency Management Menu

```
Dependency Management Menu
1. Show installed dependencies
2. Search dependencies
3. Install dependencies
4. Upgrade dependencies
5. Uninstall dependencies
6. Install from wheel file
7. Install/Fix pip
8. Return to main menu
```

### Settings Menu

```
Settings Menu
1. Manage mirror sources
2. Return to main menu
```

### Mirror Source Management Menu

```
Mirror Source Management Menu
1. Show current mirror source
2. Select built-in mirror source
3. Add custom mirror source
4. Delete custom mirror source
5. Set default mirror source
6. Return to settings menu
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

### v1.0.0
- Initial release
- Support Python version selection and installation
- Support dependency management
- Support pip repair
- Support mirror source management

---

**Happy coding!** 🎉
