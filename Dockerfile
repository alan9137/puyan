FROM python
WORKDIR /puyan

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /puyan

EXPOSE 8000

VOLUME [ "/puyan" ]

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]
