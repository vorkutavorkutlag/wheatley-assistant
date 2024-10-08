import json
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

ROOT_DIR: str = os.path.abspath(os.path.dirname(__file__))  # Absolute root directory path
DEFAULT_WAIT_TIME: int = 5   # Wait time in seconds


class Cai:
    def __init__(self, char_name: str = 'Wheatley') -> None:
        # Set name
        self.character_name: str = char_name

        # Initialize driver
        options = self.get_options(visible=False)
        self.driver: webdriver.Firefox = webdriver.Firefox(options)

        # Initialize directories if not exist
        cookie_cache_path: str = os.path.join(ROOT_DIR, 'config', 'driver_cookies.json')
        cookies_folder_path: str = os.path.join(ROOT_DIR, "config")

        os.makedirs(cookies_folder_path, exist_ok=True)

        if not os.path.exists(cookie_cache_path):
            with open(cookie_cache_path, 'w') as file:
                json.dump([], file, indent=4)

        cookies_txt_path: str = os.path.join(ROOT_DIR, "config", "config.txt")
        if os.path.exists(cookies_txt_path):
            self.netscape_convertor(cookies_txt_path, cookie_cache_path)
            os.remove(cookies_txt_path)

    @staticmethod
    def get_options(visible: bool = False, disable_perm: bool = True, fake_streams: bool = False) -> Options:
        options = Options()
        options.set_preference("media.navigator.permission.disabled", disable_perm)
        options.set_preference("media.navigator.streams.fake", fake_streams)
        if not visible:
            options.add_argument("--headless")
        return options

    @staticmethod
    def netscape_convertor(file_path: str, cookie_cache_path: str) -> None:
        """
        Converts the .txt file given by the config.txt Firefox extension to the standard Netscape form.

        :param cookie_cache_path: Path to the cookie cache. Usually config/driver_cookies.json
        :param file_path: Path to the cookie.txt file downloaded from the Firefox extension
        :return: None. Only writes to designated json file.
        """

        added_cookies: list[dict] = []

        with open(file_path, 'r') as cookiestxt:
            for line in cookiestxt:
                if line.startswith('#') or line.strip() == "":
                    continue

                args: list[str] = line.strip().split("\t")

                if len(args) < 7:
                    continue  # Skip if there are not enough arguments

                # Convert boolean strings to actual booleans
                http_only = args[1].strip().lower() == "true"
                secure = args[3].strip().lower() == "true"

                # Handle expiry as an integer
                expiry = int(args[4]) if args[4].isdigit() else None

                cookie: dict = {
                    "domain": args[0].strip(),
                    "httpOnly": http_only,
                    "path": args[2].strip(),
                    "secure": secure,
                    "expiry": expiry,
                    "name": args[5].strip(),
                    "value": args[6].strip()  # Strip only value if necessary
                }
                added_cookies.append(cookie)

        # Write to the json file
        with open(cookie_cache_path, 'r+') as file:
            existing_cookies: list[dict] = json.load(file)
            existing_cookies.extend(added_cookies)
            file.seek(0)
            json.dump(existing_cookies, file, indent=4)

    @staticmethod
    def is_first_run() -> bool:
        """
        :return:  True if program ran for first time, false if not first time
        """
        return not os.path.exists(os.path.join(ROOT_DIR, "config", "BIRTH"))

    def click_by_xpath(self, xpath: str, wait_time: int = DEFAULT_WAIT_TIME) -> None:
        """
        :param wait_time: How much time we want to wait before clicking
        :param xpath: xpath to the element we want to be clicked
        :return: None
        """
        call_button: EC.element_to_be_clickable = WebDriverWait(self.driver, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        call_button.click()

    def write_by_xpath(self, xpath: str, text: str, wait_time: int = DEFAULT_WAIT_TIME) -> None:
        """
                :param wait_time: How much time we want to wait before clicking
                :param xpath: xpath to the element we want to be clicked
                :param text: the text we want entered and sent in the textarea
                :return: None
                """
        text_area: EC.element_to_be_clickable = WebDriverWait(self.driver, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        text_area.send_keys(text)
        text_area.send_keys(Keys.ENTER)

    def load_cookies(self) -> None:
        """
        Opens the cookies in the config and loads them into the driver
        :return:  None.
        """
        with open(os.path.join(ROOT_DIR, "config", "driver_cookies.json"), 'r') as cookies_json:
            cookies = json.load(cookies_json)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def initialize_chat(self) -> None:
        """
        Writes a detailed prompt for the bot to follow in the future and sends it.
        :return: None.
        """
        initializer_message: str = "[WHATEVER IS IN BRACKETS IS OUTSIDE OF ROLEPLAY] [Context: You are a sentient " \
                                   "desktop companion on my, the user's, computer. Your purpose is to help me with " \
                                   "information, keep me company, and complete my commands. The following is a list " \
                                   "of available commands that can be completed whenever the user asks for it: " \
                                   "{CURRENTLY EMPTY}. For your first message, say 'BOOTING UP'.]"
        text_area_xpath: str = f"//textarea[@placeholder='Message {self.character_name}...']"
        self.write_by_xpath(text_area_xpath, initializer_message)


    def run(self):
        cai_website: str = "https://character.ai/"
        cai_wheatley: str = "https://character.ai/chat/l7714PjXVoRSsP6l2WYIPHkLKX3KQVbdA6ulZ5oS__M"
        call_xpath: str = "//button[@data-state='closed' and not(contains(@aria-haspopup, 'dialog')) and contains(" \
                          "@class, 'inline-flex') and not(contains(., 'Create'))] "


        # Load cookies and reload into Wheatley's chat
        self.driver.get(cai_website)
        self.load_cookies()
        self.driver.get(cai_wheatley)

        if self.is_first_run():
            self.initialize_chat()
            # Create empty BIRTH file, indicating program ran at least once.
            open(os.path.join(ROOT_DIR, "config", "BIRTH"), 'a').close()
            self.driver.get(cai_wheatley)  # For whatever reason kicks you out of the chat. No problem, we get back in

        self.click_by_xpath(xpath=call_xpath)






if __name__ == "__main__":
    web_manager = Cai()
    web_manager.run()
