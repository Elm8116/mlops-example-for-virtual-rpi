## Building MLOps Pipelines with GitHub Actions on ARM Virtual Raspberry Pi 4  

ARM virtual Raspberry Pi 4 virtualizes the functional behavior of SoCs and development kits,
including peripherals, sensors, and other board components of Raspberry Pi development board. 
It utilizes cloud-based servers and enable modern agile software development practices,
such as continuous integration and continuous deployment CI/CD (DevOps) and MLOps workflows to software developers. 

The objective of this project is to automate the image classification web-application deployment process on virtual raspberry pi 4 using GitHub Actions.
The workflow contains the following stages:
1. Build a docker image for the web-application
2. Invoke triton inference server with Arm NN backend
   * The models are served with [Triton Inference Server with Arm NN backend](https://gitlab.com/arm-research/smarter/armnn_tflite_backend) to accelerate inference
3. Run Unittest
4. Login to Docker Hub and Push image 
5. Deploy the application on virtual raspberry pi

### Set up and Configure Virtual Raspberry Pi 4 
1. Login to your Arm Virtual Hardware account at https://app.avh.arm.com/ <br /><br />
2. Create virtual Raspberry Pi 4 Device and Choose Raspberry Pi OS lite (11.2.0) <br /><br />
3. Select **CONSOLE** from device menu and login to your virtual device using the default username: _pi_ and password: _raspberry_ <br /><br />
4. Connect to your virtual device via VPN <br />
   1. download the .ovpn file from the Raspberry Pi 4's Connect tab 
   2. connect to your virtual device using openvpn
   
      ```sudo openvpn --config ~/Downloads/AVH_config.ovpn```
      * If you are on Mac OS or Windows OS, follow the steps in this [article](https://intercom.help/arm-avh/en/articles/6131455-connecting-to-the-vpn) to connect to your virtual device

### GitHub Actions

1. Install Docker on Virtual Raspberry Pi 4

   ```sudo apt-get update```

   ```sudo apt-get install -y jq docker.io```
<br /><br /> 
2. Check if the service is running

   ```sudo systemctl status docker```

   * in case having a failed state, fix the updated kernel following the steps in [Updating Raspberry Pi page](https://intercom.help/arm-avh/en/articles/6278501-updating-the-raspberry-pi-4-kernel#h_f3c477ba86) in case identifying issues with the Device Kernel <br /><br />
3. Authenticate yourself with GitHub container registry following the steps in [GitHub page](https://github.com/Azure/actions-workflow-samples/blob/master/assets/create-secrets-for-GitHub-workflows.md)
   * select ```repo``` ```workflow``` ```write:packages``` ```delete:packages``` 
   * login to ghcr.io from your Raspberry Pi Console <br />
   ```sudo cat ~/githubtoken.txt | docker login https://ghcr.io -u <username> --password-stdin```
<br />
   
**Note**: You need to [Sign Up](https://hub.docker.com/signup) to Docker Hub if you do not have an account.
<br /><br />
4. Generate an AVH API Token following the steps in [Generating an API Token](https://intercom.help/arm-avh/en/articles/6137393-generating-an-avh-api-token) article. 
<br /><br />
5. Clone the repository <br /><br />
6. Set up Secrets in GitHub Action workflows to accept jobs 
   1. navigate to the main page of your repository
   2. click on the "Setting" tab on the top of the page
   3. in the left sidebar, click Secrets and select Actions
   4. on the right bar, click on "New repository secret"
   5. add "API_TOKEN" secret to your repository with a value of your API Token
<br /><br />
7. [Add Self Hosted Runner](https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners) to the repository and select "Linux" as the OS and "ARM64" as the architecture <br /><br />
8. From Raspberry Pi 4 CONSOLE tab, run the commands referenced in the previous step <br /><br />
9. Navigate to ```actions_runner``` directory and start the runner using the following commands <br />
   ```cd actions_runner```<br />
   ``` ./run.sh```




