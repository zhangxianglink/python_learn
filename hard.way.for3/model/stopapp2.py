from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
import signal
import json

app = FastAPI()


class ScriptRequest(BaseModel):
    choice: int
    port: int


def activate_conda_env(env_name):
    """激活指定的conda虚拟环境"""
    activate_command = f"source activate {env_name} && echo 'Conda environment activated'"
    subprocess.call(activate_command, shell=True, executable="/bin/bash")


def kill_process_on_port(port):
    """杀掉指定端口的进程"""
    try:
        pid = subprocess.check_output(
            f"lsof -t -i:{port}", shell=True, text=True).strip()
        if pid:
            os.kill(int(pid), signal.SIGKILL)
            print(f"Killed process on port {port} with PID {pid}")
    except subprocess.CalledProcessError:
        print(f"No process found on port {port}")
    except Exception as e:
        print(f"Error killing process on port {port}: {e}")


def run_script(script_name):
    """使用nohup和后台运行指定的脚本，并将日志输出到指定文件"""
    log_file = "/data/app/audio_assessment_llm_deployment-new/api.log"
    script_path = os.path.join("scripts", script_name)
    try:
        subprocess.call(
            f"nohup /bin/bash {script_path} > {log_file} 2>&1 &",
            shell=True, executable="/bin/bash"
        )
        print(f"Ran script {script_path} with nohup, logging to {log_file}")
    except Exception as e:
        print(f"Error running script {script_path}: {e}")


@app.post("/run_script")
async def run_script_endpoint(request: ScriptRequest):
    if request.choice not in [0, 1]:
        raise HTTPException(status_code=400, detail="Invalid choice. Please provide 0 or 1.")

    # 激活虚拟环境
    activate_conda_env("/data/app/glm4")

    # 杀掉指定端口的进程
    kill_process_on_port(request.port)

    # 选择并运行相应的脚本
    script_name = "api_setup.sh" if request.choice == 0 else "api_setup1.sh"
    run_script(script_name)

    return {"message": f"Script {script_name} executed successfully on port {request.port}"}

@app.get("/status")
async def nv_status():
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
    command_v3 = "nvidia-smi --query-gpu=gpu_serial,name,memory.total,memory.free,memory.used,utilization.gpu,utilization.memory --format=csv,noheader"
    result2 = subprocess.run(command_v3, shell=True, capture_output=True, text=True)
    if result2.returncode == 0:
        print(f"command_v3: {result2.stdout}")
        output = result2.stdout.strip().split('\n')
        gpu_info = [dict(zip(['gpu_serial', 'name', 'memory_total', 'memory_free', 'memory_used', 'utilization_gpu', 'utilization_memory'],
                             gpu.split(', '))) for gpu in output]
        gpu_dict = {gpu['gpu_serial']: gpu for gpu in gpu_info}
        for app in app_info:
            if app['gpu_serial'] in gpu_dict:
                gpu_dict[app['gpu_serial']].update(app)
        updated_gpu_info = list(gpu_dict.values())
    else:
        print(f"名称，显存信息，gpu使用率 command_v3 执行异常: {result2.stderr} ")
    return updated_gpu_info

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8009)
