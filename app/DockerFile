FROM python:3.10.4-buster
WORKDIR /app
RUN python -m pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
