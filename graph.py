import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib
import os
matplotlib.use('Agg')

def detect_graph_type(query):
    graph_types = {
        "line plot": ["line plot", "line graph", "trend"],
        "bar chart": ["bar chart", "bar graph"],
        "histogram": ["histogram", "distribution"],
        "scatter plot": ["scatter plot", "scatter graph"],
        "pie chart": ["pie chart", "proportion"],
    }

    detected_graphs = "None"
    query = query.lower()

    for graph, keywords in graph_types.items():
        if any(keyword in query for keyword in keywords):
            detected_graphs = graph

    return detected_graphs if detected_graphs else "No graph"




def graph_generator(graph_type, data, filename = "graph.png"):

    try:

        x_list = []
        y_list = []

        for x, y in data :
            if x != None and y != None:
                x_list.append(x)
                y_list.append(y)
    except Exception as e:
        print(f"{e} in the data:", data)

    if graph_type == "line plot":

        if sum(x_list) > sum(y_list):
            x_list, y_list = y_list, x_list

        plt.plot(x_list, y_list, marker='o')

    elif graph_type == "bar chart":

        if sum(x_list) > sum(y_list):
            x_list, y_list = y_list, x_list

        plt.bar(x_list, y_list)
        
    elif graph_type == "scatter plot":

        if sum(x_list) > sum(y_list):
            x_list, y_list = y_list, x_list

        plt.scatter(x_list, y_list)

    elif graph_type == "histogram":

        plt.hist(x_list, weights=y_list, edgecolor = 'black')

    elif graph_type == "pie chart":

        if sum(x_list) < sum(y_list):
            x_list, y_list = y_list, x_list

        plt.pie(x_list, labels=y_list)  

    else:

        print("No graph, returning None Value")

        return None
    
    static_dir = "static"
    os.makedirs(static_dir, exist_ok=True)  # Create the directory if it doesn't exist
    file_path = os.path.join(static_dir, filename)
    plt.savefig(file_path, format='png')
    plt.close()

    return file_path
