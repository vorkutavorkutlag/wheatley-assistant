from RealtimeSTT import AudioToTextRecorder   # Thanks, KoljaB!
from selenium import webdriver
from pygame import mixer
import sys
import os
import random
from cai import Cai

ROOT_DIR: str = os.path.abspath(os.path.dirname(__file__))


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

    @staticmethod
    def kill_program(driver: webdriver.Firefox) -> None:
        """
        Closes webdriver (CAI connection) and shuts program down
        :param driver: Reference to the webdriver connected to CAI
        :return: None
        """
        driver.quit()
        sys.exit()

    @staticmethod
    def play_music() -> None:
        """
        Randomly chooses a song/audio to play from the music folder
        :return: None
        """
        # In case something is already playing, stop it and choose another
        if mixer.Channel(0).get_busy():
            mixer.stop()
        path_to_music_folder: str = os.path.join(ROOT_DIR, "music")
        audio_file: str = random.choice(os.listdir(path_to_music_folder))
        audio_file_path: str = os.path.join(ROOT_DIR, "music", audio_file)
        mixer.music.load(audio_file_path)
        mixer.music.play()
        return

    @staticmethod
    def pause_music() -> None:
        """
        Stops whatever song/audio is playing
        :return: None
        """
        mixer.music.pause()

    @staticmethod
    def lets_play_a_game() -> None:
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
                if file.endswith(".exe"):
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
        os.startfile(isaac_path)

    def shut_up(self) -> None:
        """
        See cai.py for docs on interrupt function
        :return: None
        """
        self.cai_reference.interrupt()

    def google(self, text_args: str) -> None:
        """
        Uses selenium to open google and search text. Uses cai.py's write_by_xpath function.
        :param text_args:
        :return:
        """
        search_textarea_xpath: str = "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea"
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.google.com")
        self.cai_reference.write_by_xpath(search_textarea_xpath, text_args)

    def kill_google(self) -> None:
        """
        Closes the temporary webdriver
        :return: None
        """
        try:
            self.driver.close()
            self.driver = None
        except AttributeError:
            return

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
        print("Wait until it says 'speak now'")
        recorder = AudioToTextRecorder()

        while True:
            recorder.text(self.process_text)


if __name__ == "__main__":
    ch = commandhandler()
    ch.run()
