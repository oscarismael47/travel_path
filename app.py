# https://googlemaps.github.io/google-maps-services-python/docs/index.html
import streamlit as st
from datetime import datetime
import map_routes_helper 

st.set_page_config(layout="wide")
# Function to display the map
def main():
    st.title("Roadmap")
    
    # Sidebar for user input
    st.sidebar.header("User Input")
    origin_input = st.sidebar.text_input("Start Location", "Merida")
    destination_input = st.sidebar.text_input("End Location", "Guanajuato")
    
    
    # Button to generate map
    if st.sidebar.button("Generate Map"):
        # Request directions via public transit
        now = datetime.now()
      
        map_file, duration, distance, instructions = map_routes_helper.get_map(origin_input, destination_input)
        
        # Display distance and duration on the sidebar
        st.sidebar.write(f"Distance: {distance}")
        st.sidebar.write(f"Duration: {duration}")

        # Display instructions in a container
        st.sidebar.subheader("Instructions")
        instructions_html = "<br>".join(instructions)  # Join instructions with line breaks
        #st.sidebar.markdown(instructions_html, unsafe_allow_html=True)  # Display as HTML
        st.sidebar.markdown(f'<div style="max-height: 300px; overflow-y: scroll;">{instructions_html}</div>', unsafe_allow_html=True)  # Display as HTML
        
       
        with open(map_file, "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=800,width= 1400)

# Call the display function
if __name__ == "__main__":
    main()