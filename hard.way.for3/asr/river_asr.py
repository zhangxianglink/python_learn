# -*- coding: utf-8 -*-
import wave

from asr.sdk.nls import *


# 消息发送
def on_message(ws, message):
    print(message)


# 异常
def on_error(ws, error):
    print(error)


# 结束
def on_close(ws, close_status_code, close_msg):
    print("### closed ###", close_status_code, close_msg)


# 连接
def on_open(ws):
    print("开始连接")


if __name__ == '__main__':
    nst = NlsSpeechTranscriber("appKey",
                               "eyJhbGciOiJIUzI1NiJ9"
                               ".eyJzdWIiOiJndWFuZ2RvbmciLCJpYXQiOjE2ODE5NzU3MzQsImV4cCI6MjAzMDgwMzIwMH0"
                               ".wn1FMgemnqj5_jaBZ6nPrKpKGsva-UBUnXbO2-MDgCQ", "taskId")
    nst.setEnableIntermediateResult(True)
    ws = getConnection("ws://192.168.6.102:9997/asr/", nst,
                       on_open=on_open,
                       on_message=on_message,
                       on_close=on_close,
                       on_error=on_error)

    print("模拟实时发送数据-------------------")
    with wave.open("D:\\data\\8kt\\20088.wav", "rb") as wav_file:
        num_frames = wav_file.getnframes()
        # Read audio data
        audio_data = wav_file.readframes(num_frames)
        # Convert audio data to bytes
        result = bytearray(audio_data)
        chunk_size = 4096
        for i in range(0, len(result), chunk_size):
            chunk = result[i:i + chunk_size]
            ws.send(chunk, opcode=websocket.ABNF.OPCODE_BINARY)
            time.sleep(0.03)
    # 等待上游断开
    while ws.sock and ws.sock.connected:
        time.sleep(1)
