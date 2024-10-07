# Бот для автовладельцев
быстрый старт:
создайте виртуальное окружение:

	python -m venv .venv
 
войдите в него:
Windows:

	.venv/Scripts/activate

Unix-systems:

	source .venv/bin/activate

Установите зависимости:

	pip install -r requirements.txt




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

### Building the Docker Image

Open a terminal and navigate to the directory containing the project.
Run the following command to build the Docker image:

``bash``

	docker build -t my-aiogram-bot .

Running the Bot

Run the Docker container with the following command:

``bash``

	docker run -d --name my-aiogram-bot-container 


Verify that the container is running:

``bash``

	docker ps

 
bd - https://app.creately.com/d/YX0TxokiOIM/edit

