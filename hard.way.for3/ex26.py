import subprocess
import json

updated_gpu_info = []
app_info = []
# 列出当前激活的计算进程。
command_v1 = "nvidia-smi --query-compute-apps=gpu_serial,pid,process_name --format=csv,noheader"
result3 = subprocess.run(command_v1, shell=True, capture_output=True, text=True)
if result3.returncode == 0:
    print(f"command_v1: {result3.stdout}")
    output3 = result3.stdout.strip().split('\n')
    app_info = [dict(zip(['gpu_serial', 'pid', 'process_name'], app.split(', '))) for app in output3]
    # 根据pid获取port
    for info in app_info:
        command_v2 = f"netstat -tulnp | grep {info['pid']} | awk '{{print $4}}' | awk -F ':' '{{print $2}}'"
        try:
            result1 = subprocess.run(command_v2, shell=True, capture_output=True, text=True, check=True)
            info['port'] = result1.stdout.strip()  # 去除字符串前后的空格和换行符
            print(f"command_v2: {result1.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"根据pid获取port. command_v2 执行异常: {e.stderr}")
else:
    print(f"当前激活的计算进程。 command_v1 执行异常: {result3.stderr} ")

# 名称，显存信息，gpu使用率
command_v3 = "nvidia-smi --query-gpu=gpu_serial,name,memory.total,memory.free,memory.used,utilization.gpu --format=csv,noheader"
result2 = subprocess.run(command_v3, shell=True, capture_output=True, text=True)
if result2.returncode == 0:
    print(f"command_v3: {result2.stdout}")
    output = result2.stdout.strip().split('\n')
    gpu_info = [dict(zip(['gpu_serial', 'name', 'memory_total', 'memory_free', 'memory_used', 'utilization_gpu'],
                         gpu.split(', '))) for gpu in output]
    gpu_dict = {gpu['gpu_serial']: gpu for gpu in gpu_info}
    for app in app_info:
        if app['gpu_serial'] in gpu_dict:
            gpu_dict[app['gpu_serial']].update(app)
    updated_gpu_info = list(gpu_dict.values())
else:
    print(f"名称，显存信息，gpu使用率 command_v3 执行异常: {result2.stderr} ")
print(json.dumps(updated_gpu_info))
