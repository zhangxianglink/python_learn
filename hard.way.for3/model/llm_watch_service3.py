from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
import signal
import time

app = FastAPI()


def kill_process_by_index(index, port):
    key = f"nvidia-smi -i {index} --query-compute-apps=gpu_serial,pid,process_name --format=csv,noheader"
    print(f'key: {key}')
    result = subprocess.run(key, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        stdout = result.stdout
        print(f'stdout: {stdout}')
        output3 = stdout.strip().split('\n')
        for app in output3:
            gpu_serial, pid, process_name = app.split(', ')
            os.kill(int(pid), signal.SIGKILL)
            print(f"Killed process on port: {port} with PID: {pid} with gpu_serial: {gpu_serial} with process_name: {process_name}")


# 8083 （0，1 显卡） 8084 （2，3 显卡）
def kill_process_on_port(port):
    if port == 8083:
        kill_process_by_index(0, port)
        kill_process_by_index(1, port)
    elif port == 8084:
        kill_process_by_index(2, port)
        kill_process_by_index(3, port)
    else:
        print(f"don't support PORT: {port}")


def run_script(port, model):
    activate_cmd = "source /root/miniconda3/etc/profile.d/conda.sh && conda activate /data/app/vllm0.5_py310"
    subprocess.call(activate_cmd, shell=True, executable="/bin/bash")
    if port == 8083:
        if model == 'qc':
            script = 'api_setup8083.sh'
        else:
            script = 'api_setup_half1_8083.sh'
        log_file = "/data/app/nvs/api8083.log"
        script_path = f"/data/app/audio_assessment_llm_deployment_new/scripts/{script}"
    elif port == 8084:
        if model == 'qc':
            script = 'api_setup8084.sh'
        else:
            script = 'api_setup_half2_8084.sh'
        log_file = "/data/app/nvs/api8084.log"
        script_path = f"/data/app/audio_assessment_llm_deployment_new/scripts/{script}"
    else:
        print(f"don't support PORT: {port}")
        return
    try:
        subprocess.call(
            f"nohup /bin/bash {script_path} > {log_file} 2>&1 &",
            shell=True, executable="/bin/bash"
        )
        print(f"Ran script {script_path} with nohup, logging to {log_file}")
    except Exception as e:
        print(f"Error running script {script_path}: {e}")


class ScriptRequest(BaseModel):
    port: int
    type: str
    model: str


@app.post("/run_script")
async def run_script_endpoint(request: ScriptRequest):
    rule = request.type
    model = request.model
    if rule not in ['start', 'stop', 'restart']:
        raise HTTPException(status_code=400, detail="Invalid rule. Please provide start/stop/restart")

    if model not in ['qc', 'profile'] and rule in ['start', 'restart']:
        raise HTTPException(status_code=400, detail="Invalid model. Please provide qc/profile")

    if rule == 'stop':
        kill_process_on_port(request.port)
        return {"message": f"kill port {request.port}"}

    if rule == 'start':
        run_script(request.port, model)
        return {"message": f" executed successfully on port {request.port}"}

    if rule == 'restart':
        kill_process_on_port(request.port)
        time.sleep(3)
        run_script(request.port, model)
        return {"message": f" executed successfully on port {request.port}"}


@app.get("/status")
async def nv_status():
    updated_gpu_info = []
    # 生成 app_info 列表，确保 pid 的唯一性
    app_info = []
    # 列出当前激活的计算进程。
    command_v1 = "nvidia-smi --query-compute-apps=gpu_serial,pid,process_name --format=csv,noheader"
    result3 = subprocess.run(command_v1, shell=True, capture_output=True, text=True)
    if result3.returncode == 0:
        print(f"command_v1: {result3.stdout}")
        output3 = result3.stdout.strip().split('\n')
        # 用于存储唯一 pid 的集合
        unique_pids = set()
        unique_gpu = set()
        for app in output3:
            gpu_serial, pid, process_name = app.split(', ')
            if pid not in unique_pids and gpu_serial not in unique_gpu:
                unique_pids.add(pid)
                unique_gpu.add(gpu_serial)
                app_info.append({
                    'gpu_serial': gpu_serial,
                    'pid': pid,
                    'process_name': process_name
                })

        # 根据pid获取port
        for info in app_info:
            if 'pid' in info:
                try:
                    command_v2 = f"netstat -tulnp | grep {info['pid']} | awk '{{print $4}}' | awk -F ':' '{{print $2}}'"
                    result1 = subprocess.run(command_v2, shell=True, capture_output=True, text=True, check=True)
                    info['port'] = result1.stdout.strip().replace('\n', ',')  # 去除字符串前后的空格和换行符
                    print(f"command_v2: {result1.stdout}")
                except subprocess.CalledProcessError as e:
                    print(f"根据pid获取port. command_v2 执行异常: {e.stderr}")
    else:
        print(f"当前激活的计算进程。 command_v1 执行异常: {result3.stderr} ")

    # 名称，显存信息，gpu使用率
    command_v3 = "nvidia-smi --query-gpu=index,gpu_serial,name,memory.total,memory.free,memory.used,utilization.gpu,utilization.memory --format=csv,noheader"
    result2 = subprocess.run(command_v3, shell=True, capture_output=True, text=True)
    if result2.returncode == 0:
        print(f"command_v3: {result2.stdout}")
        output = result2.stdout.strip().split('\n')
        gpu_info = [
            dict(zip(['index', 'gpu_serial', 'name', 'memory_total', 'memory_free', 'memory_used', 'utilization_gpu',
                      'utilization_memory'],
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
