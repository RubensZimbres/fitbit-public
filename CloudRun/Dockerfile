FROM python:3.9

EXPOSE 8080
ENV PORT 8080

WORKDIR /home

COPY . /home
RUN pip install -r /home/requirements.txt

CMD python3 /home/prediction.py