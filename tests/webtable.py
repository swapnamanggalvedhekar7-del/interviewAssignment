"""Scrape market table data from the EPEX Spot website and save it as CSV."""

import pandas as pd
from playwright.sync_api import Playwright


def test_scrape_to_csv(playwright: Playwright, browser_page, launch_browser):
    # `browser_page` is supplied by the test fixture and gives access to the page.
    page = browser_page

    # Open the target market data page for the selected date and product.
    page.goto(
        "https://www.epexspot.com/en/market-results?market_area=GB&auction=&delivery_date=2026-10-09&underlying_year=&modality=Continuous&sub_modality=&technology=&data_mode=table&period=&production_period=&product=30"
    )

    # Wait for the page to finish loading dynamic data before reading the table.
    page.wait_for_timeout(2000)

    # Access the table body and extract all rows in the page.
    table = page.locator("table tbody")
    rows = table.locator("tr")
    all_rows = rows.all()

    # Create separate lists for each column we want to export.
    cells_low = []
    cells_high = []
    cells_last = []
    cells_weight_avg = []

    # Read each row from the table and collect the cell values.
    for rows in all_rows:
        # Remove the bracket formatting returned by Playwright's text extraction.
        text_low = str(rows.locator("td").nth(1).all_inner_texts())
        text_low = text_low.replace("[", "").replace("]", "")
        cells_low.append(text_low)

        text_high = str(rows.locator("td").nth(1).all_inner_texts())
        text_high = text_high.replace("[", "").replace("]", "")
        cells_high.append(text_high)

        text_last = str(rows.locator("td").nth(1).all_inner_texts())
        text_last = text_last.replace("[", "").replace("]", "")
        cells_last.append(text_last)

        text_weight_avg = str(rows.locator("td").nth(1).all_inner_texts())
        text_weight_avg = text_weight_avg.replace("[", "").replace("]", "")
        cells_weight_avg.append(text_weight_avg)

    # Print the collected values for quick debugging during test execution.
    print(cells_low)
    print(cells_high)
    print(cells_last)
    print(cells_weight_avg)

    try:
        # Convert the lists into a pandas DataFrame and save them to CSV.
        df = pd.DataFrame(
            {
                "Low": cells_low,
                "high": cells_high,
                "last": cells_last,
                "weight_avg": cells_weight_avg,
            }
        )
        df.to_csv("testdata\\webscrape.csv", index=False)
    except Exception as e:
        # Re-raise with a clearer message if CSV generation fails.
        raise Exception(f"Error in creating csv file {e}")

