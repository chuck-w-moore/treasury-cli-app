import sys
import argparse
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta 
from tabulate import tabulate
from .api import TreasuryAPI

# Data structure for security types and descriptions.
SECURITY_MAP = {
    "Marketable": [
        "Treasury Bills", "Treasury Notes", "Treasury Bonds",
        "Treasury Inflation-Protected Securities (TIPS)",
        "Treasury Floating Rate Notes (FRN)", "Federal Financing Bank",
        "Total Marketable"
    ],
    "Non-marketable": [
        "Domestic Series", "Foreign Series", "State and Local Government Series",
        "United States Savings Securities", "United States Savings Inflation Securities",
        "Government Account Series", "Government Account Series Inflation Securities",
        "Total Non-marketable", "Special Purpose Vehicle"
    ],
    "Interest-bearing Debt": [
        "Total Interest-bearing Debt"
    ]
}

# --- Helper Functions ---

def get_last_day_of_month(year: int, month: int) -> str:
    """Returns the last day of a given month in YYYY-MM-DD format."""
    last_day = calendar.monthrange(year, month)[1]
    return f"{year}-{month:02d}-{last_day:02d}"

def validate_date_format(date_str: str, fmt: str = "%Y-%m-%d") -> bool:
    """Validates if a string matches the YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, fmt)
        return True
    except ValueError:
        return False

def validate_year_month_format(date_str: str) -> bool:
    """Validates if a string matches the YYYY-MM format."""
    return validate_date_format(date_str + "-01", "%Y-%m-%d")


def get_all_security_descriptions() -> set:
    """Returns a set of all valid security descriptions."""
    all_descs = set()
    for descs in SECURITY_MAP.values():
        all_descs.update(descs)
    return all_descs

VALID_DESCRIPTIONS = get_all_security_descriptions()

def validate_security_description(desc: str) -> str:
    """Checks if the provided security description is valid (case-insensitive check)."""
    # Find the correctly cased description
    for valid_desc in VALID_DESCRIPTIONS:
        if desc.lower() == valid_desc.lower():
            return valid_desc # Return the correctly cased version
    # If no match found, raise an error for argparse
    raise argparse.ArgumentTypeError(
        f"Invalid security description: '{desc}'. "
        f"Use the 'list-securities' command to see valid options."
    )

def find_security_type(description: str) -> str:
    """Finds the security type category for a given description."""
    for sec_type, descs in SECURITY_MAP.items():
        if description in descs:
            return sec_type
    return "Unknown" # Should not happen if validation passes

# --- Argparse Setup ---

def setup_parser() -> argparse.ArgumentParser:
    """Sets up the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Fetch U.S. Treasury security rates from the FiscalData API.",
        epilog="Use '<command> --help' for more information on a specific command."
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # --- Command: lookup ---
    lookup_parser = subparsers.add_parser(
        "lookup", help="Look up rates for specific dates (up to 5)."
    )
    lookup_parser.add_argument(
        "--dates",
        required=True,
        nargs='+', # Accepts one or more arguments
        help="One or more dates in YYYY-MM-DD format (e.g., 2023-09-30 2023-08-31)."
    )
    lookup_parser.add_argument(
        "--security1",
        required=True,
        type=validate_security_description,
        help="The description of the first security (e.g., 'Treasury Bills'). Use quotes if spaces."
    )
    lookup_parser.add_argument(
        "--security2",
        type=validate_security_description,
        help="(Optional) The description of a second security to compare."
    )

    # --- Command: range ---
    range_parser = subparsers.add_parser(
        "range", help="Look up rates over a date range (inclusive)."
    )
    range_parser.add_argument(
        "--start-date",
        required=True,
        type=str,
        help="Start date in YYYY-MM format (e.g., 2022-10)."
    )
    range_parser.add_argument(
        "--end-date",
        required=True,
        type=str,
        help="End date in YYYY-MM format (e.g., 2023-09)."
    )
    range_parser.add_argument(
        "--security1",
        required=True,
        type=validate_security_description,
        help="The description of the first security (e.g., 'Treasury Notes'). Use quotes if spaces."
    )
    range_parser.add_argument(
        "--security2",
        type=validate_security_description,
        help="(Optional) The description of a second security to compare."
    )

    # --- Command: list-securities ---
    subparsers.add_parser(
        "list-securities", help="List all available security types and descriptions."
    )

    return parser

# --- Command Handlers ---

def handle_list_securities():
    """Prints the available security types and descriptions."""
    print("\nAvailable Treasury Securities:")
    print("-" * 30)
    for sec_type, descriptions in SECURITY_MAP.items():
        print(f"\nType: {sec_type}")
        for desc in descriptions:
            print(f"  - \"{desc}\"") # Add quotes for clarity in usage
    print("\nUse the exact description (including quotes if needed) with the lookup/range commands.")


def fetch_and_display_rates(api: TreasuryAPI, dates_to_query: list[str], securities_to_find: list[str]):
    """Fetches data for given dates/securities and prints the table."""
    print("\nFetching data, please wait...")
    all_results = []
    securities_set = set(securities_to_find) # For efficient lookup

    for date in dates_to_query:
        try:
            rates_on_date = api.fetch_rates_by_date(date)
            for rate_data in rates_on_date:
                if rate_data["security_desc"] in securities_set:
                    all_results.append({
                        "Record Date": rate_data["record_date"],
                        "Security Type": find_security_type(rate_data["security_desc"]),
                        "Security Description": rate_data["security_desc"],
                        "Rate": rate_data["rate"]
                    })
        except Exception as e:
            print(f"Warning: Could not fetch data for {date}: {e}", file=sys.stderr)

    if all_results:
        # Sort results by date then description for consistent output
        all_results.sort(key=lambda x: (x["Record Date"], x["Security Description"]))
        print("\n--- Results ---")
        print(tabulate(all_results, headers="keys", tablefmt="grid"))
    else:
        print("\nNo matching data found for the selected criteria.")


def handle_lookup(api: TreasuryAPI, args: argparse.Namespace):
    """Handles the 'lookup' command logic."""
    if len(args.dates) > 5:
        print("Error: Maximum of 5 dates allowed for lookup.", file=sys.stderr)
        sys.exit(1)

    valid_dates = []
    for date_str in args.dates:
        if not validate_date_format(date_str):
            print(f"Error: Invalid date format '{date_str}'. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
        valid_dates.append(date_str)

    securities = [args.security1]
    if args.security2:
        if args.security1 == args.security2:
             print("Error: Security 1 and Security 2 cannot be the same.", file=sys.stderr)
             sys.exit(1)
        securities.append(args.security2)

    fetch_and_display_rates(api, sorted(list(set(valid_dates))), securities)


def handle_range(api: TreasuryAPI, args: argparse.Namespace):
    """Handles the 'range' command logic."""
    if not validate_year_month_format(args.start_date) or not validate_year_month_format(args.end_date):
        print("Error: Invalid date format. Use YYYY-MM.", file=sys.stderr)
        sys.exit(1)

    try:
        start = datetime.strptime(args.start_date, "%Y-%m")
        end = datetime.strptime(args.end_date, "%Y-%m")
    except ValueError:
         print("Error: Could not parse dates. Use YYYY-MM format.", file=sys.stderr)
         sys.exit(1)


    if start > end:
        print("Error: Start date cannot be after end date.", file=sys.stderr)
        sys.exit(1)

    dates_in_range = []
    current_date = start
    while current_date <= end:
        year = current_date.year
        month = current_date.month
        # Add validation for allowed date range (2020-10 to 2025-09)
        if not ( (year == 2020 and month >= 10) or \
                 (2020 < year < 2025) or \
                 (year == 2025 and month <= 9) ):
             print(f"Warning: Skipping {year}-{month:02d} - outside allowed range (2020-10 to 2025-09).", file=sys.stderr)
        else:
            dates_in_range.append(get_last_day_of_month(year, month))

        current_date += relativedelta(months=1) # Move to the next month

    if not dates_in_range:
        print("Error: No valid dates found within the specified range and allowed period (2020-10 to 2025-09).", file=sys.stderr)
        sys.exit(1)

    securities = [args.security1]
    if args.security2:
        if args.security1 == args.security2:
             print("Error: Security 1 and Security 2 cannot be the same.", file=sys.stderr)
             sys.exit(1)
        securities.append(args.security2)

    fetch_and_display_rates(api, dates_in_range, securities)


# --- Main Execution ---

def main():
    """Main function to parse arguments and execute the correct command."""
    parser = setup_parser()
    args = parser.parse_args()

    api = TreasuryAPI()

    try:
        if args.command == "lookup":
            handle_lookup(api, args)
        elif args.command == "range":
            handle_range(api, args)
        elif args.command == "list-securities":
            handle_list_securities()
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()