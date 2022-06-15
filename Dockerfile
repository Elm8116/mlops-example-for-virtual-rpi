FROM python:3.8-slim-buster

# FROM arm64v8/ubuntu
# ENV TZ=America/Toronto

# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# RUN apt-get update && \
#     apt-get -y install -y sudo  \
#     python3 \
#     python3-pip \
#     qemu binfmt-support qemu-user-static \
#     wget


RUN wget -O ArmNN-aarch64.tgz https://github.com/ARM-software/armnn/releases/download/v22.02/ArmNN-linux-aarch64.tar.gz \
&& mkdir -p ArmNN-aarch64 \
&& tar -xvf ArmNN-aarch64.tgz -C ArmNN-aarch64

# creating a working directory so we do not need to type a full file paths and can use relative paths based on working directory
WORKDIR /app

# copy all files into image
ADD . /app

RUN pip install -r requirements.txt
RUN cd .. && cp ArmNN-aarch64/libarmnn.so.28 /app && cp ArmNN-aarch64/libarmnnDelegate.so.25 /app

EXPOSE 8080

# execute the Flask app in the container
ENTRYPOINT ["python3"]
HEALTHCHECK CMD curl --fail http://localhost:8080 || exit 1
CMD ["app.py"]
