## University API Server

This project will be used to create an API server with MYSQL Backend using the following tools:

- FastAPI
- SQLAlchemy (ORM)
- Pydantic (Dataparsing and Serialization)
- Docker-Compose (Running multiple containers)

## Database ERD

### Figure

![Diagram](docs/erd.png)

Use this [link](https://dbdiagram.io/d/672b3730e9daa85aca7ede61) to view online.

## Usage

### Run Locally [Requires Database Setup]

Follow the steps to setup this project.

Go to the Project Folder and run the command:

```
source env/bin/activate
```

Now go inside the `app` folder

```
cd app
```

Install the required packages.

```
pip install -r requirements.txt
```

Run the server locally:

```
fastapi dev main.py
```

### Run on containers

Inside the `app` folder. Run the following command:

```
docker-compose up --build
```

Expected Output:

```
fastapi_app  | INFO:     Started server process [1]
fastapi_app  | INFO:     Waiting for application startup.
fastapi_app  | INFO:     Application startup complete.
fastapi_app  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Now go to the following url to view the docs for the APIs:

```
http://localhost:8000/docs
```

To shut down the containers. Use the command:

```
docker-compose down
```

Sample Output:

```
[+] Running 3/3
 ✔ Container fastapi_app  Removed      0.0s
 ✔ Container mysql_db     Removed      0.0s
 ✔ Network app_default    Removed      0.1s
```

## Testing

Check the documents of the API routes and send requests using the swagger UI at the [doc](http://localhost:8000/docs) after running the server. Sample test data `.csv` files are located at `app/test/data`.

## Folder Structure

All the project code is in the `app` folder with following sub-folders acting as different python packages.

- **/controller** : It contains the all the logic of the functions that will interact with the database to perform CRUD operations.
- **/db** : It contains database related helper functions and variables.
- **/models** : It contains the database tables defined in the form of classes for ORM.
- **/routers** : It contains the definition of routes and their respective handler functions for FastAPI's app.
- **/schemas** : It contains the pydantic classes that will be used for data validation, parsing and serialization when interacting with the `controller` functions.
- **/test** : It contains the test data for the database and any utility function for testing will be added here [IF REQUIRED]
