FROM pypy:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./

CMD [ "pypy3", "./main.py" ]