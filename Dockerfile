FROM python:3.8

ADD ./main.py .
ADD ./time_series_visualizer.py .
ADD ./test_module.py .

ADD ./fcc-forum-pageviews.csv .

ADD ./requirements.txt .

RUN pip install -r requirements.txt
RUN pip install seaborn --upgrade

CMD ["python3", "./main.py"]