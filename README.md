# PyPi Manager GUI

This document provides instructions for using the graphical user interface (GUI) version of PyPi Manager, a powerful Python environment management tool.

## Overview

The GUI version of PyPi Manager offers all the functionality of the command-line version with the added convenience of a visual interface. It is built using wxPython and provides a modern, user-friendly experience.

## Features

### 📦 pip Package Management
- **Show installed packages** - View all packages installed in your Python environment
- **Search and install packages** - Find packages on PyPI and install them with a few clicks
- **Upgrade packages** - Update packages to their latest versions
- **Uninstall packages** - Remove unwanted packages
- **Install from wheel files** - Install packages from local .whl files

### 🔧 pip Repair
- **Check pip status** - Verify if pip is working correctly
- **Fix pip issues** - Automatically repair common pip problems

### 🚀 Mirror Source Configuration
- **Built-in mirror sources** - Access 5 recommended mirror sources (Tsinghua, USTC, Alibaba Cloud, Douban, Official)
- **Custom mirror sources** - Add and manage your own mirror sources
- **Set default mirror** - Configure your preferred mirror source

### ⚡ Batch Package Management
- **Batch update** - Update all updatable packages at once
- **Batch uninstall** - Remove multiple packages simultaneously
- **Export packages** - Save installed packages list to requirements.txt
- **Install from file** - Install packages from a requirements.txt file

### 🐍 Python Version Management
- **View available versions** - See all Python versions available for installation
- **Install specific version** - Download and install a specific Python version
- **Check installed versions** - View all Python versions installed on your system

### 🌐 Python Environment Management
- **Virtual environments** - Create and manage virtual environments
- **Environment activation** - Activate virtual environments for use

### 🛠️ Tools
- **Code formatting** - Format Python code using autopep8
- **Code checking** - Analyze code quality using pylint

### 🔍 File Integrity Check
- **Check file integrity** - Verify that all program files are present and complete
- **Automatic repair** - Fix missing or corrupted files by downloading from GitHub

### 📖 Documentation
- **Detailed guides** - Access comprehensive usage instructions
- **Keyboard shortcuts** - Learn keyboard shortcuts for faster operation
- **Frequently asked questions** - Find answers to common questions

## Installation

### Prerequisites
- Python 3.6 or higher
- Windows operating system

### Steps
1. **Download the program** - Clone or download the repository to your local machine
2. **Run setup** - Double-click `setup.bat` to run the initialization script
3. **Select GUI mode** - When prompted, choose the GUI option to start the graphical interface

## User Interface

### Main Window
The main window consists of:
- **Menu bar** - Access all program functions through organized menus
- **Toolbars** - Quick access to common operations
- **Status bar** - Displays current status and progress information
- **Main content area** - Shows the selected feature's interface

### Progress Bars
The GUI version includes progress bars for all time-consuming operations, such as:
- Package installation and uninstallation
- Batch operations
- File downloads
- Python installations

### Dialogs
The application uses various dialogs for specific tasks:
- **Package Manager** - For managing pip packages
- **Mirror Source Configuration** - For setting up package sources
- **Batch Operations** - For managing multiple packages at once
- **Python Version Management** - For installing and managing Python versions
- **Update Checker** - For checking for program updates
- **File Integrity Checker** - For verifying program files

## Usage Guide

### Starting the GUI

#### Method 1: From setup.bat
1. Double-click `setup.bat`
2. When prompted, select option `2` for GUI mode

#### Method 2: Directly
1. Open a command prompt
2. Navigate to the program directory
3. Run: `python main_gui.py`

### Common Tasks

#### Installing a Package
1. Click **Package Management** in the main menu
2. Select **Search and Install** tab
3. Enter the package name in the search field
4. Click **Search**
5. Select the desired version from the results
6. Click **Install**

#### Updating All Packages
1. Click **Batch Management** in the main menu
2. Click **Check updatable packages**
3. Select the packages you want to update
4. Click **Update selected packages**

#### Configuring Mirror Source
1. Click **Mirror Configuration** in the main menu
2. Select a built-in mirror source or add a custom one
3. Click **Set as default** to make it your preferred source

#### Checking for Updates
1. Click **Help** in the main menu
2. Select **Check for updates**
3. The program will check for newer versions and prompt you to update if available

## Keyboard Shortcuts

| Shortcut | Function |
|----------|----------|
| `Ctrl+N` | New operation (context-dependent) |
| `Ctrl+S` | Save current settings |
| `Ctrl+F` | Search (context-dependent) |
| `Ctrl+R` | Refresh current view |
| `Ctrl+Q` | Exit program |
| `F1` | Show help |
| `F5` | Refresh |

## Troubleshooting

### Common Issues

#### GUI Doesn't Start
- **Issue**: The GUI fails to start with an error
- **Solution**: 
  1. Ensure wxPython is installed (`pip install wxPython`)
  2. Check that you have Python 3.6 or higher
  3. Try running `setup.bat` again to install dependencies

#### Progress Bar Freezes
- **Issue**: The progress bar stops moving during an operation
- **Solution**: 
  - The operation is likely still running in the background
  - Wait for it to complete
  - If it remains frozen for an extended period, you may need to restart the program

#### Package Installation Fails
- **Issue**: Packages fail to install
- **Solution**: 
  1. Check your internet connection
  2. Try changing the mirror source
  3. Verify that pip is working correctly using the pip repair function

## System Requirements

- **Operating System**: Windows 7 or later
- **Python**: 3.6 or higher
- **RAM**: 2GB or more recommended
- **Disk Space**: 100MB for the program, plus additional space for Python installations and packages

## Dependencies

The GUI version requires the following dependencies:
- `wxPython==4.2.5` - For the graphical interface
- `requests` - For network operations
- `autopep8` - For code formatting
- `pylint` - For code checking

These dependencies will be automatically installed by `setup.bat`.

## Screenshots

### Main Window
![Main Window](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=PyPi%20Manager%20GUI%20main%20window%20with%20menu%20bar%20and%20toolbars&image_size=landscape_16_9)

### Package Management
![Package Management](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=PyPi%20Manager%20GUI%20package%20management%20interface%20showing%20installed%20packages&image_size=landscape_16_9)

### Mirror Configuration
![Mirror Configuration](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=PyPi%20Manager%20GUI%20mirror%20source%20configuration%20interface&image_size=landscape_16_9)

## Changelog

### v1.3.0
- **Enhanced UI** - Improved visual design and layout
- **Progress bars** - Added progress bars for all time-consuming operations
- **File integrity check** - Added functionality to check and repair program files
- **Batch operations** - Improved batch package management with better user feedback
- **Search and install** - Combined search and installation into a single tab
- **Uninstall improvements** - Added package selection for uninstallation
- **Error handling** - Enhanced error messages and troubleshooting tips

### v1.2.0
- **Initial GUI release** - First version of the graphical interface
- **Basic functionality** - Implemented core features from the CLI version
- **User-friendly design** - Created intuitive interface for all operations

## Support

If you encounter any issues with the GUI version:

1. **Check the documentation** - Refer to this guide and the main README.md
2. **Run file integrity check** - Use the built-in tool to verify program files
3. **Update the program** - Check for updates to get the latest fixes
4. **Manual repair** - If all else fails, download the latest version from GitHub

## Contributing

Contributions to the GUI version are welcome! If you have suggestions for improvements or bug fixes, please submit them through the GitHub repository.

## License

PyPi Manager is released under the MIT License. See the LICENSE file for details.

---

**PyPi Manager GUI** - Simplifying Python environment management through a intuitive visual interface.

For more information about the command-line version, please refer to README.md.
