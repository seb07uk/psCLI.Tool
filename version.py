import platform
import datetime
__author__ = "Sebastian Januchowski"
__category__ = "system"
__group__ = "core"
__desc__ = "CLI version information"
NAME = "TERMINAL CLI"
VERSION = "3.1.0"
CHANNEL = "stable"
PYTHON_MIN = "3.7"
BUILD_DATE = "2026-01-19"
def info():
    return {
        "name": NAME,
        "version": VERSION,
        "channel": CHANNEL,
        "python_min": PYTHON_MIN,
        "python_runtime": platform.python_version(),
        "build_date": BUILD_DATE,
        "generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
