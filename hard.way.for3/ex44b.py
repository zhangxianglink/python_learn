# -*- coding: utf-8 -*-
import os
import subprocess

# 获取当前目录下audio文件夹中的所有音频文件
audio_folder = 'D:\\app\\bili\\audio_db'
audio_files = os.listdir(audio_folder)

# 创建convert16文件夹
# 创建convert文件夹
convert_folder = 'D:\\app\\bili\\audio_16k'
os.makedirs(convert_folder, exist_ok=True)

count = 0

# 遍历音频文件并进行转换
for audio_file in audio_files:
    input_path = os.path.join(audio_folder, audio_file)
    output_file = os.path.splitext(audio_file)[0] + '_16k.wav'
    output_path = os.path.join(convert_folder, output_file)

    # 调用ffmpeg命令进行音频转换
    subprocess.run(['ffmpeg', '-i', input_path, '-ar', '16000', output_path])
    # 计数器加1
    count += 1
    # 打印已执行次数
    print(f'已执行次数：{count}')


print('音频转换完成')




