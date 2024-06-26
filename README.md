<a name="readme-top" id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/MeorIdlan/subway-surf">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Malaysia Subway Location Searcher</h3>

  <p align="center">
    Web Application that searches for Subway locations in Malaysia
    <br />
    <a href="https://github.com/MeorIdlan/subway-surf"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/MeorIdlan/subway-surf/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/MeorIdlan/subway-surf/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://github.com/MeorIdlan/subway-surf)

So what makes this different from Subway's [original website](https://subway.com.my/find-a-subway)?

This project actually enhances on the current capabilities of the original website, on top of also having their existing features.

Here are some of the enhancements:
* Uses NLP to understand more complex queries such as: "Which stores are open at 8AM?", "List out stores that are in Kuala Lumpur."
* Features a catchment circle around a selected location (in case you wanna see your options)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python-logo]][Python-url]
* [![React][React.js]][React-url]
* [![HTML5][HTML5]][HTML5-url]
* [![CSS][CSS]][CSS-url]
* [![JavaScript][JavaScript]][JavaScript-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Follow the steps to get a local copy running.

### Prerequisites

You must have these before continuing.
* npm
  ```sh
  npm install npm@latest -g
  ```
* [Python 3.10](https://www.python.org/downloads/release/python-3100/) or above (later versions not tested, might be unstable)
* An API key from Google with Google Maps API enabled (you can get one [here](https://console.cloud.google.com)). Here's how to [enable Google APIs](https://support.google.com/googleapi/answer/6158841?hl=en)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/MeorIdlan/subway-surf.git
   ```

2. Frontend installation
    1. Open terminal and navigate to `/frontend/mh-webapp`

    2. Install NPM packages

        ```sh
        > npm install
        ```

    3. Create a new file named `api_key.tsx` in the same directory as App.tsx. In the file, enter your API key as follows and save:

        ```js
        export const API_KEY = 'YOUR_API_KEY_HERE'
        ```

3. Backend installation
    1. Navigate to `/backend`

    2. Create a virtual environment. [How to create venv](https://realpython.com/python-virtual-environments-a-primer/)

    3. Activate venv.

        (for Windows users)
        ```sh
        > venv/Scripts/activate
        ```
        (for Linux/macOS users)
        ```sh
        $ venv/bin/activate
        ```

    4. Install packages

        ```sh
        python -m pip install -r requirements.txt
        ```

    5. Download spaCy's `en_core_web_sm` pipeline

        ```sh
        python -m spacy download en_core_web_sm
        ```

    6. Install Playwright browsers

        ```sh
        playwright install
        ```

    7. This step ONLY for Windows users. To run redis (the database/cache used in this project), you need to install WSL. More info [here](https://learn.microsoft.com/en-us/windows/wsl/install).

        ```sh
        wsl --install
        ```
        After installing, run Ubuntu from your searchbar.

    8. Install Redis. (For Windows users, do this step in your WSL.)

        (from the [Redis docs](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/))
        ```sh
        curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

        echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

        sudo apt-get update
        sudo apt-get install redis
        ```

        For macOS users, I'm sorry but I don't have any experience with your OS. Here is the official [Redis docs](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-mac-os/) on how to install Redis on macOS though. Good luck!

    9. Start the Redis server. This needs to run every time you want to use the web app.

        ```sh
        sudo service redis-server start
        ```

        You can test if your server is running or not with the following command:
        ```sh
        redis-cli
        127.0.0.1:6379> ping
        PONG
        ```

4. Once you have the frontend and backend setup, you can start the webapp.

    1. Navigate to `/backend`

    2. Activate venv (if you haven't already)

    3. Start the Flask server

        ```sh
        python app.py
        ```

    4. Navigate to `/frontend/mh-webapp`

    5. Start the node development server

        ```sh
        npm start
        ```

5. Wait for the server to start...

6. Subway Surfer!


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Here are some screenshots of the web app in action:

[![Product Name Screen Shot][product-screenshot-1]]()
_<p align="center">Main screen</p>_

[![Product Name Screen Shot][product-screenshot-2]]()
_<p align="center">Clicking on a pin</p>_

[![Product Name Screen Shot][product-screenshot-3]]()
_<p align="center">Checking stores closeby</p>_

[![Product Name Screen Shot][product-screenshot-4]]()
_<p align="center">Simple query (kuala lumpur)</p>_

[![Product Name Screen Shot][product-screenshot-5]]()
_<p align="center">Complex query</p>_

[![Product Name Screen Shot][product-screenshot-6]]()
_<p align="center">Another complex query</p>_

_For more examples, please refer to the [Documentation]() <- NON-EXISTENT FOR NOW_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Implement more complex query types
- [ ] Integrate LLM (GPT, huggingface models)

See the [open issues](https://github.com/MeorIdlan/subway-surf/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



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

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Meor Idlan Shafiq - meoridlans97w@gmail.com

Project Link: [https://github.com/MeorIdlan/subway-surf](https://github.com/MeorIdlan/subway-surf)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* The dudes at [stackoverflow](https://stackoverflow.com)
    
    Thank you for answering my obscure questions, stackoverflow posts from 10 years ago 😭

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/MeorIdlan/subway-surf.svg?style=for-the-badge
[contributors-url]: https://github.com/MeorIdlan/subway-surf/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/MeorIdlan/subway-surf.svg?style=for-the-badge
[forks-url]: https://github.com/MeorIdlan/subway-surf/network/members
[stars-shield]: https://img.shields.io/github/stars/MeorIdlan/subway-surf.svg?style=for-the-badge
[stars-url]: https://github.com/MeorIdlan/subway-surf/stargazers
[issues-shield]: https://img.shields.io/github/issues/MeorIdlan/subway-surf.svg?style=for-the-badge
[issues-url]: https://github.com/MeorIdlan/subway-surf/issues
[license-shield]: https://img.shields.io/github/license/MeorIdlan/subway-surf.svg?style=for-the-badge
[license-url]: https://github.com/MeorIdlan/subway-surf/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/meor-idlan-shafiq
[product-screenshot]: images/samplerun.png
[product-screenshot-1]: images/1.png
[product-screenshot-2]: images/2.png
[product-screenshot-3]: images/3.png
[product-screenshot-4]: images/4.png
[product-screenshot-5]: images/5.png
[product-screenshot-6]: images/6.png
[Python-logo]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[HTML5]: https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white
[HTML5-url]: https://developer.mozilla.org/en-US/docs/Web/HTML
[CSS]: https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white
[CSS-url]: https://developer.mozilla.org/en-US/docs/Web/CSS
[JavaScript]: https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black
[JavaScript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript