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


## Setting up the environment

In order to make the application work correctly, some environment variable are necessary.
They are defined in the following table:
| Name                      | Description                                                                                                                  |
|---------------------------|------------------------------------------------------------------------------------------------------------------------------|
| GOOGLE_CLIENT_ID          | The google cliend id used to validate the google login token                                                                 |
| HASH_ALGORITHM            | The hash algorithm to be used to encode the authorization token (Ex. `HS256`)                                                |
| HASH_SECRET_KEY           | The secret key used by the algorithm to encode the authorization token (Can be generated in cmd with `openssl rand -hex 32`) |
| AMAZON_EXTRACTOR_KEY      | Key defining the service amazon_data_extractor by RapidAPI                                                                   |
| AMAZON_EXTRACTOR_URL      | URL defining for accessing the service amazon_data_extractor by RapidAPI                                                     |
| RAPIDAPI_KEY              | Key for accessing services offered by RapidAPI                                                                               |
| BOOK_INFO_URL             | URL defining the service to get book additional information offered by openlibrary.org                                       |


## Documentation

The FastAPI framework automatically generates a documentation for the implemented endpoints.
Two openapi documentations are generated:
* A Swagger UI documentation at `/docs`
* A Redoc documentation at `/redoc`
