from streamlit_folium import st_folium
from locations.location_data import locations
import streamlit as st
import folium
import math
import random


# calculates distance based on haversine formula to find the distance between the user guess and location co-ordinates
# over the earths surface
def calculate_dist(guess_pos, location_pos):
    guess_lat = guess_pos[0]
    guess_lng = guess_pos[1]
    location_lat = location_pos[0]
    location_lng = location_pos[1]

    radius = 6372.8  # radius of earth
    pi = math.pi / 180

    a = 0.5 - math.cos((location_lat - guess_lat) * pi) / 2 + math.cos(guess_lat * pi) * \
        math.cos(location_lat * pi) * \
        (1 - math.cos((location_lng - guess_lng) * pi)) / 2
    distance = 2 * radius * math.asin(math.sqrt(a))
    return distance

# initialises session state at the start of a round
def initialise_session(location_order, round_num):
    st.session_state.pending_guess = None
    st.session_state.confirmed_guess = None
    st.session_state.map_center = [20, 0]
    st.session_state.zoom = 2
    round_location = location_order[round_num]
    st.session_state.location = locations[round_location]





# Initialise first game
if "pending_guess" not in st.session_state:
    st.session_state.game_over = False
    st.session_state.total_score = []
    # randomly shuffling location order so that 1) it's random everytime and 2) it avoids repeats
    st.session_state.round_num = 0
    st.session_state.location_order = list(range(len(locations)))
    random.shuffle(st.session_state.location_order)
    initialise_session(st.session_state.location_order,
                           st.session_state.round_num)

if st.session_state.game_over:
    # Results page
    st.title("Game Complete!")
    st.write(
        f"Total distance score: {sum(st.session_state.total_score):.2f} km")
    
    if st.button("Play Again?"):
        # deletes the existing initalisation 
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


else: 
    # Streamlit webpage
    st.title("GeoPythr", width="stretch")
    st.write("""
        Welcome to GeoPythr, an attempt at recreating GeoGuessr using Python.

        Like [Geoguessr](https://www.geoguessr.com/), the aim of this game is to get as close to the location shown below.

        Plot your guess on the map below.
    """)
    st.image(st.session_state.location["image"], width="stretch")

    # Build map
    map = folium.Map(location=st.session_state.map_center,
                    zoom_start=st.session_state.zoom, tiles="CartoDB Positron")

    # Add marker if there's a pending guess
    if st.session_state.pending_guess:
        folium.Marker(location=st.session_state.pending_guess).add_to(map)

    # Show actual location and line after confirmation
    if st.session_state.confirmed_guess:
        folium.Marker(
            location=[st.session_state.location["lat"],
                    st.session_state.location["lng"]],
            icon=folium.Icon(color="green", icon="glyphicon-star")).add_to(map)
        folium.PolyLine(
            locations=[st.session_state.confirmed_guess, [
                st.session_state.location["lat"], st.session_state.location["lng"]]],
            color="red",
            dash_array="10").add_to(map)

    # Render map
    map_data = st_folium(map, width=700, height=500)

    # handles user markers and post-confirming guesses
    if map_data.get("last_clicked") and not st.session_state.confirmed_guess:
        user_marker = map_data["last_clicked"]
        new_guess = [user_marker["lat"], user_marker["lng"]]

        # refreshes the map whenever a new unconfirmed guess is made
        if new_guess != st.session_state.pending_guess:
            st.session_state.pending_guess = new_guess
            st.session_state.map_center = new_guess
            st.session_state.zoom = map_data["zoom"]
            st.rerun()

    left_col, right_col = st.columns(2)

    # Confirm guess button
    with left_col:
        if st.button("Confirm Guess", width="stretch"):
            if st.session_state.pending_guess:
                st.session_state.confirmed_guess = st.session_state.pending_guess
                st.rerun()
            else:
                st.warning("Ensure you have first made a guess")

        # Show result and next round / see results button
        if st.session_state.confirmed_guess:
            distance = calculate_dist(st.session_state.confirmed_guess, [
                st.session_state.location["lat"], st.session_state.location["lng"]])
            st.session_state.total_score.append(distance)
            st.text(f"Your guess was {distance:.2f} km away")

            with right_col:
                if st.session_state.round_num == (len(locations) - 1): #accounting for zero indexing
                    if st.button("See Results", width="stretch"):
                        st.session_state.game_over = True
                        st.rerun()
                else:
                    if st.button("Next Round", width="stretch"):
                        st.session_state.round_num += 1
                        initialise_session(
                            st.session_state.location_order, st.session_state.round_num)
                        st.rerun()
