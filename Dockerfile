FROM python:3.10.5-slim-buster
WORKDIR /app
RUN apt update && apt upgrade -y && \
    apt install --no-install-recommends -y \
    bash \
    python3-pip \
    python3-requests \
    python3 \
    python3-dev \
    sudo \
    && rm -rf /var/lib/apt/lists /var/cache/apt/archives /tmp

COPY requirement.txt requirement.txt
RUN pip3 install -r requirement.txt

COPY . .

CMD ["python3", "telegram_bot.py"]
