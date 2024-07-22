# -*- coding: utf-8 -*-
# 打开日志文件进行读取
import http.client
from openpyxl import Workbook

# 创建一个新的Excel工作簿
wb = Workbook()
ws = wb.active

conn = http.client.HTTPConnection("192.168.2.126", 8082)

headers = {
    'Content-Type': 'application/json'
}

with open('D:\\linuxupload\\a.log', 'r', encoding='utf-8') as file:
    line_count = 0  # 初始化行计数器
    for line in file:  # 逐行读取
        if line_count > 60:  # 如果已处理60行，则退出循环
            break
        # 检查是否包含关键字
        if "参数：" in line or "返回结果：" in line:
            keyword = "参数：" if "参数：" in line else "返回结果："
            keyword_index = line.index(keyword)
            # 输出关键字前20个字符
            id = line[max(0, keyword_index - 20):keyword_index]
            # 输出关键字后所有字符
            msg = line[keyword_index + len(keyword):].strip()
            if keyword == "参数：":
                ws.append([id, "参数", msg])
            else:
                ws.append([id, "192.168.2.23", msg])
            if msg.startswith("{\"stream\""):
                conn.request("POST", "/v1/chat/message_question_summary", msg.encode('utf-8'), headers)
                res = conn.getresponse()
                data = res.read()
                decode = data.decode("utf-8")
                print(decode)
                ws.append([id, "192.168.2.126", decode])
        line_count += 1

# 将结果追加写入文件
wb.save('D:\\data\\models\\output.xlsx')
