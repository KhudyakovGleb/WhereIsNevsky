# WhereIsNevsky


## Overview
This application is designed to process text input containing geographical information and return corresponding geocoded locations. The main functionality is powered by the `Geocoder` class, which utilizes NER models and OpenStreetMap (OSM) data for accurate address extraction and geocoding.

---

## Features

### Application Functionality
The application is built using **FastAPI** and exposes the following endpoints:

#### Endpoints

1. **`GET /`**
    - **Description**: Root endpoint providing a welcome message.
    - **Response**:
        ```json
        {
          "message": "Hello! Give me any text with geo subject and I will tell you where it is."
        }
        ```

2. **`GET /items`**
    - **Description**: Fetches a geocoded item's map visualization by its ID.
    - **Parameters**:
        - `item_id` (int): ID of the item to fetch.
    - **Response**:
        - Returns an interactive map (HTML response) for the specified item.
    - **Error Handling**:
        - Returns a `404` HTTP error if the item ID does not exist.

3. **`POST /items`**
    - **Description**: Processes the input text to extract geographical entities, geocodes them, and stores the result.
    - **Parameters**:
        - `text_ent` (str): Input text containing geographical information.
    - **Response**:
        - Returns an interactive map (HTML response) of the geocoded location.
    - **Process Flow**:
        1. The input text is wrapped in a DataFrame.
        2. The **Geocoder** class processes the text to extract geographical information using OSM data (defaulting to Saint Petersburg's OSM ID: `337422`).
        3. Geocoded results are appended to a global DataFrame (`data_df`).
        4. An interactive map with the geocoded results is returned.

### Additional Features
- **Interactive Maps**: Uses the `explore` method to provide interactive map visualizations.
- **Dynamic Data Storage**: Stores geocoded entries in a global DataFrame for easy retrieval.

---


## How to Run

### Running Locally
1. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
2. Start the application:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### Running with Docker
1. Build the Docker image:
   ```bash
   docker build -t geocoder-app .
   ```
2. Run the Docker container:
   ```bash
   docker run -p 8000:8000 geocoder-app
   ```

---

### System Requirements
- Python 3.11.5
- Docker (if running in a containerized environment)

---

## Future Enhancements
- Add a spellchecker for improved text input handling.
- Extend support for multiple languages and regions.
- Optimize map rendering for large datasets.

---

## Author
Developed with ❤️ by KhudyakovGleb.

