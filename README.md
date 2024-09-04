# ec2-jenkins-agent-deployment

![Amazon Web Services Badge](https://img.shields.io/badge/Amazon%20Web%20Services-232F3E?logo=amazonwebservices&logoColor=fff&style=for-the-badge)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Jenkins](https://img.shields.io/badge/jenkins-%232C5263.svg?style=for-the-badge&logo=jenkins&logoColor=white)
![Apache Groovy](https://img.shields.io/badge/Apache%20Groovy-4298B8.svg?style=for-the-badge&logo=Apache+Groovy&logoColor=white)
![Amazon EC2 Badge](https://img.shields.io/badge/Amazon%20EC2-F90?logo=amazonec2&logoColor=fff&style=for-the-badge)
![Ubuntu Badge](https://img.shields.io/badge/Ubuntu-E95420?logo=ubuntu&logoColor=fff&style=for-the-badge)

# Context

This project is a Jenkins pipeline to deploy EC2 instances to be used as Jenkins Agents.
Once configured in Jenkins as a multibranch pipeline, the job deploy a new Cloudformation stack which creates an EC2 instance. You can choose between Amazon Linux 2 or Ubuntu 20.04.

Once the instance is deployed, SSH into the instance to generate the SSH key to be used to connect the instance to your Jenkins Server / cluster via SSH.

There are other connection methods, but SSH was my prefered method for this deployment.

# After deployment
The basics of the agent server is setup. Jenkins user added, home dir set, and ssh key generated. However, the ssh key was generated without a passphrase. This must be added.
First step - determine what the passphrase will be then, do the following two commands

    sudo -u jenkins bash
    ssh-keygen -p -f /var/jenkins/.ssh/jenkinsAgent_rsa

Once the passphrase has been created, store it and the private key in the password store

