FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
RUN pip install firebase flask flask_cors invoke pika requests
COPY ./loginaccount.py ./invokes.py ./amqp_setup.py ./
CMD [ "python", "./loginaccount.py" ]