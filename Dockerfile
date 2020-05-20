FROM python:3.8

RUN apt-get update
RUN apt-get install -y x11-apps xauth graphviz libgraphviz-dev pkg-config
ADD requirements.txt /
RUN pip install -r requirements.txt

ADD src /src
ADD main.py /

CMD [ "python", "./main.py" ]