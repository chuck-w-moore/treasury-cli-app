# Treasury Rate Finder CLI

[![Python CI](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/tests.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python command-line application for fetching and comparing historical average interest rates for U.S. Treasury securities.

## Overview

This tool provides an interactive interface to query the U.S. Department of the Treasury's FiscalData API. Users can select specific date ranges or individual months and compare the average interest rates for up to two different treasury securities, with all data displayed in a clean, formatted table.

## Features

* **Interactive Menu:** A user-friendly, loop-based interface.
* **Flexible Date Selection:**
    * Query specific months (up to 5).
    * Query a date range (e.g., 2022-01 to 2023-06).
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

Because this project is structured as a Python package, you must run it as a module from the **root directory** of the project (the folder containing `src/`).

```bash
python -m src.main