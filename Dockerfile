# build and deploy Flask app
FROM python:3.8-slim-buster


# creating a working directory so we do not need to type a full file paths and can use relative paths based on working directory
WORKDIR /app

# copy all files into image
ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8080

# execute the Flask app in the container
ENTRYPOINT ["python"]
HEALTHCHECK CMD curl --fail http://localhost:8080 || exit 1
CMD ["app.py"]