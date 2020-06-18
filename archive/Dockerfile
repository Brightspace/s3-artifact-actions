FROM python:slim
RUN pip install boto3
COPY entrypoint.py /entrypoint.py
RUN chmod ug+x /entrypoint.py
ENTRYPOINT ["/entrypoint.py"]