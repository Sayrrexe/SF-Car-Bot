# The car owner bot


## Run bot using Docker Swarm


## Installing Docker


We suggest that you are using Linux Ubuntu or Red Hat for deploying app in other case please refer to the official Docker installation documentation.

### Starting app

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

Verify that the containers is running:

``bash``

	docker service ls
