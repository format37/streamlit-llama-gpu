# app/Dockerfile

# FROM python:3.10-slim
# FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-devel
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel


# FROM nvidia/cuda:11.8.0-devel-ubuntu22.04
# Update the package list
# RUN apt-get update
# Install Python 3 and pip3
# RUN apt-get install -y python3 python3-pip




WORKDIR /app

# COPY llama-2-7b-chat.ggmlv3.q2_K.bin llama-2-7b-chat.ggmlv3.q2_K.bin

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
# RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY app.py app.py
COPY server.py server.py

EXPOSE 8501

# ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
# Fastapi server.py
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8501"]
# ENTRYPOINT ["nvidia-smi"]