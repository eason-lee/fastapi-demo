FROM python:3.8

# Mirror
RUN echo "http://mirrors.aliyun.com/alpine/v3.8/main" > /etc/apk/repositories
RUN echo "http://mirrors.aliyun.com/alpine/v3.8/community" >> /etc/apk/repositories

# Soft
RUN apk add --no-cache gcc make musl-dev g++ linux-headers libffi-dev curl-dev zlib-dev
RUN pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple pip
RUN pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple cpython
RUN pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple numpy
RUN pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple pandas

WORKDIR /srv
COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python3", "main.py"]
