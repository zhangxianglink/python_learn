# -*- coding: utf-8 -*-
import http.client
import json
import traceback


def vad_request(appkey: str,
                token: str,
                file_link: str,
                callback_url: str,
                open_ws: bool,
                task_id=None,
                enable_semantic_sentence_detection: bool = False,
                enable_inverse_text_normalization: bool = False,
                enable_hot_rule: bool = False,
                enable_cn_rule: bool = False,
                enable_db_rule: bool = False,
                enable_speed_rule: bool = False,
                enable_default_noise_pass=None,
                enable_default_noise_command=None,
                enable_default_noise_preemphasis=None,
                enable_default_noise_equalizer=None,
                enable_default_noise_speed=None,
                enable_right_noise_pass=None,
                enable_right_noise_command=None,
                enable_right_noise_preemphasis=None,
                enable_right_noise_equalizer=None,
                enable_right_noise_speed=None
                ):
    # 构建请求体
    payload = json.dumps({
        "appkey": appkey,
        "token": token,
        "file_link": file_link,
        "callback_url": callback_url,
        "open_ws": open_ws,
        "task_id": task_id,
        "enable_semantic_sentence_detection": enable_semantic_sentence_detection,
        "enable_inverse_text_normalization": enable_inverse_text_normalization,
        "enable_hot_rule": enable_hot_rule,
        "enable_cn_rule": enable_cn_rule,
        "enable_db_rule": enable_db_rule,
        "enable_speed_rule": enable_speed_rule,
        "enable_callback": True,
        "max_single_segment_time": 500,
        "noise_type": 3,
        "enable_kafka_rule": False,
        # 音频处理
        "enable_default_noise_pass": enable_default_noise_pass,
        "enable_default_noise_command": enable_default_noise_command,
        "enable_default_noise_preemphasis": enable_default_noise_preemphasis,
        "enable_default_noise_equalizer": enable_default_noise_equalizer,
        "enable_default_noise_speed": enable_default_noise_speed,
        "enable_right_noise_pass": enable_right_noise_pass,
        "enable_right_noise_command": enable_right_noise_command,
        "enable_right_noise_preemphasis": enable_right_noise_preemphasis,
        "enable_right_noise_equalizer": enable_right_noise_equalizer,
        "enable_right_noise_speed": enable_right_noise_speed
    })

    # 构建请求头
    headers = {
        'Content-Type': 'application/json'
    }

    # 发送请求
    # 发送请求
    try:
        conn = http.client.HTTPConnection("192.168.6.102", 9997)
        conn.request("POST", "/vad/asr", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
    except Exception as e:
        print(f"请求异常：{str(e)}\n{traceback.format_exc()}")
    finally:
        conn.close()
