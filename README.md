# PyPi Manager Test Suite

This directory contains test files for the PyPi Manager application. These tests help ensure that the application functions correctly and reliably.

## Test Files

| File Name | Description |
|-----------|-------------|
| `start_cli.py` | Starts the command-line interface version of PyPi Manager |
| `start_gui.py` | Starts the graphical user interface version of PyPi Manager |
| `test_all.bat` | Runs all tests automatically |
| `test_author_info.py` | Tests the author information functionality |
| `test_batch_progress.py` | Tests progress bars for batch operations |
| `test_imports.py` | Tests module imports and dependencies |
| `test_progress_bars.py` | Tests progress bar functionality |
| `test_setup.bat` | Tests the setup batch file |
| `test_updatable.py` | Tests package update checking functionality |
| `test_update.py` | Tests the update checking functionality |
| `test_version_compare.py` | Tests version number comparison functionality |
| `ui.py` | User interface utilities for testing |

## How to Run Tests

### Run All Tests

To run all tests at once, execute the batch file:

```bash
./test_all.bat
```

### Run Individual Tests

To run a specific test, execute it directly with Python:

```bash
python test_[name].py
```

For example, to test version comparison:

```bash
python test_version_compare.py
```

## Test Categories

### Functionality Tests
- `test_author_info.py` - Verifies author information display
- `test_version_compare.py` - Ensures version comparison works correctly
- `test_updatable.py` - Tests package updatability checking
- `test_update.py` - Verifies update checking functionality

### UI and User Experience Tests
- `test_progress_bars.py` - Tests progress bar display and functionality
- `test_batch_progress.py` - Tests progress bars for batch operations

### Integration Tests
- `test_imports.py` - Ensures all modules import correctly
- `test_setup.bat` - Tests the setup process

### Launch Tests
- `start_cli.py` - Starts the CLI version
- `start_gui.py` - Starts the GUI version

## Troubleshooting

If you encounter issues running the tests:

1. Ensure Python is installed and added to your PATH
2. Make sure all dependencies are installed (run `pip install -r ../requirements.txt`)
3. Check that you're running the tests from the correct directory
4. Verify that the main application files are present in the parent directory

## Notes

- These tests are designed to work with the PyPi Manager application
- Some tests may require an internet connection (e.g., update checking)
- Test results will be displayed in the console

For more information about the PyPi Manager application, please refer to the README.md file in the parent directory.
