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

    cai_proc: Thread = Thread(target=web_manager.run)
    vc_proc: Thread = Thread(target=voice_command_manager.run)
    procs: list[Thread] = [cai_proc, vc_proc]
    for proc in procs:
        proc.start()

    turn_volume_down()

    for proc in procs:
        proc.join()



if __name__ == "__main__":
    main()