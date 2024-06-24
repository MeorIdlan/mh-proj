MindHive Assessment Project<br>
This project is web application that allows user to search for a Subway restaurant in Malaysia.<br>
The project is divided into two parts: the frontend and the API.<br>
The API or the backend is responsible for scraping data from the official Malaysia Subway website and allowing the frontend to request for restaurant locations based on user's queries.<br>
The frontend will allow the user to see each restaurants on a map.

Instructions on running backend:
1) Install Python 3.10 (create a venv if you'd like)
2) Install packages (requirements.txt soon)
3) Run redis server (requires WSL if on windows, https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-windows/)
4) Run command "python app.py" in directory (default port 5000)

Instructions on running frontend:
1) Install nodejs and npm (LTS)
2) Run npm install in /frontend/mh-webapp/ directory
3) Run npm start in same directory

TODO
1) frontend (query box)
2) better readme
