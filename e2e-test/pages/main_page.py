class MainPage:
    def __init__(self, page):
        self.page = page

    def continue_setup(self):
        self.page.wait_for_selector('text="Your business address is"')
        self.page.fill('input[name="name"]', 'Andre')
        self.page.click('button[id="wizard_step_name"]')

    def enter_business_details(self, business_name: str):
        self.page.fill('input.MuiInput-input', business_name)
        self.page.click('button[id="wizard_step_category"]')
        self.page.wait_for_load_state("load", timeout=90000)

    def add_another_service(self):
        self.page.wait_for_selector('text="Add another service"')
        self.page.click('text="Add another service"')
        

    def check_new_element_price(self):
        all_elements = self.page.query_selector_all('xpath=//ul[contains(@class, "sE5AnuAdMP8osOJSg43c")]/li[contains(@class, "_7xakvo5B6Bs9yWDJ8m_q")]')
        new_element = all_elements[-1]
        price_input = new_element.query_selector('input[placeholder="Price"]')
        price_value = price_input.get_attribute('value')
        assert price_value, "The 'Price' field is empty"

    def complete_setup(self):
        self.page.click('button[id="wizard_step_services"]')
        self.page.click('ul.RX2iAqpXZsTQWN9kH7A9 li:first-child button')
        self.page.click('button[id="wizard_step_business_name/generated"]')
        self.page.wait_for_selector("button:has-text('Got it')", timeout=190000)
        #self.page.wait_for_load_state("load", timeout=90000)
        #self.page.wait_for_load_state("networkidle")

        #self.page.wait_for_selector('text="has been launched"', timeout=90000)
        #self.page.click("button:has-text('s start')")
