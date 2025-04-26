FROM python:3.11-slim

WORKDIR /cliente

COPY . .

#RUN pip install --no-cache-dir -r requirements.txt
# Instala dependências necessárias
#RUN pip install --no-cache-dir windows-curses
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]

ENTRYPOINT ["python", "./cliente.py"]

