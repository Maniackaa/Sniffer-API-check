FROM python:3.10.11-slim-buster
WORKDIR /bot
RUN python3 -m venv venv
CMD ['source', 'env/bin/activate']
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /bot
# команда, выполняемая при запуске контейнера
#CMD [ "python", "bot_monitoring_uniswapinstant.py" ]