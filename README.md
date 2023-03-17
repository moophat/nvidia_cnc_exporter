# nvidia_cnc_exporter
cd liqid_exportet

docker build -t <image_name>:<image_tag> .

docker run -v <local_config>:<container_config> <image_name>:<image_tag> <container_config>
