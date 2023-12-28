# JK-Owling-Backend
Service and Design Engineering 2023 Course Project

## Project details

This project contains the backend application for the project.
`FastAPI` framework was used as foundation of the project, and `Pydantic` models are implemented to map the models of the data.


## Running the project

To start the project, enter the src folder and run the following code:

```
uvicorn main:app --reload
```

With the reload parameter set, the server restarts automatically every time a file is changed.
The default port used is `8000`. In order to set a different port use the `--port` parameter:
```
uvicorn main:app --reload --port 8086
```


## Documentation

The FastAPI framework automatically generates a documentation for the implemented endpoints.
Two openapi documentations are generated:
* A Swagger UI documentation at `/docs`
* A Redoc documentation at `/redoc`
