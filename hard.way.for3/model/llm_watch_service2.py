from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
import signal

app = FastAPI()


def kill_process_on_port(port):
    try:
        pid = subprocess.check_output(
            f"lsof -t -i:{port}", shell=True, text=True).strip()
        print(f"port: {port} pid: {pid}")
        if pid:
            os.kill(int(pid), signal.SIGKILL)
            print(f"Killed process on port {port} with PID {pid}")
    except subprocess.CalledProcessError:
        print(f"No process found on port {port}")
    except Exception as e:
        print(f"Error killing process on port {port}: {e}")


def run_script(port):
    activate_cmd = "source /root/miniconda3/etc/profile.d/conda.sh && conda activate /data/app/glm4"
    subprocess.call(activate_cmd, shell=True, executable="/bin/bash")
    script = ""
    # 写入8081到a.txt文件
    with open("/data/app/nvs/port.txt", "w") as file:
        file.write(str(port))
    try:
        script2 = """
        nohup bash -c 'export  CUDA_VISIBLE_DEVICES=2,3; python /data/app/audio_assessment_llm_deployment-new/src/api_setup.py \
            --flash_attn fa2 \
            --template qwen \
            --model_name_or_path /data/models/Qwen2-7B-Instruct \
            --finetuning_type lora \
            > /data/app/nvs/run8082.log 2>&1' &
        """

        script1 = """
        nohup bash -c 'export  CUDA_VISIBLE_DEVICES=0,1; python /data/app/audio_assessment_llm_deployment-new/src/api_setup.py \
            --flash_attn fa2 \
            --template qwen \
            --model_name_or_path /data/models/Qwen2-7B-Instruct \
            --finetuning_type lora \
            > /data/app/nvs/run8083.log 2>&1' &
        """

        if port == 8082:
            script = script2
        else:
            script = script1
        process = subprocess.Popen(script, shell=True, executable="/bin/bash")
        process.wait()
        print("Script executed. Check /data/app/run.log for details.")

    except Exception as e:
        print(f"Error running script {script}: {e}")


class ScriptRequest(BaseModel):
    port: int
    type: str


@app.post("/run_script")
async def run_script_endpoint(request: ScriptRequest):

    type = request.type

    if type not in ['start', 'stop', 'restart']:
        raise HTTPException(status_code=400, detail="Invalid type. Please provide start/stop/restart")

    if type == 'stop':
        kill_process_on_port(request.port)
        return {"message": f"kill port {request.port}"}

    if type == 'start':
        run_script(request.port)
        return {"message": f" executed successfully on port {request.port}"}

    if type == 'restart':
        kill_process_on_port(request.port)
        run_script(request.port)
        return {"message": f" executed successfully on port {request.port}"}


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
            if 'pid' in info:
                try:
                    command_v2 = f"netstat -tulnp | grep {info['pid']} | awk '{{print $4}}' | awk -F ':' '{{print $2}}'"
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
        gpu_info = [dict(zip(['gpu_serial', 'name', 'memory_total', 'memory_free', 'memory_used', 'utilization_gpu',
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
