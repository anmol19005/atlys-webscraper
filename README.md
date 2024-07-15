# atlys-webscraper

This project is a web scraping tool built using the FastAPI framework. 
The tool is designed to scrape product information (product name, price, and image) from the [Dental Stall website](https://dentalstall.com/shop/) and store the data locally. 

## Features

- Scrape product name, price, and image from the specified number of pages.
- Support for HTTP and HTTPS proxies.
- Store scraped data in a local JSON file.
- Simple authentication using a static token.
- Notification of scraping status.
- Caching mechanism using Redis to avoid unnecessary updates.


## Requirements

- Python 3.7+
- FastAPI
- requests
- beautifulsoup4
- pydantic
- uvicorn
- redis

## Installation

  1. Clone the repository:
  
     git clone https://github.com/yourusername/web-scraping-tool.git
     cd web-scraping-tool
  
  2. Create a virtual environment and activate it:
     python -m venv venv
     source venv/bin/activate
     
  3. pip install -r requirements.txt


## Usage

### 1. Start the FastAPI server:

    uvicorn main:app --reload

### 2. Send a POST request to the /scrape endpoint with the desired settings.

  Example using curl:

    curl --location --request POST 'http://localhost:8000/scrape' \
    --header 'Authorization: Bearer atlys_api_token' \
    --header 'Content-Type: application/json' \
    --data '{
        "pages": "2"
        }'

  Example using curl with proxy settings:

    curl --location --request POST 'http://localhost:8000/scrape' \
    --header 'Authorization: Bearer atlys_api_token' \
    --header 'Content-Type: application/json' \
    --data '{
        "pages": "2",
         "proxy": "http://yourproxy:port"
        }'



## API

### /scrape [POST]
  
    Request
    Headers:
      Authorization: atlys_api_token
      Content-Type: application/json
    Body:
      pages (int): Number of pages to scrape.
      proxy (Optional[str]): proxy URL.
    
    Response
    200 OK:
    status (str): "success"
    scraped_count (int): Number of products scraped.
    updated_count (int): Number of products updated.


## Authentication
  The API uses a static token for simple authentication. Update the API_TOKEN in the main.py file with your own token.

## Caching
  The scraper uses Redis for caching to avoid unnecessary updates to the database.
      
  ### To Start Redis Server
    redis-server
  ### To run cli
    redis-cli

  ### To list keys - keys * (if working on db 0)

  <img width="977" alt="image" src="https://github.com/user-attachments/assets/4668b112-c4b7-4b29-bec7-77627e43948a">
  
  ### To get price - get "key name"
  <img width="962" alt="image" src="https://github.com/user-attachments/assets/f59e751e-b19c-4f7e-a360-cdc43d4c63be">


  



