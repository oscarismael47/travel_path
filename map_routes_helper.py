import os
import googlemaps
from dotenv import load_dotenv
import folium
from folium.plugins import AntPath, MarkerCluster

## load env variables
load_dotenv()

def get_map(origin, destination):
    """
    Generates a map with a route from the origin to the destination using Google Maps Directions API.

    Args:
        origin (str): The starting location for the route.
        destination (str): The ending location for the route.

    Returns:
        tuple: A tuple containing the HTML file path of the generated map, estimated duration, distance, and instructions.
    """
    # API Key for Google Maps Directions API
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    gmaps = googlemaps.Client(key=api_key)
    # Get directions
    directions_result = get_directions(gmaps, origin, destination)

    # Extract and print estimated time, distance, and instructions
    duration, distance, instructions, steps = extract_info(directions_result)

    # Center of the map (midpoint between start and end points)
    start_location = directions_result[0]['legs'][0]['start_location']
    end_location = directions_result[0]['legs'][0]['end_location']
    midpoint_lat = (start_location['lat'] + end_location['lat']) / 2
    midpoint_lng = (start_location['lng'] + end_location['lng']) / 2

    # Create a Folium map
    folium_map = folium.Map(location=[midpoint_lat, midpoint_lng], zoom_start=6)

    # Add markers for origin and final destination
    folium.Marker([start_location['lat'], start_location['lng']], popup="Start: " + origin, icon=folium.Icon(color="green")).add_to(folium_map)
    folium.Marker([end_location['lat'], end_location['lng']], popup="End: " + destination, icon=folium.Icon(color="red")).add_to(folium_map)

    # Plot the route on the map and add markers for each instruction
    plot_route(folium_map, directions_result, steps)

    # Add traffic layer
    
    folium.TileLayer('cartodbdark_matter', attr='Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(folium_map)
    folium.TileLayer('cartodbpositron', attr='Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(folium_map)
    #folium.TileLayer('stamenterrain', attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(folium_map)
    #folium.TileLayer('stamentoner', attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(folium_map)
    #folium.TileLayer('stamenwatercolor', attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(folium_map)
    folium.LayerControl().add_to(folium_map)

    # Save map to an HTML file
    html_file = "map.html"
    folium_map.save(html_file)
    #print("Map has been generated and saved as 'map.html'.")

    # Open the HTML file in the default web browser
    #webbrowser.open(html_file)

    return html_file, duration, distance, instructions

def get_directions(gmaps, start, end):
    """
    Retrieves directions from the Google Maps Directions API.

    Args:
        gmaps (googlemaps.Client): The Google Maps client.
        start (str): The starting location for the route.
        end (str): The ending location for the route.

    Returns:
        list: A list of directions results.
    """
    directions_result = gmaps.directions(start, end, mode="driving", departure_time="now")
    return directions_result

def extract_info(directions_result):
    """
    Extracts information such as duration, distance, and instructions from the directions result.

    Args:
        directions_result (list): The directions result from the Google Maps Directions API.

    Returns:
        tuple: A tuple containing the duration, distance, instructions, and steps.
    """
    leg = directions_result[0]['legs'][0]
    duration = leg['duration']['text']    
    distance = leg['distance']['text']
    instructions = []
    steps = []
    for step in leg['steps']:
        instruction = step['html_instructions']
        instructions.append(instruction)
        steps.append(step)
    return duration, distance, instructions, steps

def plot_route(folium_map, directions_result, steps):
    """
    Plots the route on the Folium map and adds markers for each instruction.

    Args:
        folium_map (folium.Map): The Folium map object.
        directions_result (list): The directions result from the Google Maps Directions API.
        steps (list): The steps of the route.
    """
    route_points = []
    marker_cluster = MarkerCluster().add_to(folium_map)
    for step in steps:
        polyline = step['polyline']['points']
        points = decode_polyline(polyline)
        route_points.extend(points)
        
        # Add marker for each instruction
        start_location = step['start_location']
        folium.Marker([start_location['lat'], start_location['lng']], popup=step['html_instructions'], icon=folium.Icon(color="blue")).add_to(marker_cluster)
    
    # Add animated line for the main route
    AntPath(route_points, color="blue", weight=2.5, opacity=1).add_to(folium_map)

def decode_polyline(polyline_str):
    """
    Decodes a polyline that is encoded using the Google Maps method.

    Args:
        polyline_str (str): The encoded polyline string.

    Returns:
        list: A list of tuples representing the decoded latitude and longitude coordinates.
    """
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}

    while index < len(polyline_str):
        for key in changes.keys():
            shift, result = 0, 0

            while True:
                byte = ord(polyline_str[index]) - 63
                index += 1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break

            if (result & 1):
                changes[key] = ~(result >> 1)
            else:
                changes[key] = (result >> 1)

        lat += changes['latitude']
        lng += changes['longitude']
        coordinates.append((lat / 1e5, lng / 1e5))

    return coordinates

if __name__ == "__main__":
    origin = "Chiapas, mexico"
    destination = "Tijuana"
    html_file, duration, distance, instructions = get_map(origin, destination)
    print(f"Estimated time: {duration}")
    print(f"Estimated distance: {distance}")
    print("Instructions:")
    for instruction in instructions:
        print(instruction)