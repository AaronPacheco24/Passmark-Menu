"# Passmark-Menu

Passmark-Menu is a Python-based utility for automating AXCA customer hardware validation and burn-in testing workflows. It provides a centralized menu interface for coordinating Passmark BurnInTest (BIT) execution, result verification, and test log organization across multiple customer configurations.

## Overview

This project orchestrates end-to-end hardware testing for customer systems by:
- Presenting a customer-selection menu
- Routing to customer-specific validation workflows
- Executing hardware burn-in tests via BurnInTest
- Verifying test results and system specifications
- Archiving test logs to server-based storage (PASSED/FAILED directories)

The tool is designed to streamline manufacturing quality assurance by eliminating manual test execution and reducing operator error during hardware validation phases.

## Key Features

- **Customer-Driven Menu System** - Easy selection interface for different customers (Allied, Signify, Locus)
- **Automated Hardware Validation** - Integrates with BurnInTest for comprehensive system burn-in testing
- **Result Classification** - Automatically routes test results to PASSED or FAILED log directories on remote servers
- **Configuration Management** - Centralized JSON-based product metadata with model-specific settings
- **System Verification** - Validates required hardware components against stored specifications
- **Error Handling** - Graceful handling of missing files, encoding issues, and validation failures

## Architecture

### High-Level System Design

```
Menu Selection (main.py)
         ↓
Customer Routing (customer_kickoff.py)
         ↓
Hardware Validation Flow:
  ├─ Load Product Configuration (product_info.json)
  ├─ Execute BurnInTest (HardwareCheck/)
  ├─ Compare System Info (compare_files)
  ├─ Check Test Results (check_passmark)
  └─ Archive Logs (PASSED/FAILED directories)
```

### Directory Structure

```
Passmark-Menu/
├── README.md                          # Project documentation
├── src/
│   ├── main.py                        # Entry point & menu interface
│   ├── customer_kickoff.py            # Core validation workflow logic
│   ├── product_info.json              # Product configurations & metadata
│   └── HardwareCheck/
│       ├── HardWareCheck.bitcfg       # BurnInTest configuration template
│       └── POST-HARDWARE.bat          # Post-test batch script (Windows automation)
```

### Component Descriptions

#### `src/main.py` - Application Entry Point
- **Purpose**: Provides the primary user interface menu
- **Functionality**:
  - Displays customer selection options (Allied, Signify, Locus, Exit)
  - Routes selections to appropriate customer kickoff procedures
  - Maintains continuous menu loop until exit
  - Clears console between menu displays for clean UX
- **Dependencies**: `customer_kickoff`, `os`, `sys`
- **Key Functions**:
  - `menu()` - Renders menu and processes user input

#### `src/customer_kickoff.py` - Validation Workflow Engine
- **Purpose**: Orchestrates hardware testing and result verification for each customer
- **Functionality**:
  - Loads product configuration from JSON
  - Executes hardware burn-in tests
  - Validates system components against specifications
  - Processes BurnInTest logs and routes them to appropriate directories
- **Dependencies**: `os`, `sys`, `subprocess`, `re`, `time`, `json`, `pathlib`, `shutil`
- **Key Functions**:
  - `customer_specification(customer_name)` - Main entry point for customer workflows
  - `check_passmark(product_info, modelNum, serialNum)` - Analyzes BIT results and archives logs
  - `compare_files(requiredParts)` - Validates system information against required components

**`check_passmark()` Workflow**:
1. Reads BurnInTest log file from `X:\Program Files\BurnInTest\BIT_log.log`
2. Scans for "FAIL" entries indicating test failures
3. Routes log to either:
   - `product_info[modelNum]["PASSED"]` if all tests passed
   - `product_info[modelNum]["FAILED"]` if any failures detected
4. Names archived log with serial number for traceability

**`compare_files()` Workflow**:
1. Reads system information log from `X:\Program Files\BurnInTest\TempSysInfo.txt`
2. Validates presence of all required parts/components
3. Returns `True` only if all required parts are found
4. Exits on missing TempSysInfo.txt file

#### `src/product_info.json` - Configuration Database
- **Purpose**: Stores model-specific paths, patterns, and validation rules
- **Structure**: Key-value mapping where key is the product model number
- **Fields per Model**:
  - `CONFIG` - Path to model-specific BurnInTest configuration
  - `BITCFG` - BurnInTest configuration file location
  - `PASSED` - Server directory for successful test logs
  - `FAILED` - Server directory for failed test logs
  - `RegEX` - Regular expression pattern for serial number validation

**Example Entry**:
```json
{
  "41-000326-00": {
    "CONFIG": "Y:\\Locus\\configs\\41-000326-00.cfg",
    "BITCFG": "Y:\\Locus\\41-000326-00\\41-000326-00.bitcfg",
    "PASSED": "Y:\\Locus\\41-000326-00\\PASSED-LOGS\\",
    "FAILED": "Y:\\Locus\\41-000326-00\\FAILED-LOGS\\",
    "RegEX": "^E[A-Z0-9]{15}$"
  }
}
```

#### `src/HardwareCheck/` - Hardware Validation Tools
- **HardWareCheck.bitcfg** - BurnInTest configuration template defining:
  - CPU stress tests
  - Memory diagnostics
  - Storage validation
  - Thermal monitoring
  - Other hardware-specific burn-in parameters

- **POST-HARDWARE.bat** - Windows batch script for:
  - Post-test system state restoration
  - Log file cleanup/organization
  - Server synchronization
  - Result notifications

### Data Flow

```
User Input (Customer Selection)
            ↓
main.py routes to customer_kickoff.customer_specification()
            ↓
Load product_info.json configuration for model
            ↓
Execute BurnInTest with HardWareCheck.bitcfg
            ↓
Generate system info log (TempSysInfo.txt)
Generate test results log (BIT_log.log)
            ↓
Parallel validation:
  ├─ compare_files() - Verify required components
  └─ check_passmark() - Parse test results
            ↓
Archive logs to PASSED or FAILED directory
            ↓
Execute POST-HARDWARE.bat (cleanup/notifications)
            ↓
Return to menu
```

### External Dependencies

- **Python 3.8+** - Core runtime
- **BurnInTest** - Third-party hardware diagnostics software installed at `X:\Program Files\BurnInTest\`
- **Network Drives** - Y: and X: drives for configuration access and log storage
- **Windows Batch Runtime** - For executing POST-HARDWARE.bat scripts

## Getting Started

### Prerequisites
1. Python 3.8 or higher
2. BurnInTest software installed on system
3. Network access to configuration and log storage locations
4. Appropriate product entries in `product_info.json`

### Installation

1. Clone or download this repository
2. Ensure product models are configured in `src/product_info.json`
3. Verify network drive paths (Y:\ and X:\) are accessible

### Running the Application

```bash
cd src
python main.py
```

The application will display a menu. Select a customer to begin the validation workflow.

## Configuration Guide

### Adding a New Customer/Product Model

1. Open `src/product_info.json`
2. Add a new entry with the model number as the key:

```json
{
  "YOUR-MODEL-NUMBER": {
    "CONFIG": "Y:\\CustomerName\\configs\\YOUR-MODEL-NUMBER.cfg",
    "BITCFG": "Y:\\CustomerName\\YOUR-MODEL-NUMBER\\YOUR-MODEL-NUMBER.bitcfg",
    "PASSED": "Y:\\CustomerName\\YOUR-MODEL-NUMBER\\PASSED-LOGS\\",
    "FAILED": "Y:\\CustomerName\\YOUR-MODEL-NUMBER\\FAILED-LOGS\\",
    "RegEX": "^[A-Z]{1}[A-Z0-9]{15}$"
  }
}
```

3. Create corresponding directories on the network
4. Generate or copy appropriate `.bitcfg` configuration file
5. Update `main.py` customer routing as needed

## Technical Notes

- **Log Encoding**: Customer kickoff script handles UTF-16 and UTF-8 encodings in system info logs
- **Error Tolerance**: Script continues processing even if system info log has encoding issues
- **Server Storage**: Test logs are archived to network drives with serial numbers for traceability
- **Regex Validation**: Serial numbers can be validated using patterns defined per product model
- **Windows Platform**: Currently Windows-specific due to BurnInTest and batch script dependencies

## Future Enhancements

- Support for additional customers and product models
- Web-based dashboard for viewing historical test results
- Email notifications on test completion
- Database integration for result tracking and analytics
- Cross-platform support (Linux/macOS)
" 
