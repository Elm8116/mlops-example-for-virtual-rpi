
### Deploy TFLite model into Raspberry Pi 4 with GitHub Actions
Creating a workflow with the following stages:

- Build Docker Image and push it to Docker Hub Registry.
- Testing - Download the Docker Image from container registry and test it on Raspberry Pi
- Deploy the docker image on Raspberry Pi  