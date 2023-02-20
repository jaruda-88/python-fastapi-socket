FROM python:3.10

# working dir
WORKDIR /app/

# install dependences
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy source
COPY . /app

# run

CMD ["python3", "main.py"]