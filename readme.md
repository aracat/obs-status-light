This is an AI slop-coded bridge between OBS Studio's congestion indicator and various "I'm Busy/In A Call" status lights.

## Installation

1. Start OBS and install the script
	Tools -> Scripts -> + button -> Select `congestion-writer.lua`

2. Verify %temp%\obs_status.txt exists

3. Install python 3 + requirements
	`python -m pip install -r requirements.txt`

##  Use

1. Start OBS

2. Run `light-controller.py`

If the light doesn't turn white briefly on script startup, you probably need to go adjust
%appdata%\Roaming\Python\{PYTHON VERSION}\site-packages\busylight\lights\light.py
to comment out line 554 and 555 that add a padding byte on Windows.

3. Watch the light

* Breathing green - yellow - red: stream active, color indicates congestion status (red = bad)

* Blinking red: disconnected and attempting to reconnect

* Breathing blue: not streaming

* Blinking blue: status file not updating (OBS crash)

* Blinking magenta: malformed or missing status file, or a python bug

* Off or any continuous color: script not running

## Notes

Color mixing: https://docs.obsproject.com/reference-outputs and https://github.com/obsproject/obs-studio/blob/1be1f51635ac85b3ad768a88b3265b192bd0bf18/UI/window-basic-status-bar.cpp#L327 for the color

Light driver: https://github.com/JnyJny/busylight

Traffic shaping: https://www.reddit.com/r/networking/comments/ttfvg0/simulating_network_latency_bandwidth_and_packet/