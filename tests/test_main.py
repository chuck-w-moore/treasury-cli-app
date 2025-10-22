import pytest
from unittest.mock import patch
import sys

# Modifying sys.argv allows simulating command-line arguments for testing.
# The main function is imported within tests after sys.argv is patched.
# This pattern facilitates testing argparse-based CLIs.

# Define sample data returned by the mocked API
MOCK_API_DATA = [
    {
        "record_date": "2023-09-30",
        "security_type_desc": "Marketable",
        "security_desc": "Treasury Bills",
        "rate": "4.187%",
    },
    {
        "record_date": "2023-09-30",
        "security_type_desc": "Marketable",
        "security_desc": "Treasury Notes",
        "rate": "3.112%",
    },
    {
        "record_date": "2023-08-31",
        "security_type_desc": "Marketable",
        "security_desc": "Treasury Bills",
        "rate": "4.000%",
    },
]


# --- Test Cases ---

@patch('src.main.TreasuryAPI')  # Mock the entire TreasuryAPI class
def test_lookup_single_security(mock_api_class, capsys):
    """Test the 'lookup' command with one security."""
    # Configure the mock instance's method
    mock_api_instance = mock_api_class.return_value
    mock_api_instance.fetch_rates_by_date.return_value = MOCK_API_DATA

    # Simulate command line arguments
    test_args = ['src/main.py', 'lookup', '--dates', '2023-09-30',
                 '--security1', 'Treasury Bills']
    with patch.object(sys, 'argv', test_args):
        # Import inside test function after patching sys.argv
        from src.main import main
        main()

    # Capture the output
    captured = capsys.readouterr()

    # Assertions
    mock_api_instance.fetch_rates_by_date.assert_called_once_with('2023-09-30')
    assert "--- Results ---" in captured.out
    assert "Treasury Bills" in captured.out
    assert "4.187%" in captured.out
    # Should only show the requested security
    assert "Treasury Notes" not in captured.out
    assert "Error" not in captured.err


@patch('src.main.TreasuryAPI')
def test_lookup_compare_securities(mock_api_class, capsys):
    """Test the 'lookup' command comparing two securities."""
    mock_api_instance = mock_api_class.return_value
    mock_api_instance.fetch_rates_by_date.return_value = MOCK_API_DATA

    test_args = ['src/main.py', 'lookup', '--dates', '2023-09-30',
                 '--security1', 'Treasury Bills',
                 '--security2', 'Treasury Notes']
    with patch.object(sys, 'argv', test_args):
        from src.main import main
        main()

    captured = capsys.readouterr()
    mock_api_instance.fetch_rates_by_date.assert_called_once_with('2023-09-30')
    assert "Treasury Bills" in captured.out
    assert "4.187%" in captured.out
    assert "Treasury Notes" in captured.out
    assert "3.112%" in captured.out
    assert "Error" not in captured.err


@patch('src.main.TreasuryAPI')
def test_range_command(mock_api_class, capsys):
    """Test the 'range' command."""
    mock_api_instance = mock_api_class.return_value
    # Simulate API returning data for multiple dates

    def side_effect(date):
        if date == "2023-08-31":
            return [MOCK_API_DATA[2]]  # Only Bills for Aug
        elif date == "2023-09-30":
            return MOCK_API_DATA[0:1]  # Only Bills for Sep
        return []
    mock_api_instance.fetch_rates_by_date.side_effect = side_effect

    test_args = ['src/main.py', 'range', '--start-date', '2023-08',
                 '--end-date', '2023-09', '--security1', 'Treasury Bills']
    with patch.object(sys, 'argv', test_args):
        from src.main import main
        main()

    captured = capsys.readouterr()
    assert mock_api_instance.fetch_rates_by_date.call_count == 2
    mock_api_instance.fetch_rates_by_date.assert_any_call('2023-08-31')
    mock_api_instance.fetch_rates_by_date.assert_any_call('2023-09-30')
    assert "2023-08-31" in captured.out
    assert "4.000%" in captured.out
    assert "2023-09-30" in captured.out
    assert "4.187%" in captured.out
    assert "Error" not in captured.err


def test_list_securities(capsys):
    """Test the 'list-securities' command."""
    test_args = ['src/main.py', 'list-securities']
    with patch.object(sys, 'argv', test_args):
        from src.main import main
        main()

    captured = capsys.readouterr()
    assert "Available Treasury Securities" in captured.out
    assert "Marketable" in captured.out
    assert "Treasury Bills" in captured.out
    assert "Non-marketable" in captured.out
    assert "Interest-bearing Debt" in captured.out
    assert "Error" not in captured.err


# --- Error Handling Tests ---

@patch('src.main.TreasuryAPI')
def test_lookup_invalid_date_format(mock_api_class, capsys):
    """Test 'lookup' with an invalid date format."""
    test_args = ['src/main.py', 'lookup', '--dates', '2023/09/30',
                 '--security1', 'Treasury Bills']
    with patch.object(sys, 'argv', test_args):
        from src.main import main
        # Argparse errors usually cause SystemExit
        with pytest.raises(SystemExit):
            main()

    captured = capsys.readouterr()
    assert "Error: Invalid date format '2023/09/30'" in captured.err


@patch('src.main.TreasuryAPI')
def test_lookup_too_many_dates(mock_api_class, capsys):
    """Test 'lookup' with more than 5 dates."""
    dates = ['2023-01-31', '2023-02-28', '2023-03-31', '2023-04-30',
             '2023-05-31', '2023-06-30']
    test_args = ['src/main.py', 'lookup', '--dates'] + dates + \
                ['--security1', 'Treasury Bills']
    with patch.object(sys, 'argv', test_args):
        from src.main import main
        with pytest.raises(SystemExit):
            main()

    captured = capsys.readouterr()
    assert "Error: Maximum of 5 dates allowed" in captured.err


@patch('src.main.TreasuryAPI')
def test_lookup_invalid_security(mock_api_class, capsys):
    """Test 'lookup' with an invalid security description."""
    test_args = ['src/main.py', 'lookup', '--dates', '2023-09-30',
                 '--security1', 'Invalid Security']
    with patch.object(sys, 'argv', test_args):
        from src.main import main
        with pytest.raises(SystemExit):
            # Argparse's type validation should raise an error and exit
            main()

    captured = capsys.readouterr()
    # Argparse prints usage info and the error message to stderr
    assert "Invalid security description: 'Invalid Security'" in captured.err


@patch('src.main.TreasuryAPI')
def test_range_invalid_date_format(mock_api_class, capsys):
    """Test 'range' with invalid YYYY-MM format."""
    test_args = ['src/main.py', 'range', '--start-date', '2023-13',
                 '--end-date', '2024-01', '--security1', 'Treasury Bills']
    with patch.object(sys, 'argv', test_args):
        from src.main import main
        with pytest.raises(SystemExit):
            main()

    captured = capsys.readouterr()
    assert "Error: Invalid date format. Use YYYY-MM." in captured.err


@patch('src.main.TreasuryAPI')
def test_range_start_after_end(mock_api_class, capsys):
    """Test 'range' where start date is after end date."""
    test_args = ['src/main.py', 'range', '--start-date', '2024-01',
                 '--end-date', '2023-12', '--security1', 'Treasury Bills']
    with patch.object(sys, 'argv', test_args):
        from src.main import main
        with pytest.raises(SystemExit):
            main()

    captured = capsys.readouterr()
    assert "Error: Start date cannot be after end date." in captured.err


@patch('src.main.TreasuryAPI')
def test_lookup_same_securities(mock_api_class, capsys):
    """Test 'lookup' comparing the same security."""
    test_args = ['src/main.py', 'lookup', '--dates', '2023-09-30',
                 '--security1', 'Treasury Bills',
                 '--security2', 'Treasury Bills']
    with patch.object(sys, 'argv', test_args):
        from src.main import main
        with pytest.raises(SystemExit):
            main()

    captured = capsys.readouterr()
    assert "Error: Security 1 and Security 2 cannot be the same." in captured.err
