# -*- coding: utf-8 -*-
import websocket
import time
import threading


def getConnection(ws_url, nst, on_open, on_message, on_close, on_error):
    ws = websocket.WebSocketApp(ws_url + nst.taskId,
                                on_open=on_open, on_message=on_message, on_close=on_close, on_error=on_error,
                                header=nst.__dict__)
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()
    conn_timeout = 1
    while not ws.sock.connected and conn_timeout <= 10:
        print(f"连接建立等待: {conn_timeout};")
        time.sleep(1)
        conn_timeout += 1
    if conn_timeout > 10:
        print("尝试10秒连接未成功建立")
    return ws


class NlsSpeechTranscriber(object):
    def __init__(self, appKey, token, taskId):
        self.token = token
        self.appKey = appKey
        self.sampleRate = "8000"
        self.taskId = taskId
        self.enableIntermediateResult = None
        self.resample = None
        self.punctuation = None
        self.hotRule = None
        self.numRule = None
        self.cnRule = None
        self.dbRule = None
        self.speedRule = None

    def setTaskId(self, taskId: str):
        self.taskId = taskId

    def setEnableIntermediateResult(self, enableIntermediateResult: bool):
        self.enableIntermediateResult = "true" if enableIntermediateResult else "false"

    def setResample(self, resample: bool):
        self.resample = "1" if resample else "2"

    def setPunctuation(self, punctuation: bool):
        self.punctuation = "1" if punctuation else "2"

    def setHotRule(self, hotRule: bool):
        self.hotRule = "1" if hotRule else "2"

    def setNumRule(self, numRule: bool):
        self.numRule = "1" if numRule else "2"

    def setCnRule(self, cnRule: bool):
        self.cnRule = "1" if cnRule else "2"

    def setDbRule(self, dbRule: bool):
        self.dbRule = "1" if dbRule else "2"

    def setSpeedRule(self, speedRule: bool):
        self.speedRule = "1" if speedRule else "2"
