# -*- coding: utf-8 -*-
import io
import torch
import torchaudio
from omegaconf import OmegaConf
from utils import get_audio_backend, init_jit_model, vad_split

# 加载预训练模型
device = torch.device('cpu')  # 选择设备，可以是 'cpu' 或 'cuda'
model, utils = init_jit_model(model_path='model.vad', device=device)

# 选择合适的音频后端
backend = get_audio_backend()
torchaudio.set_audio_backend(backend)

# 假设你有一个名为 audio_bytes 的字节流对象
audio_bytes = b'...'  # 用实际的音频字节流替换这里的省略号

# 将字节流转换为音频张量
byte_stream = io.BytesIO(audio_bytes)
waveform, sample_rate = torchaudio.load(byte_stream)
waveform = waveform.to(device)

# 根据需要调整采样率
target_sample_rate = 16000
if sample_rate != target_sample_rate:
    waveform = torchaudio.transforms.Resample(
        orig_freq=sample_rate, new_freq=target_sample_rate
    )(waveform)

# 使用 VAD 进行分割
vad_chunks = vad_split(audio=waveform,
                       model=model,
                       num_steps=4,
                       sample_rate=target_sample_rate,
                       device=device,
                       **OmegaConf.to_container(utils, resolve=True))

# 保存分割后的音频文件
for idx, chunk in enumerate(vad_chunks):
    torchaudio.save(f'output_{idx}.wav', chunk.unsqueeze(0), target_sample_rate)
