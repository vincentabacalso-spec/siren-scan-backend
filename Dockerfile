FROM python:3.11-slim

WORKDIR /code

# Copy requirements (torch installed via pip)
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --prefer-binary --no-cache-dir -r requirements.txt

COPY ./src /code/src

EXPOSE 8000

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
