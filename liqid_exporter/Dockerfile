FROM python:3.6-slim
WORKDIR /opt/nvidia_cnc_exporter
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY . .
CMD ["python", "server.py"]
EXPOSE 9023
