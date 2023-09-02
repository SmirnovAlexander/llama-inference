FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04

RUN apt update && apt install -y python-is-python3 python3-pip 

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY . .

CMD ["python", "main.py"]
