FROM python:3.12

WORKDIR /code

# Copy requirements first to leverage Docker cache
COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./main.py .

EXPOSE 8000

# Command to run the application
CMD ["fastapi", "run", "./main.py"]
