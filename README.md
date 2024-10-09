# The car owner bot


## Run bot using Docker


## Installing Docker


## Windows

Download the Docker Desktop installer from Docker Hub.
Run the installer and follow the installation instructions.
Once installed, start Docker Desktop.
------------------------------------------------------------------------------

### macOS

Download the Docker Desktop installer from Docker Hub.
Open the .dmg file and drag Docker to your Applications folder.
Start Docker from your Applications.
------------------------------------------------------------------------------

### Linux

For Ubuntu or Debian-based distributions, you can use the following commands:

``bash``

	sudo apt-get update
	sudo apt-get install -y \
		apt-transport-https \
		ca-certificates \
		curl \
		software-properties-common

	curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
	sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
	sudo apt-get update
	sudo apt-get install -y docker-ce
---------------------------------------------------------------------------------
For other Linux distributions, please refer to the official Docker installation documentation.

Start docker and enable docker (unix system):
``bash``
    sudo systemctl start docker
    sudo systemctl enable docker

Manage Docker as a Non-Root User:
``bash``
    sudo usermod -aG docker ${USER}


### Building the Docker Image

Open a terminal and navigate to the directory containing the project.
Run the following commands to start bot:

Create file with env TOKEN and DB_URD:
``bash``
    touch .env

Edit right for running scripr:
``bash``
    chmod +x run_bot.sh

Run script:

``bash``

    ./run_bot.sh	

Verify that the container is running:

``bash``

	docker service ls
