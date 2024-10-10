import cai
import voice_commands
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
            volume.SetMasterVolume(0.4, None)


def main():
    web_manager: cai.Cai = cai.Cai()
    voice_command_manager: voice_commands.commandhandler = voice_commands.commandhandler(web_manager)

    cai_thread: Thread = Thread(target=web_manager.run)
    vc_thread: Thread = Thread(target=voice_command_manager.run)
    threads: list[Thread] = [cai_thread, vc_thread]
    for thread in threads:
        thread.start()

    try:
        turn_volume_down()
    except:
        # Most likely because user uses Linux
        pass

    for thread in threads:
        thread.join()



if __name__ == "__main__":
    main()