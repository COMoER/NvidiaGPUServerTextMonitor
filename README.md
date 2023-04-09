# NvidiaGPUServerTextMonitor v0.1

- Just run
  
```bash
SAVE_FILE=/dataset/gpu_query CFG_FILE=ssh_gpu_cfg_sample.yaml python upload_SFML_status.py
```
- A demo
```
[INFO] UPDATEING...
UPDATE AT ***
IP *** Port*** :
GPU0[***]: 24092MiB/24576MiB
GPU1[***]: 18846MiB/24576MiB
GPU2[***]: 23856MiB/24576MiB
[NONLEAF]:
######################
[INFO] UPDATEING...
UPDATE AT ***
IP *** Port*** :
GPU0[***]: 13975MiB/24268MiB
GPU1[***]: 9335MiB/24268MiB
GPU2[***]: 21270MiB/24268MiB
GPU3[***]: 21755MiB/24265MiB
######################
IP *** Port*** :
GPU0[***]: 22283MiB/24576MiB
GPU1[***]: 22263MiB/24576MiB
GPU2[***]: 220MiB/24576MiB

```
- `~/.bashrc` quick command
```bash
alias GPUinspect='cat /data0/dataset/gpu_query'
```
- Pkg Requirement
```bash
pip install paramiko
pip install pyyaml==5.4.1
```


