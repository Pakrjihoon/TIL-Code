FROM python as build
WORKDIR /install
COPY ./requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt

FROM python:slim
WORKDIR /app
COPY --from=build /install /usr/local
COPY ./*.py ./
EXPOSE 5000

ENTRYPOINT ["python", "waitress_server.py"]