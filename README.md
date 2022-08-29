## Building MLOps Pipelines with GitHub Actions on ARM Virtual Raspberry Pi 4  

ARM virtual Raspberry Pi 4 virtualizes the functional behavior of SoCs and development kits,
including peripherals, sensors, and other components of Raspberry Pi development board. 
It utilizes cloud-based servers and enable modern agile software development practices,
such as continuous integration and continuous deployment CI/CD (DevOps) and MLOps workflows to software developers. 

The objective of this project is to automate the image classification web-application deployment process on virtual raspberry pi 4 using GitHub Actions.

The workflow contains the following stages:
1. Build a docker image for the application using Dockerfile
2. Invoke triton inference server with Arm NN backend
   * The models are served with [Triton Inference Server with Arm NN backend](https://gitlab.com/arm-research/smarter/armnn_tflite_backend) to accelerate inference
3. Run Unittest to test Flask server by checking if it is retuning 200 status code
4. Login to Docker Hub and Push image 
5. Deploy the application on virtual raspberry pi


### Prerequisites 

#### Triton Inference Server Model Repository Layout
To load the model in triton inference server with Arm NN backend, a model repository with the following structure should be created. These repository paths are specified when triton is started using ```--model-reposiotry``` option. Find more details about the model repository and directory structure in Triton inference server from [documentation](https://github.com/triton-inference-server/server/blob/r20.12/docs/model_repository.md). The below is an example model repository layout for MobileNet:   
``` models
├── tflite_model
│   ├── 1
│   │   └── model.tflite
│   └── config.pbtxt
|   └── labels.txt
```
#### Download MobileNet model in its subdirectory 

```
# Get the model 
$ mkdir mobilenet 
$ curl http://download.tensorflow.org/models/mobilenet_v1_2018_08_02/mobilenet_v1_1.0_224.tgz | tar xvz -C ./mobilenet

# Get labels corresponding to each image 
$ curl https://storage.googleapis.com/download.tensorflow.org/models/mobilenet_v1_1.0_224_frozen.tgz | tar xzv –C ./mobilenet 

$ mkdir -p models/tflite_model/1 

$ mv mobilenet/mobilenet_v1_1.0_224.tflite models/tflite_model/1

$ cp mobilenet/mobilenet_v1_1.0_224/labels.txt models/tflite_model
```

#### Triton Inference Server Model Configuration and Runtime Optimization with Am NN Delegate 
Each model in the model repository must include a model config that provides required and optional information about the model such as Name, Platform and Backend. To accelerate inference on Raspberry Pi with Cortex-A72 processor use cpu acceleration with ```armnn``` parameter in the optimization model configuration as follow:

``` configuration = """
name: "tflite_model"
backend: "armnn_tflite"
max_batch_size: 0
input [
 {
   name: "input"
   data_type: TYPE_FP32
   dims: [ 1, 244, 244, 3 ]
 }
]
output [
 {
   name: "MobilenetV1/Predictions/Reshape_1"
   data_type: TYPE_FP32
   dims: [ 1, 1001 ]
 },

]
optimization { execution_accelerators {
 cpu_execution_accelerator : [ { name : "armnn" } ]
}}
""" 
```


### Set up and Configure Virtual Raspberry Pi 4 
1. Login to your Arm Virtual Hardware account at https://app.avh.arm.com/ 
2. Create virtual Raspberry Pi 4 Device and Choose Raspberry Pi OS lite (11.2.0) 
3. Select **CONSOLE** from device menu and login to your virtual device using the default username: _pi_ and 
password: _raspberry_ 
4. Connect to your virtual device via VPN 
   * download the .ovpn file from the Raspberry Pi 4's Connect tab 
   * connect to your virtual device using openvpn
   
      ```sudo openvpn --config ~/Downloads/AVH_config.ovpn```
      
If you are on Mac OS or Windows OS, follow the steps in this [article](https://intercom.help/arm-avh/en/articles/6131455-connecting-to-the-vpn) to connect to your virtual device

### Set up Docker Hub and AVH API Tokens 
1. Install Docker on Virtual Raspberry Pi 4

   ```sudo apt-get update```

   ```sudo apt-get install -y jq docker.io```
2. Check if the service is running
   ```sudo systemctl status docker```
   
**Note**: In case identifying issues with the Device Kernel, follow the steps in [Updating Raspberry Pi page](https://intercom.help/arm-avh/en/articles/6278501-updating-the-raspberry-pi-4-kernel#h_f3c477ba86) to fix the updated kernel 

3. Authenticate yourself with GitHub container registry following the steps in [GitHub page](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-to-the-container-registry)
   * select ```repo``` ```workflow``` ```write:packages``` ```delete:packages``` 
   * login to ghcr.io from your Raspberry Pi Console 
   ```sudo cat ~/githubtoken.txt | docker login https://ghcr.io -u <username> --password-stdin```
4. Authenticate yourself with Docker Hub and use your Docker Hub username ```DOCKERHUB_USERNAME``` and token ```DOCKERHUB_TOKEN``` as secrets in your GitHub repo. To do so, follow these steps:
   * sign in to Docker Hub
   * select account settings on the top right of the page
   * select security tab from the left sidebar 
   * generate NEW Access Token and save it 
5. From Docker Hub dashboard, click Create Repository and type name ```ml-app-pi``` in the Name section 
   
**Note**: You need to [Sign Up](https://hub.docker.com/signup) to Docker Hub if you do not have an account.

6. Generate an AVH API Token following the steps in [Generating an API Token](https://intercom.help/arm-avh/en/articles/6137393-generating-an-avh-api-token) article and save it. 
7. Select Raspberry Pi 4 CONSOLE tab and clone the repository 
8. Set up Secrets in GitHub Action workflows to accept jobs 
   * navigate to the main page of your repository.
   * click on the "Setting" tab on the top of the page.
   * in the left sidebar, click Secrets and select Actions.
   * on the right bar, click on "New repository secret".
   * add ```API_TOKEN``` secret to your repository with a value of your API Token.
   * add ```DOCKERHUB_USERNAME``` and ```DOCKERHUB_TOKEN``` secrets to your repository with a value of your username and a token generated in the step 4.
   
### Add Self-hosted Runner 

1. [Add Self Hosted Runner](https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners) to the repository and select "Linux" as the OS and "ARM64" as the architecture 
2. From Raspberry Pi 4 CONSOLE tab, run the commands referenced in the previous step 
3. Navigate to ```actions_runner``` directory and start the runner: 

    ```cd actions_runner```

    ``` ./run.sh```




