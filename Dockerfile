FROM python:3.10

WORKDIR /assessment

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./assessment /assessment

EXPOSE 5000

ENTRYPOINT ["python3", "-m", "flask", "--app", "src.api", "run", "--host", "0.0.0.0"]


