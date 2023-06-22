from playwright.sync_api import Page
class AuthPage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto("https://app.inita.com/auth/sign-up")

    def login(self, email: str):
       self.page.fill('input[name="email"]', email)
       self.page.click('button[type="submit"].MuiButton-root')

