import os.path
import subprocess
import time
import win32com.client
import hashlib
import pygame
from aip import AipSpeech

client = AipSpeech('15214676', 'ec38ooAnseLccgP1U89iI88l', '04h8Dhm4DdMuztfkWAlWwBzf5dtF8Mc8')


def md5(data):
    return hashlib.md5(data.encode()).hexdigest()


def speak(text: str, file: str = ""):
    """
机器说话(百度)
    :param text:
    :param file:
    """
    if file == "":
        save_file = 'temp/%s.mp3' % md5(text)
    else:
        save_file = file
    n = 0
    while True:
        try:
            rt = client.synthesis(text, options={'per': 0, 'vol': 8,'spd':5})
            break
        except Exception as e:
            n += 1
            if n > 5:
                raise e
    if not os.path.exists('temp'):
        os.mkdir('temp')
    open(save_file, 'wb').write(rt)
    if file == "":
        pygame.mixer.init()
        pygame.mixer.music.load(save_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == 1:
            pygame.time.wait(1)


# def speak(text: str, file: str = ""):
#     """
# 机器说话
#     :param text:
#     :param file:
#     """
#     s = win32com.client.Dispatch('SAPI.SpVoice')
#     if file != "":
#         f = win32com.client.Dispatch('SAPI.SpFileStream')
#         f.Open(file, '3')
#         s.AudioOutputStream = f
#     s.Speak(text)
#     if file != "":
#         f.Close()

def command(cmd, timeout=60):
    """执行命令cmd，返回命令输出的内容。
    如果超时将会抛出TimeoutError异常。
    cmd - 要执行的命令
    timeout - 最长等待时间，单位：秒
    """
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    t_beginning = time.time()
    seconds_passed = 0
    while True:
        if p.poll() is not None:
            break
        seconds_passed = time.time() - t_beginning
        if timeout and seconds_passed > timeout:
            p.terminate()
            return None
        time.sleep(0.1)
    return p.stdout.read().decode(encoding='gbk')


def now_datetime(format: str = '%Y-%m-%d %H:%M:%S'):
    """
    返回当天时间并格式化
    :return:
    """
    return time.strftime(format, time.localtime(time.time()))
