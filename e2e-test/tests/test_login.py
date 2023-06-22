import pytest
import json
import datetime
import logging
from typing import List
import random
import json
import urllib
import subprocess
from playwright.sync_api import sync_playwright
from pages import AuthPage, MainPage, ProfilePage

desired_cap = {
  'browser': 'chrome',  # allowed browsers are `chrome`, `edge`, `playwright-chromium`, `playwright-firefox` and `playwright-webkit`
  'browser_version': 'latest', # this capability is valid only for branded `chrome` and `edge` browsers and you can specify any browser version like `latest`, `latest-beta`, `latest-1` and so on.
  'os': 'osx',
  'os_version': 'catalina',
  'name': 'Branded Google Chrome on Catalina',
  'build': 'playwright-python-1',
  'browserstack.username': 'inita_431LrJ',
  'browserstack.accessKey': 'zsZt2WpzqncLWqXshGyS',
  'browserstack.networkLogs' : 'true',
  'browserstack.networkLogsOptions': {
    'captureContent': 'true'
}

}

# Configure logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def read_test_data(file_path: str) -> List[str]:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

@pytest.fixture(scope="function")
def setup():
    network_types_to_log = ["fetch", "xhr"]
    playwright = sync_playwright().start()

    clientPlaywrightVersion = str(subprocess.getoutput('playwright --version')).strip().split(" ")[1]
    desired_cap['client.playwrightVersion'] = clientPlaywrightVersion

    cdpUrl = 'wss://cdp.browserstack.com/playwright?caps=' + urllib.parse.quote(json.dumps(desired_cap))

    browser = playwright.chromium.connect(cdpUrl)
    context = browser.new_context()
    page = context.new_page()

    yield page, network_types_to_log

    browser.close()
    playwright.stop()

def check_graphql_errors(response, network_types_to_log):
    text_body = None
    try:
        resource_type = response.request.resource_type
        if resource_type not in network_types_to_log:
            return
        request = response.request
        request_body = request.post_data
        text_body = response.text()
        logging.debug(f"Request URL: {request.url}")
        logging.debug(f"Request method: {request.method}")
        logging.debug(f"Request headers: {request.headers}")
        logging.debug(f"Request body: {request_body}")
        logging.debug(f"Response status: {response.status}")
        logging.debug(f"Response headers: {response.headers}")
        logging.debug(f"Response body: {text_body}")
        json_bodies = text_body.split("\n")
        for json_body in json_bodies:
            if json_body:
                try:
                    json_body = json.loads(json_body)
                except json.JSONDecodeError:
                    logging.error(f"JSONDecodeError: Could not decode the response: {json_body}")
                    continue
                # Here is where you add the isinstance check
                if isinstance(json_body, dict) and "errors" in json_body:
                    logging.error(f"GraphQL error in response: {json_body}")
        if response.status >= 400:
            logging.error(f"HTTP error {response.status} in response: {response.url}")
    except UnicodeDecodeError:
        if text_body is not None:
            logging.error(f"UnicodeDecodeError: Could not decode the response: {text_body}")
        else:
            logging.error("UnicodeDecodeError: Could not get the text from the response")
    except Exception as e:
        logging.error(f"Error in check_graphql_errors: {str(e)}")
        raise


def test_login_process(setup):
    page, network_types_to_log = setup
    try:
        page.on("response", lambda res: check_graphql_errors(res, network_types_to_log))
        auth_page = AuthPage(page)
        auth_page.goto()
        random_number = random.randint(100, 1000)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        email_to_login = 'deploytorelease' + str(random_number) + '@inita.com'
        auth_page.login(email_to_login)
        main_page = MainPage(page)
        main_page.continue_setup()
        test_data = read_test_data('tests/test_data.txt')
        random_business_name = random.choice(test_data)
        main_page.enter_business_details(random_business_name)
        main_page.add_another_service()
        main_page.check_new_element_price()
        main_page.complete_setup()

        profile_page = ProfilePage(page)
        profile_page.go_to_profile()
        new_page = profile_page.go_to_website()
        new_page.screenshot(path=f'screenshots_site/{str(timestamp)}_{email_to_login}.png', full_page=True)
        new_page.close()
        profile_page.go_to_profile()
        profile_page.delete_account()
        executor_object = {
            'action': 'setSessionStatus',
            'arguments': {
                'status': "passed",
                'reason': "All steps completed successfully"
            }
        }
        browserstack_executor = 'browserstack_executor: {}'.format(json.dumps(executor_object))
        page.evaluate(browserstack_executor)
    except Exception as e:
        logging.error(f"Exception occurred", exc_info=True)
        page.screenshot(path=f'screenshots/error_{str(e)}_{email_to_login}.png', full_page=True)
        executor_object = {
            'action': 'setSessionStatus',
            'arguments': {
                'status': "failed",
                'reason': str(e)
            }
        }
        browserstack_executor = 'browserstack_executor: {}'.format(json.dumps(executor_object))
        page.evaluate(browserstack_executor)
        raise