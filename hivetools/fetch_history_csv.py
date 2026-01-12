#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = [
#     "httpx",
#     "rich",
# ]
# ///

import argparse
import csv
import datetime

import httpx
from rich.console import Console

console = Console()

# Default Defaults
DEFAULT_ACCOUNT = "null"
DEFAULT_SYMBOL = "SIM"


def get_history(account: str, symbol: str):
    """
    Fetches account history from Hive Engine with pagination.
    """
    url = "https://history.hive-engine.com/accountHistory"
    limit = 500
    offset = 0
    all_data = []

    console.print(
        f"[cyan]Fetching history for account: [bold]{account}[/bold], symbol: [bold]{symbol}[/bold]...[/cyan]"
    )

    with httpx.Client(timeout=30.0) as client:
        while True:
            params = {
                "account": account,
                "symbol": symbol,
                "limit": limit,
                "offset": offset,
            }

            try:
                response = client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if not data:
                    break

                all_data.extend(data)
                console.print(f"  Fetched {len(data)} records (Total: {len(all_data)})")

                if len(data) < limit:
                    break

                offset += limit

            except httpx.HTTPError as e:
                console.print(f"[red]HTTP error occurred: {e}[/red]")
                break
            except Exception as e:
                console.print(f"[red]An error occurred: {e}[/red]")
                break

    return all_data


def save_to_csv(data, filename):
    """
    Saves the list of dictionaries to a CSV file with timestamp conversion.
    """
    if not data:
        console.print("[yellow]No data to save.[/yellow]")
        return

    # Use keys from the first record as fieldnames
    fieldnames = list(data[0].keys())

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        count = 0
        for row in data:
            # Convert timestamp
            ts = row.get("timestamp")
            if ts:
                try:
                    # Convert Unix timestamp to human-readable format
                    dt_object = datetime.datetime.fromtimestamp(
                        ts, tz=datetime.timezone.utc
                    )
                    # Formatting as ISO 8601-like string which is very readable
                    row["timestamp"] = dt_object.strftime("%Y-%m-%d %H:%M:%S UTC")
                except Exception:
                    # If conversion fails, keep the original value
                    pass

            writer.writerow(row)
            count += 1

    console.print(
        f"[green]Successfully saved [bold]{count}[/bold] records to [bold]{filename}[/bold][/green]"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Hive Engine account history and save to CSV."
    )
    parser.add_argument(
        "--account",
        type=str,
        default=DEFAULT_ACCOUNT,
        help=f"The account to fetch history for (default: {DEFAULT_ACCOUNT})",
    )
    parser.add_argument(
        "--symbol",
        type=str,
        default=DEFAULT_SYMBOL,
        help=f"The token symbol (default: {DEFAULT_SYMBOL})",
    )

    args = parser.parse_args()

    output_file = f"history_{args.account}_{args.symbol}.csv"

    data = get_history(args.account, args.symbol)
    save_to_csv(data, output_file)


if __name__ == "__main__":
    main()
