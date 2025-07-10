
FROM python:3.13.5


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./main.py /code/app


CMD ["fastapi", "run", "app/main.py", "--port", "80"]