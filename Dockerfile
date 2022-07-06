FROM arm64v8/python:3.8-slim-buster
RUN apt-get -y update && apt-get install -y wget


# creating a working directory so we do not need to type a full file paths and can use relative paths based on working directory
WORKDIR /app

# copy all files into image
ADD . /app

RUN pip install -r requirements.txt
RUN pip install tritonclient\[all]\


EXPOSE 8080

# execute the Flask app in the container
ENTRYPOINT ["python3"]
HEALTHCHECK CMD curl --fail http://localhost:8080 || exit 1
CMD ["app.py"]
