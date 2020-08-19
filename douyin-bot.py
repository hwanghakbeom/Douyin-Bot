# -*- coding: utf-8 -*-
import sys
import random
import time
from PIL import Image
import argparse
import os.path
import pickle
import subprocess
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from ppadb.client import Client as AdbClient
import re

if sys.version_info.major != 3:
    print('Please run under Python3')
    exit(1)
try:
    from common import debug, config, screenshot, UnicodeStreamFilter
    from common.auto_adb import auto_adb
    from common import apiutil
    from common.compression import resize_image, calcPercentage
except Exception as ex:
    print(ex)
    print('Please put the script in the project root directory to run')
    print('Please check in the project root directory common Does the folder exist')
    exit(1)

VERSION = "0.0.1"

# 我申请的 Key，随便用，嘻嘻嘻
# 申请地址 http://ai.qq.com
AppID = '1106858595'
AppKey = 'bNUNgOpY6AeeJjFu'

DEBUG_SWITCH = True
FACE_PATH = 'face/'

adb = auto_adb()
#adb.test_device()
# 审美标准
BEAUTY_THRESHOLD = 80

# 最小年龄
GIRL_MIN_AGE = 14


def yes_or_no():
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    i = 0
    for device in devices:
        print(str(i) + " : " + device.serial)
        i = i + 1
    while True:
        if i == 0: exit(0)
        yes_or_no = str(input('Choose devices 0 to {x1} n for exit:'.format(x1 = i-1) ))
        if yes_or_no == 'n':
           print('Thanks for using')
           exit(0) 
        if 0 <= int(yes_or_no) <= i:
            global device_id
            device_id = devices[int(yes_or_no)].serial
            adb.set_device(device_id)
            size = adb.get_screen()
            m = re.search(r'(\d+)x(\d+)', size)
            
            global config
            print("get device info....")
            config = config.open_accordant_config(device_id)
            if m:
                config['screen_size']['x'] = int(m.group(1))
                config['screen_size']['y'] = int(m.group(2))
            
            break
        else:
            print('please enter again')


def _random_bias(num):
    """
    random bias
    :param num:
    :return:
    """
    return random.randint(-num, num)


def next_page():
    """
    翻到下一页
    :return:
    """
    percentageX= config['screen_size']['x'] / 2
    percentageY= config['screen_size']['y'] /10 * 6

    percentageX1= config['screen_size']['x'] / 2
    percentageY1= config['screen_size']['y'] /6

    cmd = 'shell input swipe {x1} {y1} {x2} {y2} {duration}'.format(
        x1=percentageX,
        y1=percentageY,
        x2=percentageX1,
        y2=percentageY1,
        duration=350
    )
    adb.run(cmd)
    time.sleep(1.5)


def follow_user():
    """
    关注用户
    :return:
    """
    cmd = 'shell input tap {x} {y}'.format(
        x=config['follow_bottom']['x'] + _random_bias(10),
        y=config['follow_bottom']['y'] + _random_bias(10)
    )
    adb.run(cmd)
    time.sleep(0.5)


def thumbs_up():
    """
    点赞
    :return:
    """
    #check white

    percentageX= config['screen_size']['x'] / 100 * 93
    percentageY= config['screen_size']['y'] / 100 * 50

    cmd = 'shell input tap {x} {y}'.format(
        x=percentageX + _random_bias(10),
        y=percentageY + _random_bias(10)
    )
    adb.run(cmd)
    time.sleep(0.5)


def tap(x, y):
    cmd = 'shell input tap {x} {y}'.format(
        x=x + _random_bias(10),
        y=y + _random_bias(10)
    )
    adb.run(cmd)


def auto_reply():

    msg = random.choice(msgList)

    #adb -s 172.30.65.129:5555 shell input keyevent 279
    
    # Click the comment button on the right
    percentageX= config['screen_size']['x'] / 10 * 9
    percentageY= config['screen_size']['y'] / 10 * 6

    tap(percentageX,percentageY)
    time.sleep(2)
    #After the comment list pops up, click the input comment box

    percentageX1= config['screen_size']['x'] / 10 * 5
    percentageY1= config['screen_size']['y'] / 100 * 93
    tap(percentageX1, percentageY1)
    time.sleep(2)
    #Enter the above msg content, pay attention to use ADB keyboard, otherwise it cannot be entered automatically, refer to: https://www.jianshu.com/p/2267adf15595
    #cmd =' shell am broadcast -a ADB_INPUT_TEXT --es msg "你好嗎'
    cmd = 'shell am broadcast -a ADB_INPUT_TEXT --es msg {text}'.format(text=msg)

    #cmd = 'shell input text "{}"'.format(msg)
    #cmd = 'shell input text "{}"'.format('Nice')
    adb.run(cmd)
    time.sleep(2)
    # Click the send button
    cmd = 'shell input keyevent 4'
    adb.run(cmd)
    time.sleep(2)

    cmd = 'shell input keyevent 4'
    adb.run(cmd)
    time.sleep(2)

    print("send msg")
    percentageX2= config['screen_size']['x'] / 100 * 93
    percentageY2= config['screen_size']['y'] / 100 * 94
    tap(percentageX2, percentageY2)
    time.sleep(2)

    print("close popup") #1300, 340
    cmd = 'shell input keyevent 4'
    adb.run(cmd)
    # Trigger the return button, keyevent 4 corresponds to the return key of the Android system, refer to the corresponding button operation of KEY:  https://www.cnblogs.com/chengchengla1990/p/4515108.html
    


def parser():
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--reply", action='store_true',
                    help="auto reply")
    args = vars(ap.parse_args())
    return args


def main():
    """
    maintest_device
    :return:
    """
    


    print('Program version number : {}'.format(VERSION))
    print('Activate the window and press CONTROL + C Key combination to exit')
    # debug.dump_device_info()
    screenshot.check_screenshot(device_id)

    cmd_args = parser()

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SAMPLE_SPREADSHEET_ID = '1RePp_f8FqGBEotcK0TscFo4L5lwPHBypsjzJnJJJLU8'
    SAMPLE_RANGE_NAME = 'Sheet1!A2:A4'

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        global msgList
        msgList = []
        for row in values:
            msgList.append(row[0])

            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s' % (row[0]))

    #msgList = getfrom google spreadsheet


    while True:
        next_page()

        time.sleep(1)
        screenshot.pull_screenshot(device_id)

        resize_image('autojump.png', 'optimized.png', 1024*1024)

        with open('optimized.png', 'rb') as bin_data:
            image_data = bin_data.read()

        ai_obj = apiutil.AiPlat(AppID, AppKey)
        rsp = ai_obj.face_detectface(image_data, 0)

        major_total = 0
        minor_total = 0

        if rsp['ret'] == 0:
            beauty = 0
            for face in rsp['data']['face_list']:

                msg_log = '[INFO] gender: {gender} age: {age} expression: {expression} beauty: {beauty}'.format(
                    gender=face['gender'],
                    age=face['age'],
                    expression=face['expression'],
                    beauty=face['beauty'],
                )
                print(msg_log)
                face_area = (face['x'], face['y'], face['x']+face['width'], face['y']+face['height'])
                img = Image.open("optimized.png")
                cropped_img = img.crop(face_area).convert('RGB')
                cropped_img.save(FACE_PATH + face['face_id'] + '.png')
                # 性别判断
                if face['beauty'] > beauty and face['gender'] < 50:
                    beauty = face['beauty']

                if face['age'] > GIRL_MIN_AGE:
                    major_total += 1
                else:
                    minor_total += 1

            # 是个美人儿~关注点赞走一波
            if beauty > BEAUTY_THRESHOLD and major_total > minor_total:
                print('Found a beautiful girl! ! !')
                start_heart_x = config['screen_size']['x'] * 100 / 90
                start_heart_y = config['screen_size']['y'] * 100 / 50
                heart_area = (start_heart_x, start_heart_y, start_heart_x+10, start_heart_y+10)
                origin_img = Image.open("autojump.png")
                heart_img = origin_img.crop(heart_area)
                ratio = detect_color('red',heart_img)
                thumbs_up()
                follow_user()
                auto_reply()
                #if cmd_args['reply']:

                #    auto_reply()

        else:
            print(rsp)
            continue


if __name__ == '__main__':
    try:
        yes_or_no()
        main()
    except KeyboardInterrupt:
        #adb.run('kill-server')
        print('Thanks for using')
        exit(0)
