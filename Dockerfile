FROM python:3.7-slim as development
WORKDIR /usr/src/app
RUN apt update && apt install fonts-noto-cjk \
  && pip install --upgrade pip
COPY src /usr/src/app
RUN pip install .
COPY pandas_profiling.mplstyle /usr/local/lib/python3.7/site-packages/pandas_profiling/view/pandas_profiling.mplstyle
CMD ["bq_profile"]

FROM development as release
ENTRYPOINT ["bq_profile"]
