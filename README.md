# Travel Path

**Travel Path** is an interactive web app built with [Streamlit](https://streamlit.io/) for generating and visualizing driving routes between two locations using the Google Maps Directions API. The app displays a dynamic map with the route, calculates estimated travel time and distance, and provides step-by-step driving instructions.

## Features

- **Interactive Map**: Visualize routes between any two locations.
- **Step-by-Step Instructions**: Detailed driving instructions in the sidebar.
- **Distance & Duration**: See estimated travel time and distance instantly.
- **Multiple Map Styles**: Switch between different map tile layers.
- **Clustered Markers**: Route steps are marked and clustered for clarity.

## Demo

![travel_path demo screenshot](demo.gif)  
*Example: Route from Merida to Guanajuato.*

## Getting Started

### Prerequisites

- Python 3.8+
- Google Maps Directions API key

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/travel_path.git
    cd travel_path
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**

    Create a `.env` file in the project root and add your Google Maps API key:
    ```
    GOOGLE_MAPS_API_KEY=your_api_key_here
    ```

### Running the App

```sh
streamlit run app.py
```
