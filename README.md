# MicroPython Generic Display App
An application which displays text on various devices.
The MicroPython code is located in [the `mpy` directory](/mpy).

## Usage
1. Copy the MicroPython code to your device.
1. Edit the `DEVICE_TYPE` in `config.json` to match your device.
1. Optionally set `WIFI_NETWORK` and `WIFI_PASSWORD` in `config.json`.

It is really important to set the correct device type.
If you forget and your device starts to behave weirdly, you may need to flash the [Pico Universal Flash Nuke](https://github.com/Gadgetoid/pico-universal-flash-nuke) and then re-flash the relevant firmware.

## Configuration

The following configuration items can be set in `config.json`, and are optional unless otherwise noted:
- `DEVICE_TYPE` (mandatory): the type of device that this code is running on, see below for more details.
- `EINK_REFRESH_INTERVAL`: the frequency with which to do a "full" (as opposed to a "fast") refresh on eInk displays that support variable update speed. Defaults to `60`.
- `EINK_UPDATE_SPEED`: the speed for regular ("fast") refreshes on eInk displays that support variable update speed. Defaults to `2`. See [Pimoroni's GitHub](https://github.com/pimoroni/badger2040/blob/f2b3dbc61e8c92376217c06045ec11a8aff1df8c/docs/reference.md#update-speed) for more details.
- `LOG_LIMIT`: the number of log entries to store.
- `NTP_HOST`: the host of the NTP server to use to sync the internal clock. Defaults to `time.cloudflare.com` ([Cloudflare Time Services](https://www.cloudflare.com/time/)).
- `NTP_INTERVAL_HOURS`: the frequency (in hours) to sync the internal clock with the NTP server. Defaults to `4`.
- `WIFI_DEBUG_SHOW_HOSTNAME`: show the device hostname when connecting to WiFi. Defaults to `false`.
- `WIFI_DEBUG_SHOW_IP`: show the device IP address after connecting to WiFi. Defaults to `false`.
- `WIFI_DEBUG_SHOW_MAC`: show the device MAC address when connecting to WiFi. Defaults to `false`.
- `WIFI_DEBUG_SHOW_SSID`: show the WiFi SSID when connecting. Defaults to `true`.
- `WIFI_DEBUG_SUCCESS_SECS`: show the WiFi success message for a certain number of seconds. Defaults to `3`.
- `WIFI_NETWORK`: the WiFi network name (SSID) to connect to.
- `WIFI_PASSWORD`: the password (PSK) for the WiFi network.

## Supported Devices
For full details on supported devices see [`mpy/devices.py`](/mpy/devices.py).
- [Pimoroni Badger 2040 W](https://shop.pimoroni.com/products/badger-2040-w): `badger_2040`
- [Pimoroni Inky Frame 4](https://shop.pimoroni.com/products/inky-frame-4): `inky_frame_4`
- [Pimoroni Inky Pack](https://shop.pimoroni.com/products/pico-inky-pack): `inky_pack`
- [Pimoroni Presto](https://shop.pimoroni.com/products/presto): `presto`

## Application Structure
- `main.py`: runs when the device is booted, initialises `App` class.
- `devices.py`: contains details about supported devices.
- `app.py`: contains the logic required to display application data on the device, including state required for outputting to a display.
- `hello.py`: our example "Hello" application, which contains its own state.
