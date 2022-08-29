#
# SPDX-FileCopyrightText: Copyright 2022 Arm Limited and/or its affiliates <open-source-office@arm.com>
# SPDX-License-Identifier: MIT
#

FROM arm64v8/python:3.8
RUN apt-get -y update 


# creating a working directory so we do not need to type a full file paths and can use relative paths based on working directory
WORKDIR /app

# copy all files into image
ADD . /app

RUN mkdir -p uploads
RUN pip install tritonclient\[all\]
RUN pip install -r requirements.txt



EXPOSE 8080

# execute the Flask app in the container
ENTRYPOINT ["python3"]
HEALTHCHECK CMD curl --fail http://localhost:8080 || exit 1
CMD ["app.py"]
