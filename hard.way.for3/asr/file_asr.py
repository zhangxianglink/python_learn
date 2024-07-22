# -*- coding: utf-8 -*-
from asr.sdk.vad import vad_request

if __name__ == '__main__':
    open_ws = True
    callback_url = "http://192.168.6.102:10101/sdk/vad"
    file_link = "http://192.168.6.55:10000/data/model/2024-02-20-17-32-40_30300013023096150_18500194588.mp3"
    token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJndWFuZ2RvbmciLCJpYXQiOjE2ODE5NzU3MzQsImV4cCI6MjAzMDgwMzIwMH0.wn1FMgemnqj5_jaBZ6nPrKpKGsva-UBUnXbO2-MDgCQ"
    vad_request(appkey="default", token=token, file_link=file_link, callback_url=callback_url, open_ws=open_ws)
