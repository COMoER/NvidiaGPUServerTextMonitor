#   Copyright 2023 COMoER
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import os
import paramiko  # SSH package
import subprocess
import yaml
THISDIR = os.path.abspath(os.path.dirname(__file__))
if 'SAVE_FILE' in os.environ.keys():
    SAVE_FILE = os.environ["SAVE_FILE"]
else:
    SAVE_FILE = os.path.join(THISDIR,'gpu_query.txt')

if 'CFG_FILE' in os.environ.keys():
    CFG_FILE = os.path.join(THISDIR,os.environ["CFG_FILE"])
else:
    CFG_FILE = os.path.join(THISDIR,'ssh_gpu_cfg.yaml')


# def yaml_read():


def query_gpu(server_info):
    try:
        ssh = paramiko.SSHClient()

        know_host = paramiko.AutoAddPolicy()
        ssh.set_missing_host_key_policy(know_host)
        ssh.connect(server_info[0], server_info[1], username=server_info[2], password=server_info[3],timeout=1)

        ssh_stdin, ssh_nvidia_smi, ssh_stderr = ssh.exec_command(f"nvidia-smi --query-gpu=index,name,memory.used,memory.total --format=csv,noheader")
        # now available one gpu lost
        ssh_info = ssh_nvidia_smi.read().decode()
        if "MiB" in ssh_info:
            # valid
            one_gpu_info_whole = [_.split(',') for _ in ssh_info.split('\n') if len(_) > 0]
            one_gpu_info = [[ogi[0],ogi[2],ogi[3]] for ogi in one_gpu_info_whole]
            gpu_name = [ogi[1] for ogi in one_gpu_info_whole]
            one_gpu_info = [[int(h_.replace(' ','').replace('MiB','')) for h_ in _] for _ in one_gpu_info]
            out_info = '\n'.join([f"GPU{_[0]}[{h_[1:]}]: {_[1]:d}MiB/{_[2]:d}MiB" for _,h_ in zip(one_gpu_info,gpu_name)])
        else:
            out_info = "[ERROR] Invalid Info! Check Server Stage!"

        # print(out_info)
        # print('Connected to SSH share')
    except Exception as e:
        print('Something went wrong with the SSH connection')
        out_info = "[ERROR] Invalid Info! Check Server State!"

    ssh.close()
    return out_info

def query_noleaf_gpu(server_info):
    try:
        ssh = paramiko.SSHClient()

        know_host = paramiko.AutoAddPolicy()
        ssh.set_missing_host_key_policy(know_host)
        ssh.connect(server_info[0], server_info[1], username=server_info[2], password=server_info[3],timeout=1)

        ssh_stdin, ssh_nvidia_smi, ssh_stderr = ssh.exec_command("cat /data0/dataset/gpu_query")
        # now available one gpu lost
        out_info = '######################\n'+ssh_nvidia_smi.read().decode()+'######################'
        # print(out_info)
        # print('Connected to SSH share')
    except Exception as e:
        print('Something went wrong with the SSH connection')
        out_info = "[ERROR] Invalid Info! Check Server State!"

    ssh.close()
    return out_info

def query_gpu_self():
    try:
        result = subprocess.check_output(f"nvidia-smi --query-gpu=index,name,memory.used,memory.total --format=csv,noheader", shell=True)
        # ssh_stdin, ssh_nvidia_smi, ssh_stderr = exec()
        # now available one gpu lost
        ssh_info = result.decode()
        if "MiB" in ssh_info:
            # valid
            one_gpu_info_whole = [_.split(',') for _ in ssh_info.split('\n') if len(_) > 0]
            one_gpu_info = [[ogi[0],ogi[2],ogi[3]] for ogi in one_gpu_info_whole]
            gpu_name = [ogi[1] for ogi in one_gpu_info_whole]
            one_gpu_info = [[int(h_.replace(' ','').replace('MiB','')) for h_ in _] for _ in one_gpu_info]
            out_info = '\n'.join([f"GPU{_[0]}[{h_[1:]}]: {_[1]:d}MiB/{_[2]:d}MiB" for _,h_ in zip(one_gpu_info,gpu_name)])
        else:
            out_info = "[ERROR] Invalid Info! Check Server Stage!"

        # print(out_info)
        # print('Connected to SSH share')
    except Exception as e:
        print('Something went wrong with the SSH connection')
        out_info = "[ERROR] Invalid Info! Check Server State!"
    return out_info


def decode_yaml(filename):
    with open(filename,'r') as f:
        ssh_cfg = yaml.safe_load(f)
    local_info = []
    server_info = []
    for key,v in ssh_cfg.items():
        if key == "local": # local_info:
            local_info = [v['ip'],v['port']]
        else: # server_info
            server_info.append([v['ip'],v['port'],v['id'],v['pwd'],
                                v['ip_name'],v['port_name'],not v['leaf']])
    return local_info,server_info
if __name__ == '__main__':
    import time
    from datetime import datetime
    local_info,server_info = decode_yaml(CFG_FILE)
    while True:
        with open(SAVE_FILE,'w') as f:
            f.write("[INFO] UPDATEING...\n")
            f.flush()
            out_info = f'UPDATE AT {datetime.now().strftime("%Y.%m.%D %H:%M:%S")}\n'
            out_info += f'IP {local_info[0]} Port{local_info[1]} :\n{query_gpu_self()}\n'
            for sf in server_info:
                if sf[-1]: # not leaf
                    out_info += f'[NONLEAF]:\n{query_noleaf_gpu(sf)}\n'
                else:
                    out_info += f'IP {sf[-3]} Port{sf[-2]} :\n{query_gpu(sf)}\n'
            f.write(out_info)
            f.flush()
        time.sleep(30)





