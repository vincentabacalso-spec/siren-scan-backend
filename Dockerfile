# Use CPU-only PyTorch wheel base
FROM pytorch/pytorch:2.1.0-cpu-py3.11

WORKDIR /code

# Copy and install dependencies (torch is already included)
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy only app source code
COPY ./src /code/src

# Expose port for FastAPI
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
