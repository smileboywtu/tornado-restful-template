FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN addgroup -S tornado \
    && adduser -S -G tornado tornado

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/production/tornado/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
RUN chown tornado /entrypoint

COPY ./compose/production/tornado/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
RUN chown tornado /start

COPY ./compose/production/tornado/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker
RUN chown tornado /start-celeryworker

COPY ./compose/production/tornado/celery/beat/start /start-celerybeat
RUN sed -i 's/\r//' /start-celerybeat
RUN chmod +x /start-celerybeat
RUN chown tornado /start-celerybeat

COPY ./compose/production/tornado/celery/flower/start /start-flower
RUN sed -i 's/\r//' /start-flower
RUN chmod +x /start-flower

COPY . /app

RUN chown -R tornado /app

USER tornado

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
