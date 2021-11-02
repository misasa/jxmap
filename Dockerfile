FROM python:2.7
WORKDIR /root/jxmap
COPY . /root/jxmap
RUN pip install --upgrade pip && \
  pip install -r /root/jxmap/requirements.txt && \
  pip install /root/jxmap

#RUN pip install .

