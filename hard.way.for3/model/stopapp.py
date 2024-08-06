from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
import signal

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)
