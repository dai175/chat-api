FROM python:3.11.8
ENV TZ=Asia/Tokyo

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.8.2

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . /app

RUN groupadd -g 1000 uvicorn
RUN useradd -m -s /bin/bash -u 1000 -g 1000 uvicorn

RUN chown -R uvicorn:uvicorn /app

USER uvicorn

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
