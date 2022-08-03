<div id="top"></div>
<!--
*** This repo contains sample Kafka producer/consumer dockerized code which connects to Kafka broker 
*** consumes messages from input topic then parse/correct messages containing timestamps
*** and loads them to target topic.
-->



<!-- PROJECT KAFKA_VALIDATE -->
<!--
*** The sample code can be cloned from repo and modified as required.
-->

[![LinkedIn][linkedin-shield]][https://www.linkedin.com/in/rahul-ramawat-b4462482/]

<!--This project contains -->

## Project Details
## KAFKA_VALIDATE

This repo contains sample Kafka producer/consumer dockerized code which connects to Kafka broker 
consumes messages from input topic then parse/correct messages containing timestamps
and loads them to target topic.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#setup">Project Setup</a>
      <ul>
        <li><a href="#how-to-run">How to run</a></li>
      </ul>
    </li>
    <li>
      <a href="#code-explaination">Code Explaination</a>
      <ul>
        <li><a href="#script-files">script files</a></li>
        <li><a href="#docker-files">docker files</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>



<!-- Project Setup -->
## Project Setup

The project is divided into python, docker , shell scripts.


In order to run the project below setups are required to be installed.


(1) Docker engine CE or any other Docker distributions.

(2) For Kafka distribution we are using Confluent docker base image along with zookeeper, if required the images latest version can be used.


(3) scripts / files:

    * PYTHON SCRIPTS  
    (a) message_setup.py -- This scripts creates sample data for our input topic, along with our topic creations.script is using a sample data file for loading multiple messages to input topic available under /sample_data/sample_json.txt , the values can be modified based on requirement, this script will be doing our initial load by loading all the data/json values into input topic of the kafka broker .
    (b) consumer_client.py -- This consumer client access the messages produced to input topic and then parses the timestamp(ISO-8601) and convert them  to UTC (ISO-8601), for doing this it calls a separate class written under '/kafka_class/validate_kafka_class.py' which does the work for processing the data and producing messaages to target topic.
    (c) validate_kafka_class.py -- This is the main class written to do most of the work (connecting to kafka cosumer/producer, subscribing to Kafka,topic, process ilformed timestamps, set configuration variables ).
    
    * SHELL SCRIPTS
    (a) build_image.sh -- This shell scripts is used to build the docker image.
    (b) build.sh -- available under '/scripts/build.sh' , this script acts as entry point of the docker image and run the scripts 'message_setup.py'    and 'consumer_client.py'.
    
    * DOCKER FILES
    (a) Docker.kafka_validate -- Docker file for building docker image of our consumer / producer client .
    (d) docker-compose.yml --  available under /docker-kafka/docker-compose.yml ,Docker compose file for Confluent (Kafka / Zookeeper) images.

    * CONFIG FILES
    (a) config.yml -- available under /config/config.ymlc ontains Kafka broker level configuration like topic names, broke names , kafka configs 
      Ex: #APPLICATION
          target_tz: UTC
          force_process: Y
          process_flag: Y

          #KAFKA
          kafka_broker: broker:29092
          source_topic: input_topic
          target_topic: output_topic
          group_id: foo
          batch_num_messages: 1
          queue_buffering_max_messages: 1

          # KAFKA-PRODUCER
          auto_commit_set: False
          auto_offset_reset: earliest

          # KAFKA-PRODUCER
          kafka_producer_poll: 0.0009
          kafka_prod_ack_flag: Y
    * SAMPLE DATA
    (a) sample_json.txt : This file contains sample JSON data which can be used to ingest data to inout topic
       Ex: {"myKey": 1, "myTimestamp": "2022-04-01T09:11:04+01:00"}
           {"myKey": 2, "myTimestamp": "2022-04-02T09:11:04+01:00"}

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started
This code consumes message from kafka input topic as below
{"myKey": 1, "myTimestamp": "2022-04-01T09:11:04+01:00"}
where the timestamps "myTimestamp" are in incorrect format (non UTC) and convert them to UTC.
it consumes data from input topic and after modifying the timestamp to UTC moves it to output topic
* There is a config variable available in cofig.yml 'target-tz' which can be configured to change the output of the timestamp conversion to desired    timezone.


### Prerequisites

Test if docker is installed or not
* docker
  ```sh
  docker version
  ```
* docker compose
  ```sh
  docker-compose version
  ```

### Installation

_Below is the process of installing and setting up this app.

   
1. Clone the repo in your home directory
   ```sh
   git clone https://github.com/ra1376/kafka_validate.git
   ```
2. CD to the folder and check the files
   ```sh
   cd ~/kafka_validate
   ```
3. Change execution permisison of files
   ```sh
   chmod +x *.sh
   ```
4. Change execution permisison of files
   ```sh
   cd ~/kafka_validte/docker-kafka
   ```
5. Execute Kafka / Zookeeper containers 
   ```sh
   docker-compose up -d
   ```
6. Check for containers status
   ```sh
   docker-compose ps
   ```
7. build docker container
   ```sh
   cd ~/kafka_validate
   ./build_image.sh
   ```
8. check container status
   ```sh
   docker ps
   ```
9. Inspect network allocated to Kafka container, by copying the container id by running command specified in step-6 and find for Network config 
   This step is required so that custom container and kafka container are on same network in docker , since docker assign custom network to containers created by docker-compose.
   
   ```sh
   docker inspect container_id
   ```
   ```sh
      "Networks": {
                "docker-kafka_default": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": [
                        "broker",
                        "5caab1476bec"
                    ],
   ```
10. run the application container
   ```sh
   docker run -i --network="docker-kafka_default" -t kafka_validate:latest /root/scripts/build.sh
   ```
11. Validate the console logs and you can messages being consumed and converted
    ```sh
      [I 220803 14:18:41 validate_kafka_class:202] Consumed event from topic input_topic: key = 10           value = {"myKey": 10, "myTimestamp": "2022-04-10T09:11:04+01:00"}
      [I 220803 14:18:41 validate_kafka_class:208] processing processed messages to target_topic for incorrect timestamp values to topic : output_topic
      [I 220803 14:18:41 validate_kafka_class:214] {"myKey": 10, "myTimestamp": "2022-04-10T08:11:04+00:00"}
      [I 220803 14:18:41 validate_kafka_class:110] connecting function connect_kafka_producer
      [I 220803 14:18:41 validate_kafka_class:119] producer properties {'bootstrap.servers': 'broker:29092', 'acks': 'all', 'batch.num.messages': 1, 'queue.buffering.max.messages': 1}
      [I 220803 14:18:41 validate_kafka_class:76] Produced event to topic output_topic: key = 10           value = {'myKey': 10, 'myTimestamp': '2022-04-10T08:11:04+00:00'}
      [I 220803 14:18:41 validate_kafka_class:219] processed messages to Kafka target topic
      [I 220803 14:18:41 validate_kafka_class:202] Consumed event from topic input_topic: key = 11           value = {"myKey": 11, "myTimestamp": "2022-04-11T09:11:04+01:00"}
      [I 220803 14:18:41 validate_kafka_class:208] processing processed messages to target_topic for incorrect timestamp values to topic : output_topic
      [I 220803 14:18:41 validate_kafka_class:214] {"myKey": 11, "myTimestamp": "2022-04-11T08:11:04+00:00"}

    ``` 

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- Note -->
## Note

* If there is change of topic name and in Broker name , then for intial setup these values are required to be changed under 'message_setup.py', for consumer app the changes can be directly configured under config.yml
* validate_kafka_class does not check for other type of data under "myTimestamp" if there is another type of data then the program would fail.
* Function documentation was not done. yet to be done.
* Consumer will do synchronous commit of the message after every 1000 messages are consumed.
* Quit the consumer client on console by typing CTRL-C.
* In case of kafka broker not running when run docker-compose then kill the containers and re-run.


<p align="right">(<a href="#top">back to top</a>)</p>

