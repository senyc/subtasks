FROM python:3.12

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8000

# Command to run the application
CMD ["fastapi", "run", "./main.py"]
