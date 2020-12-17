FROM python:3.8

WORKDIR /app/fastapi-demo

ADD ./requirements.txt /app/
RUN pip install --trusted-host mirrors.aliyun.com -i http://mirrors.aliyun.com/pypi/simple/ -r /app/requirements.txt

ADD ./entrypoint.sh /entrypoint.sh
ENTRYPOINT ["bash", "/entrypoint.sh"]

ADD . /app

CMD ["python3", "main.py"]
