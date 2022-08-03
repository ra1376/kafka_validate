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
    (a) message_setup.py -- This scripts creates sample data for our input topic, along with our topic creations.
                            script is using a sample data file for loading multiple messages to input topic available under /sample_data/sample_json.txt , the values can be modified based on requirement, this script will be doing our initial load by loading all the data/json values into input topic of the kafka broker .
    (b) consumer_client.py -- This consumer client access the messages produced to input topic and then parses the timestamp(ISO-8601) and convert them 
                              to UTC (ISO-8601), for doing this it calls a separate class written under '/kafka_class/validate_kafka_class.py' which does the work for processing the data and producing messaages to target topic.
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


<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

(1) Please clone the repo inside your home directory.


### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 