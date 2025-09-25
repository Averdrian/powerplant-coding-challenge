FROM rockylinux/rockylinux:9-minimal


RUN microdnf install -y python3 python3-pip

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 8888


ENTRYPOINT ["python3", "app.py"]