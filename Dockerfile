FROM python:3.9-slim
WORKDIR /app

RUN apt-get update && apt-get install -y tini && apt-get clean
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY app/. .

ENV DATE=DEC-16-2024

LABEL version=$DATE company=Gopenux

ENTRYPOINT ["tini", "--"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]