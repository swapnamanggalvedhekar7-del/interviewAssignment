import pytest
from playwright.sync_api import Playwright
from pyjavaproperties import Properties


path = "config.properties"

@pytest.fixture(scope= "session")
def launch_browser(base_url,playwright:Playwright):
    p = Properties()
    p.load(open(path))

    browser = p["browser"]
    if browser.lower() == 'chrome':
        return playwright.chromium.launch(headless=False)
    elif browser.lower() == 'Firefox':
        return playwright.firefox.launch(headless=False)
    else:
        return playwright.webkit.launch(headless=False)

@pytest.fixture(scope="function")
def browser_page(launch_browser):
    context = launch_browser.new_context()
    page = context.new_page()
    return page