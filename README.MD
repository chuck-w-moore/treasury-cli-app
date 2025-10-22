# Treasury Rate Finder CLI

[![Python CI](https://github.com/chuck-w-moore/treasury-cli-app/actions/workflows/tests.yml/badge.svg)](https://github.com/chuck-w-moore/treasury-cli-app/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python command-line application using an interactive interface to fetch and compare historical average interest rates for U.S. Treasury securities via the Treasury FiscalData API.

## Overview

This tool provides an interactive interface to query the U.S. Department of the Treasury's FiscalData API for average interest rates. Users are guided through selecting date ranges or specific dates and can compare the rates for up to two different treasury security categories. The results are displayed in a clean, formatted table.

## Features

* **Interactive Menu:** A user-friendly, loop-based interface guides the user through the process.
* **Flexible Date Selection:**
    * Query specific months (up to 5, entered chronologically).
    * Query a date range (e.g., 2022-11 to 2023-06).
* **Security Comparison:** Select one or two securities from a menu (Type -> Description) to compare rates side-by-side.
* **Built-in Validation:** Smart prompts prevent invalid dates, ensure chronological order for specific dates, and prevent duplicate security selections.
* **Formatted Output:** All results are printed in a clear, easy-to-read `tabulate` table.
* **Data Range:** Currently fetches data between October 2020 and September 2025 (inclusive).

## API Information

This project uses the **U.S. Department of the Treasury FiscalData API** and specifically targets the `/v2/accounting/od/avg_interest_rates` endpoint.

Full API documentation can be found here: <https://fiscaldata.treasury.gov/api-documentation/>

## Installation

Follow these steps to set up the project locally.

**Prerequisites:**

* Python 3.10 or higher installed.
* Git installed.

**Steps:**

1.  **Clone the repository:** Open your terminal or command prompt and navigate to where you want to store the project. Then run:
    ```bash
    git clone [https://github.com/chuck-w-moore/treasury-cli-app.git](https://github.com/chuck-w-moore/treasury-cli-app.git)
    cd treasury-cli-app
    ```

2.  **Create and activate a virtual environment:** This is highly recommended to isolate project dependencies and avoid conflicts with other Python projects.
    ```bash
    python -m venv venv
    ```
    * **On Windows:** Activate the environment.
        ```bash
        venv\Scripts\activate
        ```
        *(Your prompt should now start with `(venv)`)*
    * **On macOS/Linux:** Activate the environment.
        ```bash
        source venv/bin/activate
        ```
        *(Your prompt should now start with `(venv)`)*

3.  **Install required dependencies:** Use pip to install the packages listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

You are now ready to use the application!

## Usage

This application is run as a Python module from the **root directory** of the project (the `treasury-cli-app` folder). Use the `-m` flag followed by the package name (`src`).

**Starting the Application:**

Navigate to the project's root directory in your terminal (ensure your virtual environment is active) and run:

```bash
python -m src
```

## License

Please review the license section to see the license.
