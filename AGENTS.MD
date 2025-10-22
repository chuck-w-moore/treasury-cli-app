# Federal Reserve Treasury Bond Rates CLI

## Project Overview

Command-line application using `argparse` to fetch and showcase historical U.S. Treasury security average interest rates from the Treasury FiscalData API. Users can query rates for specific dates or date ranges and compare up to two securities.

#### Available Securities:

| Security Type           | Available Security Descriptions                                                                                                                                                                                           |
| :---------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Marketable** | <ul><li>Treasury Bills</li><li>Treasury Notes</li><li>Treasury Bonds</li><li>Treasury Inflation-Protected Securities (TIPS)</li><li>Treasury Floating Rate Notes (FRN)</li><li>Federal Financing Bank</li><li>Total Marketable</li></ul> |
| **Non-marketable** | <ul><li>Domestic Series</li><li>Foreign Series</li><li>State and Local Government Series</li><li>United States Savings Securities</li><li>United States Savings Inflation Securities</li><li>Government Account Series</li><li>Government Account Series Inflation Securities</li><li>Total Non-marketable</li><li>Special Purpose Vehicle</li></ul> |
| **Interest-bearing Debt** | <ul><li>Total Interest-bearing Debt</li></ul>                                                                                                                                                                            |

## API Integration

-   **API:** U.S. Department of the Treasury FiscalData
-   **Base URL:** <https://api.fiscaldata.treasury.gov/services/api/fiscal_service>
-   **Key endpoint:**
    -   `/v2/accounting/od/avg_interest_rates` - Fetches average interest rates based on filters (like date).
-   **Data format:** JSON

## CLI Commands (`argparse`)

-   `lookup --dates <date1> [date2...] --security1 <desc1> [--security2 <desc2>]`
    -   Fetches rates for specific dates (YYYY-MM-DD, up to 5).
    -   Requires at least one security description (`--security1`).
    -   Optionally allows a second security for comparison (`--security2`).
-   `range --start-date <YYYY-MM> --end-date <YYYY-MM> --security1 <desc1> [--security2 <desc2>]`
    -   Fetches rates for a range of months (inclusive).
    -   Requires start and end dates (YYYY-MM).
    -   Requires at least one security description (`--security1`).
    -   Optionally allows a second security for comparison (`--security2`).
-   `list-securities`
    -   Displays all available security types and their descriptions.

## AI-Assisted Development Process
AI assistance (Gemini & Copilot) was utilized for:
-   Initial project scaffolding and structure suggestions.
-   Generating boilerplate code for API calls and argparse setup.
-   Writing unit tests, particularly implementing mocking for API calls.
-   Generating docstrings and documentation (README, AGENTS.md).
-   Refactoring code (e.g., switching from interactive input to argparse).
-   Debugging errors (e.g., ModuleNotFoundErrors, argparse issues).

## Technical Stack

-   Python 3.10+
-   `argparse` for CLI argument parsing
-   `requests` library for API calls
-   `tabulate` for formatting output tables
-   `python-dateutil` for date range calculations
-   `pytest` for testing with mocking (`pytest-mock`)

## Code Organization

-   `src/__init__.py` - Makes `src` a package.
-   `src/__main__.py` - Entry point for `python -m src`.
-   `src/main.py` - Main CLI logic, `argparse` setup, command handlers.
-   `src/api.py` - `TreasuryAPI` class for interacting with the external API.
-   `tests/` - Contains unit tests.
    -   `tests/test_api.py` - Tests for `api.py` using mocks.
    -   `tests/test_main.py` - Tests for `main.py` CLI argument parsing and function calls, mocking API interaction.

## Standards

-   Docstrings for all functions and classes.
-   Follow PEP 8 style guidelines.
-   Handle errors gracefully (e.g., API errors, invalid user input) using `try/except` and `argparse` validation.
-   Mock all external API calls in tests.