import sys
import re
import calendar
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
        "United States Savings Securities",
        "United States Savings Inflation Securities",
        "Government Account Series",
        "Government Account Series Inflation Securities",
        "Total Non-marketable", "Special Purpose Vehicle"
    ],
    "Interest-bearing Debt": [
        "Total Interest-bearing Debt"
    ]
}


def get_last_day_of_month(year: int, month: int) -> str:
    """Returns the last day of a given month in YYYY-MM-DD format."""
    last_day = calendar.monthrange(year, month)[1]
    return f"{year}-{month:02d}-{last_day:02d}"


def prompt_for_dates() -> list[str] | None:
    """Guides the user to select either specific dates or a date range."""
    while True:
        print("\n--- Date Selection ---")
        print("How would you like to select dates?")
        print("  1. Specific Months (up to 5)")
        print("  2. A Date Range")
        choice = input("Your choice (1-2): ")

        if choice == '1':
            # Specific Dates Logic
            dates = []
            print("\nEnter up to 5 dates chronologically (earliest to latest).")
            print("Note: For year 2020, months are 10-12. For 2025, months are 01-09.")
            while len(dates) < 5:
                try:
                    year_str = input(
                        f"Enter Year #{len(dates) + 1} (YYYY), or press Enter to finish: "
                        )
                    if not year_str:
                        break
                    year = int(year_str)

                    month_str = input(f"Enter Month #{len(dates) + 1} (MM): ")
                    month = int(month_str)

                    # Updated validation logic
                    if not (2020 <= year <= 2025):
                        print("Invalid input. Year must be between 2020 and 2025.")
                        continue
                    if year == 2020 and month < 10:
                        print("Invalid input. For 2020, earliest month is 10.")
                        continue
                    if year == 2025 and month > 9:
                        print("Invalid input. For 2025, latest month is 9.")
                        continue
                    if not (1 <= month <= 12):
                        print("Invalid input. Month must be between 01 and 12.")
                        continue

                    new_date = get_last_day_of_month(year, month)
                    if dates and new_date < dates[-1]:
                        print("Error: Dates must be in chronological order.")
                        # Let user retry entering the current date
                        continue

                    dates.append(new_date)

                except ValueError:
                    print("Invalid input. Please enter numbers for year/month.")
            # Ensure unique and sorted before returning
            return sorted(list(set(dates)))

        elif choice == '2':
            # Date Range Logic
            while True:  # Loop for date range input validation
                try:
                    print("\nEnter Start Date (Note: Range is 2020-10 to 2025-09):")
                    start_year = int(input("  Start Year (YYYY): "))
                    start_month = int(input("  Start Month (MM): "))

                    print("Enter End Date:")
                    end_year = int(input("  End Year (YYYY): "))
                    end_month = int(input("  End Month (MM): "))

                    # More robust validation
                    valid_start = (2020 <= start_year <= 2025 and
                                   1 <= start_month <= 12)
                    valid_end = (2020 <= end_year <= 2025 and
                                 1 <= end_month <= 12)

                    if not (valid_start and valid_end):
                        print("Invalid input. Ensure years 2020-2025, months 01-12.")
                        continue

                    if (end_year, end_month) < (start_year, start_month):
                        print("Error: End date cannot be before start date.")
                        continue

                    # Check against overall allowed range
                    if (start_year == 2020 and start_month < 10) or start_year < 2020:
                         print("Error: Start date out of allowed range (min 2020-10).")
                         continue
                    if (end_year == 2025 and end_month > 9) or end_year > 2025:
                         print("Error: End date out of allowed range (max 2025-09).")
                         continue

                    dates = []
                    for year in range(start_year, end_year + 1):
                        s_month = start_month if year == start_year else 1
                        e_month = end_month if year == end_year else 12
                        for month in range(s_month, e_month + 1):
                            # Ensure generated dates are within the hard limits
                            if year == 2020 and month < 10: continue
                            if year == 2025 and month > 9: continue
                            dates.append(get_last_day_of_month(year, month))
                    return dates # Return dates if validation passes
                except ValueError:
                    print("Invalid input. Please enter numbers for year/month.")
                    # Loop will repeat the date range questions

        else:
            print("Invalid choice. Please enter 1 or 2.")
            # Loop will repeat the date selection menu


def prompt_for_security(existing_security: dict | None = None) -> dict:
    """Guides the user to select a security, ensuring it's not a duplicate."""
    print("\n--- Security Selection ---")

    # Prompt for Security Type
    while True:
        print("Select a Security Type:")
        type_keys = list(SECURITY_MAP.keys())
        for i, key in enumerate(type_keys):
            print(f"  {i+1}. {key}")

        try:
            type_choice_str = input(f"Your choice (1-{len(type_keys)}): ")
            type_choice = int(type_choice_str) - 1
            if 0 <= type_choice < len(type_keys):
                selected_type = type_keys[type_choice]
                break  # Valid type selected
            else:
                print("Invalid choice. Please select a number from the list.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number.")

    # Prompt for Security Description
    while True:
        print("\nSelect a Security Description:")
        descriptions = SECURITY_MAP[selected_type]
        for i, desc in enumerate(descriptions):
            print(f"  {i+1}. {desc}")

        try:
            desc_choice_str = input(f"Your choice (1-{len(descriptions)}): ")
            desc_choice = int(desc_choice_str) - 1
            if 0 <= desc_choice < len(descriptions):
                selected_desc = descriptions[desc_choice]

                # Validation against existing selection
                new_security = {"type": selected_type, "desc": selected_desc}
                if existing_security and new_security == existing_security:
                    print("\nError: Already selected. Choose different security.")
                    continue  # Re-ask for the description

                return new_security  # Choice is valid and not a duplicate
            else:
                print("Invalid choice. Please select a number from the list.")

        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number.")


def run_interactive_cli():
    """Main function to run the interactive command-line interface."""
    api = TreasuryAPI()
    print("=" * 50)
    print("      Welcome to the Treasury Rate Finder CLI")
    print("=" * 50)

    while True:
        # --- Main Menu ---
        print("\nPlease select an option from the menu below:")
        print("\n  1. Research and compare Treasury securities")
        print("  2. Exit application")
        choice = input("\nYour choice: ")

        if choice == '1':
            # 1. Get Dates
            dates_to_query = prompt_for_dates()
            # If prompt_for_dates returns None due to error, loop back
            if dates_to_query is None:
                 input("\nDate entry error. Returning to main menu...")
                 continue
            if not dates_to_query: # Handle case where user finishes early
                 input("\nNo dates selected. Returning to main menu...")
                 continue

            # 2. Get Securities
            securities_to_find = []
            first_security = prompt_for_security()
            securities_to_find.append(first_security)

            while True: # Loop for compare choice validation
                compare = input("\nCompare another security? (y/n): ").lower()
                if compare in ['y', 'n']:
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

            if compare == 'y':
                # Pass first security to check for duplicates
                second_security = prompt_for_security(
                    existing_security=first_security
                    )
                securities_to_find.append(second_security)

            # 3. Fetch Data and Display Results
            print("\nFetching data, please wait...")
            all_results = []
            fetch_errors = False
            for date in dates_to_query:
                try:
                    rates_on_date = api.fetch_rates_by_date(date)
                    if not rates_on_date:
                        print(f"Info: No data found for {date}.",
                              file=sys.stderr)
                        continue # Skip date if API returns empty

                    for sec in securities_to_find:
                        found_on_date = False
                        for rate_data in rates_on_date:
                            if rate_data["security_desc"] == sec["desc"]:
                                all_results.append({
                                    "Record Date": rate_data["record_date"],
                                    "Security Type": sec["type"], # Use stored type
                                    "Security Description": rate_data["security_desc"],
                                    "Rate": rate_data["rate"]
                                })
                                found_on_date = True
                                break # Found match for this security on this date
                        # if not found_on_date:
                        #     print(f"Info: No rate found for '{sec['desc']}' on {date}.", file=sys.stderr)

                except Exception as e:
                    print(f"Error fetching data for {date}: {e}",
                          file=sys.stderr)
                    fetch_errors = True

            if all_results:
                # Sort results by date then description
                all_results.sort(key=lambda x: (x["Record Date"],
                                                x["Security Description"]))
                print("\n--- Results ---")
                print(tabulate(all_results, headers="keys", tablefmt="grid"))
            elif not fetch_errors:
                 print("\nNo matching data found for selected criteria and dates.")

            input("\nPress Enter to return to the main menu...")

        elif choice == '2':
            print("\nThank you for using the Treasury Rate Finder. Goodbye!")
            break # Exit the main loop

        else:
            print("\nInvalid choice. Please enter 1 or 2.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    # Directly run the interactive CLI when the script is executed
    try:
        run_interactive_cli()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)