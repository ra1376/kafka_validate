echo "building docker image for Kafka validation"
export CONTAINER_NAME=kafka_validate:latest
echo ${CONTAINER_NAME} 
cd /home/rahul/kafka_validate
sudo docker build -f Dockerfile.kafka_validate -t ${CONTAINER_NAME} .
sudo docker images ${CONTAINER_NAME}