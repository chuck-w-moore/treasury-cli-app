# Treasury Rate Finder CLI

[![Python CI](https://github.com/chuck-w-moore/treasury-cli-app/actions/workflows/tests.yml/badge.svg)](https://github.com/chuck-w-moore/treasury-cli-app/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python command-line application for fetching and comparing historical average interest rates for U.S. Treasury securities.

## Overview

This tool provides an interactive interface to query the U.S. Department of the Treasury's FiscalData API. Users can select specific date ranges or individual months and compare the average interest rates for up to two different treasury securities, with all data displayed in a clean, formatted table.

## Features

* **Interactive Menu:** A user-friendly, loop-based interface.
* **Flexible Date Selection:**
    * Query specific months (up to 5).
    * Query a date range (e.g., 2022-11 to 2023-06).
* **Security Comparison:** Select one or two securities from a three-level menu (Type -> Description) to compare rates side-by-side.
* **Built-in Validation:** Smart prompts prevent invalid dates and duplicate security selections.
* **Formatted Output:** All results are printed in a clean, easy-to-read `tabulate` table.

## API Information

This project uses the **U.S. Department of the Treasury FiscalData API** and specifically targets the `/v2/accounting/od/avg_interest_rates` endpoint.

Full API documentation can be found here: <https://fiscaldata.treasury.gov/api-documentation/>

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO.git](https://github.com/YOUR_USERNAME/YOUR_REPO.git)
    cd YOUR_REPO
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```
    * **On Windows:**
        ```bash
        venv\Scripts\activate
        ```
    * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

## Usage

This application is run as a Python module from the **root directory** of the project (the `treasury-cli-app` folder). Use the `-m` flag followed by the package name (`src`) and the specific command.

**General Command Structure:**

```bash
python -m src <command> [options]
```

**Available Commands:**

1.  **`list-securities`**: Displays all available security types and their exact descriptions. Useful for finding the correct names to use with other commands.
    ```bash
    python -m src list-securities
    ```
    *(Output will show Marketable, Non-marketable, etc., with their descriptions)*

2.  **`lookup`**: Fetches rates for one or more specific dates.
    * `--dates`: Required. Provide one to five dates in `YYYY-MM-DD` format, separated by spaces.
    * `--security1`: Required. The exact description of the security. Use quotes if the name contains spaces (e.g., `"Treasury Bills"`).
    * `--security2`: Optional. A second security description for comparison. Cannot be the same as `--security1`.

    *Example (Single Security, Single Date):*
    ```bash
    python -m src lookup --dates 2023-09-30 --security1 "Treasury Bills"
    ```

    *Example (Compare Securities, Multiple Dates):*
    ```bash
    python -m src lookup --dates 2023-09-30 2023-08-31 --security1 "Treasury Notes" --security2 "Treasury Bonds"
    ```
    *(Output will be a table showing rates for both securities on both dates)*

3.  **`range`**: Fetches rates over a continuous range of months.
    * `--start-date`: Required. The starting month in `YYYY-MM` format.
    * `--end-date`: Required. The ending month in `YYYY-MM` format (inclusive).
    * `--security1`: Required. The exact description of the security. Use quotes if needed.
    * `--security2`: Optional. A second security description for comparison.

    *Example (Single Security, Date Range):*
    ```bash
    python -m src range --start-date 2022-11 --end-date 2023-02 --security1 "Total Marketable"
    ```

    *Example (Compare Securities, Date Range):*
    ```bash
    python -m src range --start-date 2023-01 --end-date 2023-03 --security1 "Treasury Bills" --security2 "Federal Financing Bank"
    ```
    *(Output will be a table showing rates for both securities for Jan, Feb, and Mar 2023)*

**Getting Help:**

You can always get help on the available commands or specific command options using `--help`:

```bash
python -m src --help
python -m src lookup --help
python -m src range --help
```

## Testing

This project uses `pytest` for unit testing. The tests primarily focus on the `src/api.py` module, ensuring correct API interaction and data handling using mocking. Tests for `src/main.py` verify argument parsing and error handling.

To run the test suite, execute the following command from the project's root directory (ensure your virtual environment is active and test dependencies are installed):

```bash
pytest -v
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.