from fastapi import FastAPI


# Create an instance of the FastAPI app
app = FastAPI()

# Define a simple route that responds with a welcome message
@app.get("/")
def read_root():
    return {"message": "Welcome to your FastAPI server!"}

# Define a route that takes a path parameter (e.g., name)
@app.get("/hello/{name}")
def read_item(name: str):
    return {"message": f"Hello, {name}!"}

