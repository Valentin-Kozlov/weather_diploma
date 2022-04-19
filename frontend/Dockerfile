FROM python:alpine3.14

WORKDIR /usr/src/app

COPY requirements.txt .

RUN adduser -D user

RUN apk add --no-cache \
    # gcc \
    # musl-dev \
    # mariadb-dev \
    bash

RUN pip install --upgrade pip && pip install -r requirements.txt

USER user

ENV FLASK_APP frontend.py
ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Yekaterinburg

EXPOSE 5000

COPY --chmod=755 . .

ENTRYPOINT [ "/usr/src/app/entry.sh" ]