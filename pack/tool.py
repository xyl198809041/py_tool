import subprocess
import time
import win32com.client


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


def speak(text: str, file: str = ""):
    """
机器说话
    :param text:
    :param file:
    """
    s = win32com.client.Dispatch('SAPI.SpVoice')
    if file != "":
        f = win32com.client.Dispatch('SAPI.SpFileStream')
        f.Open(file, '3')
        s.AudioOutputStream = f
    s.Speak(text)
    if file != "":
        f.Close()
