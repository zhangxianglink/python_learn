# -*- coding: utf-8 -*-
import os
import requests
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='download.log', filemode='w')

file_path = "/data/audio/file.txt"
download_dir = "/data/audio/may/"

with open(file_path, "r", encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        download_url = "http://10.188.34.2:21601/cc/atm/tprecord/msa/record/downRecordfile?callid="+line+"&filetype=1"
        filename = os.path.basename(line + ".wav")
        try:
            response = requests.get(download_url, timeout=10)
            response.raise_for_status()
            os.makedirs(download_dir, exist_ok=True)
            with open(os.path.join(download_dir, filename), "wb") as f:
                f.write(response.content)
            logging.info("成功下载文件：" + os.path.join(download_dir, filename))

        except requests.exceptions.RequestException as e:
            logging.error("下载文件失败：" + os.path.join(download_dir, filename))
            logging.error("错误记录：" + str(e))