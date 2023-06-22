class ProfilePage:
    def __init__(self, page):
        self.page = page

    def go_to_profile(self):
        self.page.wait_for_selector('xpath:"//*[@id=\'__next\']/div[2]/div/div/div/div/div[1]/span/svg"', timeout=3000)
        self.page.click('xpath:"//*[@id=\'__next\']/div[2]/div/div/div/div/div[1]/span/svg"')
        try:


            self.page.wait_for_selector("button:has-text('Got it')", timeout=2000)
            self.page.click("button:has-text('Got it')")
        except Exception:
            pass  # Если кнопка не появилась в течение 2 секунд, просто продолжаем выполнение
        self.page.click("a[href='/dashboard/profile']")
        try:
            self.page.wait_for_selector("button:has-text('Got it')", timeout=2000)
            self.page.click("button:has-text('Got it')")
        except Exception:
            pass  # Если кнопка не появилась в течение 2 секунд, просто продолжаем выполнение


    def go_to_website(self):
        self.page.click("a[href='/dashboard/edit-website']")
        self.page.click("button:has-text('Got it')")

        with self.page.expect_popup() as new_page_info:
            self.page.click("button:has-text('Visit My Website')")
        
        new_page = new_page_info.value
        new_page.wait_for_load_state("load", timeout=90000)

        return new_page

    def delete_account(self):
        self.page.click("button:has-text('Delete account')")
        self.page.click("button:has-text('Delete my account')")
        self.page.wait_for_load_state("load")
