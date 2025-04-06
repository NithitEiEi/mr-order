FROM python:3.11

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY .env .

COPY app .

COPY prisma .

EXPOSE 8000

CMD ["sh", "-c", "prisma generate && prisma migrate deploy && python main.py" ]