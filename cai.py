import json
import os
import time
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

ROOT_DIR: str = os.path.abspath(os.path.dirname(__file__))  # Absolute root directory path
DEFAULT_WAIT_TIME: int = 15   # Default Wait time in seconds for WebBrowserWait
QUICK_WAIT_TIME: int = 2      # Quick wait time in seconds
DESIRED_VOICE = 3             # Best fitted voice for Wheatley


class Cai:
    def __init__(self, char_name: str = 'Wheatley', my_name: str = "vorkuta"):
        # Set name and prompt message
        self.my_name = my_name
        self.character_name: str = char_name
        self.prompt_message: str = f"### [START_CONTEXT: You, {self.character_name}, " \
                                   f"are able to communicate with me through my computer" \
                                   f"You are like a desktop companion on my," \
                                   f" {self.my_name}'s computer. Your purposes: " \
                                   f"help me with information, keep me company, and complete tasks. " \
                                   "The following is a list of available commands that are completed when" \
                                   "the user asks for it: {Play music, Launch game, Google something}... " \
                                   "Keep true to your personality in Portal 2, be curious, rude, moronic. " \
                                   "Do not RP in asteriks! Only speech.] ###" \
                                   "        Hello!"

        # Initialize driver
        options = self.get_options(visible=False)
        self.driver: webdriver.Firefox = webdriver.Firefox(options)

        # Initialize directories if not exist
        cookie_cache_path: str = os.path.join(ROOT_DIR, 'config', 'driver_cookies.json')
        config_folder_path: str = os.path.join(ROOT_DIR, "config")

        os.makedirs(config_folder_path, exist_ok=True)

        if not os.path.exists(cookie_cache_path):
            with open(cookie_cache_path, 'w') as file:
                json.dump([], file, indent=4)

        cookies_txt_path: str = os.path.join(ROOT_DIR, "config", "cookie.txt")
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
        Converts the .txt file given by the cookie.txt Firefox extension to the standard Netscape form.

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
                Finds element by xpath, writes, presses enter.
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
        Finds the textarea and sends the prompt message.
        At times the textarea changes to a different xpath, so we try both.
        :return: None.
        """
        text_area_xpath: str = "/html/body/div[1]/div/main/div/div/div/main/div/div/div[3]/div/div/div/div[1]/textarea"
        try:
            self.write_by_xpath(text_area_xpath, self.prompt_message, wait_time=QUICK_WAIT_TIME)
        except selenium.common.exceptions.TimeoutException:
            text_area_xpath: str = "/html/body/div[1]/div/main/div/div/div/main/div/div/div/div[3]/div/div/div/div[1]/textarea"
            self.write_by_xpath(text_area_xpath, self.prompt_message, wait_time=QUICK_WAIT_TIME)

    def get_new_chat(self) -> None:
        """
        Opens options, locates new chat button, clicks. Website automatically changes into new chat.
        At times the settings button changes to a different xpath, so we try both.
        :return: None
        """
        triple_dot_xpath: str = "/html/body/div[1]/div/main/div/div/div/main/div/div/div[1]/div[2]/div/button"
        new_chat_button_xpath: str = "/html/body/div[3]/div[4]/button[1]"
        try:
            self.click_by_xpath(triple_dot_xpath, wait_time=QUICK_WAIT_TIME)
        except selenium.common.exceptions.TimeoutException:
            triple_dot_xpath: str = "/html/body/div[1]/div/main/div/div/div/main/div/div/div/div[1]/div[2]/div/button"
            self.click_by_xpath(triple_dot_xpath, wait_time=QUICK_WAIT_TIME)
        self.click_by_xpath(new_chat_button_xpath)

    def switch_voice(self, voice_num: int) -> None:
        """
        Opens options, locates voice button and selects new voice
        :param voice_num:
        :return:
        """
        if voice_num == 1:
            return

        triple_dot_xpath: str = "/html/body/div[1]/div/main/div/div/div/main/div/div/div[1]/div[2]/div/button"
        voice_button_xpath: str = "/html/body/div[3]/div[4]/div[1]/button"
        desired_voice_xpath: str = f"/html/body/div[4]/div[3]/div[2]/div[{voice_num}]/button[2]"
        try:
            self.click_by_xpath(triple_dot_xpath)
            self.click_by_xpath(voice_button_xpath)
            self.click_by_xpath(desired_voice_xpath)
        except selenium.common.exceptions.TimeoutException:
            # Press escape to close the pop-up
            webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(QUICK_WAIT_TIME)


    def interrupt(self) -> None:
        """
        Can only be used while in a call, otherwise will throw an error. Clicks the interrupt button.
        :return:
        """
        interrupt_button_xpath: str = "/html/body/div[1]/div/main/div/div/div/main/div[2]/div/div[2]/button"
        self.click_by_xpath(interrupt_button_xpath)

    def is_making_sound(self) -> bool:
        """
        :return: True if webdriver is making audio, false otherwise
        """
        try:
            # If we can find the interrupt button, it means character is speaking.
            interrupt_button_xpath: str = "/html/body/div[1]/div/main/div/div/div/main/div[2]/div/div[2]/button"
            button = self.driver.find_element(By.XPATH, interrupt_button_xpath)
            return button.is_displayed()
        except selenium.common.exceptions.NoSuchElementException:
            return False

    def run(self):
        cai_website: str = "https://character.ai/"
        cai_character: str = "https://character.ai/chat/l7714PjXVoRSsP6l2WYIPHkLKX3KQVbdA6ulZ5oS__M"
        call_xpath: str = "/html/body/div[1]/div/main/div/div/div/main/div/div/div[3]/div/div/button"


        # Load cookies and reload into character's chat
        self.driver.get(cai_website)
        self.load_cookies()
        self.driver.get(cai_character)
        # Ensures the website loads properly before writing
        time.sleep(QUICK_WAIT_TIME)

        if self.is_first_run():
            self.get_new_chat()
            time.sleep(QUICK_WAIT_TIME)
            self.initialize_chat()
            time.sleep(QUICK_WAIT_TIME)
            self.switch_voice(DESIRED_VOICE)
            # Create empty BIRTH file, indicating program ran at least once.
            open(os.path.join(ROOT_DIR, "config", "BIRTH"), 'a').close()

        # Click call button
        try:
            self.click_by_xpath(xpath=call_xpath, wait_time=QUICK_WAIT_TIME)
        except selenium.common.exceptions.TimeoutException:
            call_xpath: str = "/html/body/div[1]/div/main/div/div/div/main/div/div/div/div[3]/div/div/button"
            self.click_by_xpath(xpath=call_xpath, wait_time=QUICK_WAIT_TIME)


if __name__ == "__main__":
    web_manager = Cai()
    web_manager.run()
