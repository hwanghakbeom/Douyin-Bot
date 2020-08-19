# -*- coding: utf-8 -*-
import os
import subprocess
import platform
import re

class auto_adb():
    def __init__(self):
        try:
            adb_path = 'adb'
            subprocess.Popen([adb_path], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
            self.adb_path = adb_path
        except OSError:
            if platform.system() == 'Windows':
                adb_path = os.path.join('Tools', "adb", 'adb.exe')
                try:
                    subprocess.Popen(
                        [adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.adb_path = adb_path
                except OSError:
                    pass
            else:
                try:
                    subprocess.Popen(
                        [adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                except OSError:
                    pass
            print('Please Install ADB And drive and configure environment variables')
            exit(1)

    def set_device(self, device):
        self.adb_path = self.adb_path + ' -s ' + device

    def get_screen(self):
        try:
            process = os.popen(self.adb_path + ' shell wm size')
            output = process.read()
            return output
        except:
            print('error return default')
            return '1920x1080'

    def run(self, raw_command):
        print(raw_command)
        command = '{} {}'.format(self.adb_path, raw_command)
        process = os.popen(command)
        output = process.read()
        return output

    def test_device(self):
        print('Check if the device is connected...')
        command_list = [self.adb_path, 'devices']
        print(command_list)
        process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()
        if output[0].decode('utf8') == 'List of devices attached\n\n':
            print('Device not Found')
            print('adb Output:')
            for each in output:
                print(each.decode('utf8'))
            exit(1)
        print('Device connected')
        print('adb Output:')
        for each in output:
            print(each.decode('utf8'))

    # def test_density(self):
    #     process = os.popen(self.     + ' shell wm density')
    #     output = process.read()
    #     return output

    # def test_device_detail(self):
    #     process = os.popen(self.adb_path + ' shell getprop ro.product.device')
    #     output = process.read()
    #     return output

    # def test_device_os(self):
    #     process = os.popen(self.adb_path + ' shell getprop ro.build.version.release')
    #     output = process.read()
    #     return output

    def adb_path(self):
        return self.adb_path
