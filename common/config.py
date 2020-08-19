# -*- coding: utf-8 -*-
"""
调取配置文件和屏幕分辨率的代码
"""
import os
import sys
import json
import re

from common.auto_adb import auto_adb


def open_accordant_config(device):
    """
    Call configuration file
    """
    screen_size = _get_screen_size(device)
    config_file = "{path}/config/{screen_size}/config.json".format(
        path=sys.path[0],
        screen_size=screen_size
    )

    # Get the configuration file of the executable file directory first
    here = sys.path[0]
    for file in os.listdir(here):
        if re.match(r'(.+)\.json', file):
            file_name = os.path.join(here, file)
            with open(file_name, 'r') as f:
                print("Load config file from {}".format(file_name))
                return json.load(f)

    # Find profile based on resolution
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            print("From {} Load configuration file".format(config_file))
            return json.load(f)
    else:
        with open('{}/config/default.json'.format(sys.path[0]), 'r') as f:
            print("Load default config")
            return json.load(f)


def _get_screen_size(device):

    adb = auto_adb()
    adb.set_device(device)
    size_str = adb.get_screen()
    m = re.search(r'(\d+)x(\d+)', size_str)
    if m:
        return "{height}x{width}".format(height=m.group(2), width=m.group(1))
    return "1920x1080"
