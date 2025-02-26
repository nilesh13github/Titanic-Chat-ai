from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from agent import agent
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static files from the "static" folder
app.mount("/static", StaticFiles(directory="static"), name="static")

class Data(BaseModel):
    prompt: str

@app.post("/get_response")
def rsp(data: Data):
    response, graph_plotted_path = agent(data.prompt)

    if graph_plotted_path:
        # Extract the filename from the full path
        graph_filename = graph_plotted_path.split("/")[-1]
        return {"Assistant": response, "Graph": f"{graph_filename}"}
    else:
        return {"Assistant": response, "Graph": "Graph not generated"}

@app.get("/get_graph/{image_name}")
def get_graph(image_name: str):
    file_path = f"./static/{image_name}"  # Directly fetch the image from static
    return FileResponse(file_path, media_type="image/png")
