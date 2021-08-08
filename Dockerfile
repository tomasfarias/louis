FROM tiangolo/uvicorn-gunicorn-fastapi:python3.6

COPY . /app

CMD ["uvicorn", "louis.rest_api:app", "--host", "0.0.0.0", "--port", "8080"]
