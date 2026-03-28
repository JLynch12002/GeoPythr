# GeoPythr
Welcome to GeoPythr, my capstone project for the Sigma Labs pre-work. GeoPythr is my attempt at recreating (a very basic version) of GeoGuessr. Like GeoGuessr, you are shown an image of a Google Street View location and, using either your geographical knowledge or gut-feeling, must attempt to mark the location on a map. The aim is to place your guess as closely as possible to the location's co-ordinates, but be warned that some locations will be very difficult to pinpoint (especially without the ability to move the camera around like in GeoGuessr). Therefore, to make it more fair, there is no time limit. 

This project primarily uses the Streamlit library to render the location image and interactive map on an internet browser, although GeoPythr will still run without an internet connection. Clicking the map will place a red marker, representing your guess. You are able to move your marker as many times as you like until you are confident with your guess, where you then must confirm the position by clicking the button below. The distance between the guess and location co-ordinates is calculated using the Haversine formula, which measures the distance between two points on Earth 'as the crow flies' (a.k.a. in a straight path irrespective of terrain/elevation).

After each round you are given the option to begin another. If you wish to end the game, in your terminal press <code>Control + c</code> to end the Streamlit server. 

## Set-up
In your terminal:

1. Clone the repository
```
git clone https://github.com/JLynch12002/GeoPythr.git
```

2. Create and activate a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```
(On Windows use <code>.venv\Scripts\activate</code> instead.)

3. Install the required dependencies
```
pip install -r requirements.txt
```
or 
```
pip3 install -r requirements.txt
```

4. Run GeoPythr
```
streamlit run GeoPythr.py
```
This will open a new tab in your internet browser with the game.

5. To exit GeoPythr, return to the terminal and press <code>Control + c</code> to end the Streamlit server. To deactivate the virtual environment, enter into the terminal
```
deactivate
```
