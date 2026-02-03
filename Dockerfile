FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /code

# Copy requirements from root
COPY requirements.txt .

# Install dependencies (torch already in base image)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory
COPY ./src /code/src

# Expose port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
