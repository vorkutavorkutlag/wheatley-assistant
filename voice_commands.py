import selenium.common.exceptions
from RealtimeSTT import AudioToTextRecorder   # Thanks, KoljaB!
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pygame import mixer
import os
import random
from cai import Cai

ROOT_DIR: str = os.path.abspath(os.path.dirname(__file__))
QUICK_WAIT_TIME: int = 2      # Quick wait time in seconds


class commandhandler:
    def __init__(self, cai_reference: Cai):
        """
        Dynamically creates a phrase<->function dictionary
        """
        mixer.init()
        mixer.music.set_volume(0.2)

        self.commands: dict[str, callable] = {}
        self.cai_reference: Cai = cai_reference
        self.driver: (webdriver.Chrome, None) = None

        for attr in dir(self):
            if attr[:1] == "_" or attr[:1] == "c":
                continue
            spaced_attr: str = attr.replace("_", " ")
            self.commands[spaced_attr] = getattr(self, attr)

    def terminate_application(self) -> None:
        """
        Closes webdriver (CAI connection), driver, and shuts program down
        :return: None
        """
        try:
            self.terminate_google()
        finally:
            try:
                self.cai_reference.driver.quit()
                os._exit(0)
            except (BrokenPipeError, ):
                return

    # @staticmethod
    # def play_music() -> None:
    #     """
    #     Randomly chooses a song/audio to play from the music folder
    #     :return: None
    #     """
    #     # In case something is already playing, stop it and choose another
    #     if mixer.Channel(0).get_busy():
    #         mixer.stop()
    #     path_to_music_folder: str = os.path.join(ROOT_DIR, "music")
    #     audio_file: str = random.choice(os.listdir(path_to_music_folder))
    #     audio_file_path: str = os.path.join(ROOT_DIR, "music", audio_file)
    #     mixer.music.load(audio_file_path)
    #     mixer.music.play()
    #     return
    #
    # @staticmethod
    # def pause_music() -> None:
    #     """
    #     Stops whatever song/audio is playing
    #     :return: None
    #     """
    #     mixer.music.pause()

    def init_webdriver(self) -> None:
        """
        Loads extensions and creates webdriver
        :return:
        """
        extensions_path: str = os.path.join(ROOT_DIR, "extensions")
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['--headless'])
        for extension in os.listdir(extensions_path):
            extension_abspath: str = os.path.join(extensions_path, extension)
            options.add_extension(extension_abspath)

        self.driver = webdriver.Chrome(options=options)

    def on_youtube_play(self, text_args: str):
        if self.driver is None:
            self.init_webdriver()

        search_query: str = 'https://www.youtube.com/results?search_query={}'.format(text_args)
        self.driver.get(search_query)

        WebDriverWait(self.driver, QUICK_WAIT_TIME).until(EC.visibility_of_element_located((By.ID, "video-title")))
        self.driver.find_element(By.ID, "video-title").click()


    @staticmethod
    def lets_play_a_random_game() -> None:
        """
        Made for Windows, randomly launches a game from steam.
        :return: None
        """

        steam_path: str = r"C:\Program Files (x86)\Steam\steamapps\common"
        tries: int = 0
        while True:
            if tries >= 10:
                return
            chosen_game_fp: str = os.path.join(steam_path, random.choice(os.listdir(steam_path)))
            for file in os.listdir(chosen_game_fp):
                if file.endswith(".exe") and not file.startswith("Unity"):
                    abs_file_path = os.path.join(steam_path, chosen_game_fp, file)
                    os.startfile(abs_file_path)
                    return
            tries += 1


    @staticmethod
    def lets_play_isaac() -> None:
        """
        Okay, this is more for personal use. Change this function / the following with games applicable for you
        :return: None
        """
        isaac_path: str = r"C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth\isaac-ng.exe"
        try:
            os.startfile(isaac_path)
        except FileNotFoundError:
            return

    def shut_up(self) -> None:
        """
        See cai.py for docs on interrupt function
        :return: None
        """
        try:
            self.cai_reference.interrupt()
        except selenium.common.exceptions.TimeoutException:
            # Meaning it did not find the interruption button - meaning character was not speaking
            return

    def terminate_google(self) -> None:
        """
        Closes the temporary webdriver
        :return: None
        """
        try:
            self.driver.close()
            self.driver = None
        except AttributeError:
            return

    def please_google(self, text_args: str) -> None:
        """
        Uses selenium to open google and search text.
        :param text_args:
        :return:
        """
        if self.driver is None:
            self.init_webdriver()

        self.driver.get("https://www.google.com")
        text_area: EC.element_to_be_clickable = WebDriverWait(self.driver, QUICK_WAIT_TIME).until(
            EC.element_to_be_clickable((By.NAME, 'q')))

        text_area.send_keys(text_args)
        text_area.send_keys(Keys.ENTER)

    def process_text(self, text: str) -> None:
        """
        Finds appropriate function for user's input, if one even exists
        :param text: None
        :return:
        """
        print(text)
        # Filter text
        text = text.lower()
        text = text.replace("'", "")
        text = text.replace(",", "")
        for func_name in self.commands.keys():
            if func_name in text:
                try:
                    text_args: str = text.split(func_name, 1)[1]
                    self.commands[func_name](text_args)
                except TypeError:
                    self.commands[func_name]()
                return

    def run(self) -> None:
        """
        Runs STT indefinitely, constantly inputs user's voice
        :return: None
        """
        print("Wait until you can see character")
        recorder = AudioToTextRecorder()

        while True:
            recorder.text(self.process_text)


if __name__ == "__main__":
    ch = commandhandler()
    ch.run()
