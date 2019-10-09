FROM python:3.7-slim
WORKDIR /usr/src/app
RUN apt update && apt install fonts-noto-cjk \
  && pip install --upgrade pip \ 
  && pip install pandas pandas-profiling pandas-gbq google-cloud-storage
COPY src /usr/src/app
RUN pip install .
COPY pandas_profiling.mplstyle /usr/local/lib/python3.7/site-packages/pandas_profiling/view/pandas_profiling.mplstyle
ENTRYPOINT ["bq_profile"]
