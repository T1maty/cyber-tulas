FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


#Comment: This Dockerfile sets up a FastAPI application with Python 3.12.
# It installs the required dependencies from requirements.txt and starts the application using uvicorn.

