FROM pytorch/pytorch:2.1.0-cpu

WORKDIR /code

# Copy requirements (torch already included)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy only app source
COPY ./src /code/src

# Expose port
EXPOSE 8000

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
