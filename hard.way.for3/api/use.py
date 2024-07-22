# -*- coding: utf-8 -*-
from sdk.asr.vad import *

if __name__ == '__main__':
    open_ws = True
    callback_url = "http://192.168.6.102:10101/sdk/vad"
    file_link = "http://192.168.6.55:10000/data/model/1.wav"
    token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJndWFuZ2RvbmciLCJpYXQiOjE2ODE5NzU3MzQsImV4cCI6MjAzMDgwMzIwMH0.wn1FMgemnqj5_jaBZ6nPrKpKGsva-UBUnXbO2-MDgCQ"
    client = VadClient("192.168.6.102", 9997, "/vad/asr")
    client.vad_request(appkey="yue", token=token, file_link=file_link, callback_url=callback_url, open_ws=open_ws
                       ,enable_hot_rule=True,enable_cn_rule=True,enable_inverse_text_normalization=True,
                       enable_db_rule=True,enable_speed_rule=True,enable_semantic_sentence_detection=True
    )