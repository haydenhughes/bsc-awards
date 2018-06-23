FROM python:3.6.5

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

CMD python3 run.py --config Development
