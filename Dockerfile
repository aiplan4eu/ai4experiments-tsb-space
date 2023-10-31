FROM python:3.8

WORKDIR /up-service
COPY . /up-service

RUN ln -s /up-service/tsb-space/src /up-service/src/tsb_space_src

RUN cp /up-service/tsb-space/src/* /up-service/src

RUN pip install -r requirements.txt

RUN pip install /up-service/up-graphene-engine

EXPOSE 8061 8062

CMD ["python", "src/run.py"]
