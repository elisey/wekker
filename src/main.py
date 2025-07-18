import time
import signal
import sys

from hal import BinaryInput, AnalogInput, get_hal, WekkerHardwareAbstract
from music import get_player
from music.player import Player
from music.radio import Radio

hw: WekkerHardwareAbstract | None = None
file_player: Player = get_player("file")
radio_player: Radio = get_player("url")


def signal_handler(signum, frame):
    print("Signal received, cleaning up GPIO...")
    hw.close()
    radio_player.stop()
    file_player.stop()
    sys.exit(0)

def some(binary_input, state):
    print(f"Callback called for input={binary_input.name}, state={state} ")
    if state:
        file_player.stop()
        radio_player.stop()
        return

    if binary_input == BinaryInput.ALARM:
        file = "/home/wekker/surok.mp3"
        file_player.play(file)
    elif binary_input == BinaryInput.RADIO or binary_input == BinaryInput.BAND:
        result = radio_player.play()
        if not result:
            file = "/home/wekker/krik.mp3"
            file_player.play(file)

    else:
        assert False

def on_tune_change(input, value):
    radio_player.change()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
    global hw
    hw = get_hal("gpiozero")

    global player
    player = Player()

    hw.register_binary_input_change_handler(BinaryInput.ALARM, some)
    hw.register_binary_input_change_handler(BinaryInput.RADIO, some)
    hw.register_binary_input_change_handler(BinaryInput.BAND, some)
    hw.register_analog_input_change_handler(AnalogInput.TUNE, on_tune_change)

    print(hw.get_input_state(BinaryInput.ALARM))  # True
    # print(hw.get_analog_state(AnalogInput.VOLUME))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    print_hi('PyCharm')
    while(True):
        time.sleep(1)
        #print(".", end="")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
