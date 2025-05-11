# MicroPython Generic Display App
An application which displays text on various devices.
The MicroPython code is located in [the `mpy` directory](/mpy).

## Usage
1. Copy the MicroPython code to your device.
1. Edit the `DEVICE_TYPE` in `config.json` to match your device.

It is really important to set the correct device type.
If you forget and your device starts to behave weirdly, you may need to flash the [Pico Universal Flash Nuke](https://github.com/Gadgetoid/pico-universal-flash-nuke) and then re-flash the relevant firmware.

## Supported Devices
For full details on supported devices see [`mpy/devices.py`](/mpy/devices.py).
- [Pimoroni Inky Frame 4](https://shop.pimoroni.com/products/inky-frame-4): `inky_frame_4`
- [Pimoroni Inky Pack](https://shop.pimoroni.com/products/pico-inky-pack): `inky_pack`
- [Pimoroni Presto](https://shop.pimoroni.com/products/presto): `presto`

## Application Structure
- `main.py`: runs when the device is booted, initialises `App` class.
- `devices.py`: contains details about supported devices.
- `app.py`: contains the logic required to display application data on the device, including state required for outputting to a display.
- `hello.py`: our example "Hello" application, which contains its own state.
