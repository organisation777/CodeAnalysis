# -*- encoding: utf-8 -*-
"""
job任务的心跳进程
应用场景:
localscan扫描时,如果有进程需要发送到server端公共机器执行,此时启动一个job心跳,告诉server本地客户端进程在线.
避免本地退出,而server无感知,一直等待本地客户端取私有进程任务的死等情况.
"""

import time
import logging
import threading

logger = logging.getLogger(__name__)


class JobHeartBeatThread(threading.Thread):
    """
    任务心跳线程,通过JobHeartBeat管理类调用
    """
    def __init__(self, event, job_id, server):
        threading.Thread.__init__(self)
        self._event = event
        self._job_id = job_id
        self._server = server
        self._sleep_interval = 8  # 每 8 秒上报一次心跳

    def run(self):
        while self._event.is_set():
            time.sleep(self._sleep_interval)
            self._server.job_heart_beat(self._job_id)


class JobHeartBeat(object):
    """
    任务心跳管理类
    """
    def __init__(self, job_id, dog_server):
        """
        初始化
        :param job_id:
        :param dog_server:
        :return:
        """
        self._job_id = job_id
        self._dog_server = dog_server
        self._event = threading.Event()  # 通过event事件控制心跳线程退出
        self._event = threading.Event()

    def start(self):
        """
        启动心跳线程
        :return:
        """
        self._event.set()
        JobHeartBeatThread(self._event, self._job_id, self._dog_server).start()

    def stop(self):
        """
        停止心跳线程
        :return:
        """
        # 清除线程信号标记,心跳线程即可退出
        self._event.clear()
