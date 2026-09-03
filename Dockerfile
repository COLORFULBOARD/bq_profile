FROM python:3.12-slim as development
WORKDIR /usr/src/app
RUN apt update && apt install fonts-noto-cjk \
  && pip install --upgrade pip
COPY src /usr/src/app
RUN pip install .
CMD ["bq_profile"]

FROM development as release
ENTRYPOINT ["bq_profile"]
