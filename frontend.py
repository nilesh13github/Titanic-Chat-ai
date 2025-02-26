import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# User input
prompt = st.chat_input("Ask Titanic Chat")

if prompt:
    # Display user message
    with st.chat_message("human"):
        st.write(prompt)

    # Get response from the backend
    response = requests.post("http://0.0.0.0:8000/get_response", json={"prompt": prompt})

    # Display assistant response
    if response.status_code == 200:
        result = response.json()

        # Display assistant text response
        if "Assistant" in result:
            with st.chat_message("assistant"):
                st.write(result["Assistant"])

        # Check if there is a graph
        if "Graph" in result and result["Graph"] != "Graph not generated":
            graph_url = f"http://0.0.0.0:8000/static/{result['Graph']}"  # Construct the full graph URL
            graph_response = requests.get(graph_url)

            if graph_response.status_code == 200:
                graph_img = Image.open(BytesIO(graph_response.content))
                st.image(graph_img, caption="Generated Graph", use_container_width=True)
            else:
                st.error("Graph image not found on the server.")
    else:
        st.error("Failed to get a response from the server.")
