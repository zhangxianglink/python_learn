import http.client
# 查看asr运行状态
ipList = [
          "192.168.1.98",
          "192.168.1.78",
          "192.168.1.68",
          "192.168.1.62",
          "192.168.1.18",
          "192.168.1.85",
          "192.168.1.64",
          "192.168.1.16",
          "192.168.2.14",
          "192.168.2.15",
    
          "192.168.2.100",
          "192.168.2.116",
          "192.168.1.44",
          "192.168.2.87",

          "192.168.1.20",
          "192.168.1.26",
          "192.168.1.50",
          "192.168.1.55",
          "192.168.2.13",
          "192.168.2.77",
          "192.168.2.27",
          "192.168.2.65",
          "192.168.2.92"]


def rtf3(ip: str):
    conn = http.client.HTTPConnection(ip, 9997)
    conn.request("GET", "/vad/listen")
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


def clean3(ip: str):
    conn = http.client.HTTPConnection(ip, 9997)
    conn.request("POST", "/vad/retry/clean")
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


if __name__ == '__main__':
    for item in ipList:
        print(item + " - " + rtf3(item))
