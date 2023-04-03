FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt 
RUN pip install firebase flask flask_cors invokes pika requests
ENV account_URL=http://localhost:5200
ENV location_URL=http://localhost:8080
ENV listing_URL=http://localhost:5001
COPY ./BuyItem.py ./invokes.py ./amqp_setup.py ./
CMD [ "python", "./LoginAccount.py" ]