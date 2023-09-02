# Llama Inference

Minimalistic simple example to run Llama in container environment.


## Prerequisites

- VM with Nvidia GPU
- Nvidia GPU driver (`nvidia-smi` should work)
- `docker` & `docker compose`
- NVIDIA Container Toolkit (for me (Debian 12 & Tesla T4) worked instruction from [https://www.server-world.info/en/note?os=Debian_12&p=nvidia&f=2](https://www.server-world.info/en/note?os=Debian_12&p=nvidia&f=2))
- `git-lfs` for downloading weights from hugging face (`sudo apt install git-lfs`)


## How to launch

1. Download desired Llama version to `./models/` folder, e.g.:

```bash
(cd ./models && git clone https://huggingface.co/TheBloke/Llama-2-7B-GPTQ)
```

2. Specify model folder in `config.ini` in `[model]` section as `model_folder` parameter, e.g.:

```
[model]
model_folder=Llama-2-7B-GPTQ
```

3. Run the whole thing:

```bash
sudo docker compose up -d --build
```

## How to use

Now you have a web server which is capable of serving your requests, e.g.:

```bash
curl -X 'GET' \
  '0.0.0.0:4000/align?task=Learn%20to%20swim'
```
```
{"smart-aligned-task":"Practice swimming techniques regularly and master freestyle strokes by the end of summer."}
```
