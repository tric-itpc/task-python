# Pull official base Python Docker image
FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy FastAPI project
COPY . /code/

# Set the command to run the uvicorn server.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]