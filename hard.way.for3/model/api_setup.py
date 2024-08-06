import os
import setproctitle
import uvicorn


from llamafactory.api_audio_assessment import create_app
from llamafactory.chat import ChatModel


def main():
    # 读取a.txt文件并输出内容
    with open("/data/app/nvs/port.txt", "r") as file:
        content = file.read()
        api_port = int(content)
    setproctitle.setproctitle("llm_completion_api")
    chat_model = ChatModel()
    app = create_app(chat_model)
    api_host = os.environ.get("API_HOST", "0.0.0.0")
    print(f"Visit http://{api_host}:{api_port}/docs for API document.")
    uvicorn.run(app, host=api_host, port=api_port, workers=1)


if __name__ == "__main__":
    main()
