FROM python:3.11-slim

WORKDIR /cliente

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
CMD ["python", "./cliente.py"]

