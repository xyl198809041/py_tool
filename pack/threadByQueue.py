import threading, time


class threadByQueue:

    def __init__(self, max: int, target, args_fun=None, args: list = list()):
        self.max = max
        self.thread_list = []
        for i in range(max):
            self.thread_list.append(threading.Thread())
        self.target = target
        self.args_fun = args_fun
        self._args = args
        self.running = True

    def __running_fun__(self):
        if len(self.args) > 0:
            self.target(self.args.pop())
        elif self.args_fun is not None:
            self.target(self.args_fun())
        else:
            return
        #print(threading.currentThread().name + '完成')

    @property
    def args(self):
        return self._args

    def start(self):
        self.running = True
        threading.Thread(target=self.__run__).start()
        print('开始运行')

    def stop(self):
        self.running = False

    def __run__(self):
        while self.running:
            for i in range(self.max):
                if not self.thread_list[i].isAlive():
                    self.thread_list[i] = threading.Thread(target=self.__running_fun__, name=i + 1)
                    self.thread_list[i].start()
            time.sleep(1)
        print('结束运行')
