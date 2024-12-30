import cai
import voice_commands
import desktop_presence
from threading import Thread
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume


def turn_volume_down() -> None:
    """
    Uses pycaw to turn volume down. Incompatible with Linux
    :return: None
    """
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "firefox.exe":
            volume.SetMasterVolume(0.2, None)


def main():
    """
    The main function for Wheatley Assistant.
    Creates several threads for each component of the application and runs them.
    :return: None
    """
    web_manager: cai.Cai = cai.Cai()
    voice_command_manager: voice_commands.commandhandler = voice_commands.commandhandler(web_manager)

    cai_thread: Thread = Thread(target=web_manager.run)
    vc_thread: Thread = Thread(target=voice_command_manager.run)
    dp_thread: Thread = Thread(target=desktop_presence.run, args=(web_manager,))
    threads: list[Thread] = [cai_thread, vc_thread, dp_thread]
    for thread in threads:
        thread.start()

    try:
        turn_volume_down()
    except Exception:
        # Most likely because user does not use Windows
        pass

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
