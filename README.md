# nvidia_cnc_exporter

## Step 1: Build docker images
cd liqid_exporter

docker build -t <image_name>:<image_tag> .

## Step 2: Edit config.yaml file
Edit port for docker container in "port" section

Edit api link in "links" section

## Step 3: Edit docker-compose.yml
Edit path to local config.yaml file in "volumes" section in docker-compose.yml to mount local config.yaml to container

Edit "port" section in docker-compose.yml to expose port from docker container to outside.

## Step 4: Run docker compose
docker compose up
