# similar_words

## Overview
The Similar Words is a backend application that provides an API for querying similar words in the English language.
Two words are considered similar if one is a letter permutation of the other.

## Installation and Setup:
#### Clone the repository: git clone "<repository-url>"
#### Navigate to the project directory: cd "<project-directory>"
#### Make sure you have docker and docker compose on you system.
#### Set up environment variables by creating a .env file in the project directory and providing the required values:
- ROOT_PASSWORD=<root_password>
- DB_HOST=<host> 
- DB_USER=<user_name>
- DB_PASSWORD=<user_password>
- DB_DATABASE=<database_name>

#### create a docker network for the services and modify docker-compose.yaml in the networks sections.
$ docker network create <your_network_name>

#### Build the docker image and modify docker-compose.yaml in the web -> image section.
$ docker build -t <image_name_of_flask_app> .

## Run the project:
$ docker compose up -d

## API Endpoints
#### GET /api/v1/similar?word="<your-word>"
Returns all words in the dictionary in JSON format that have the same permutation as the provided word.
The word in the query is not included in the response.

#### POST /api/v1/add-word
Add a word to the dictionary.
The word should be added to the dictionary and be available for future queries.
The request body should be a JSON object as follows:
{
    "word":"<word to add>"
}

#### GET /api/v1/stats
return general statistics about the word querying(about the `/api/v1/similar` endpoint):
- Total number of words in the dictionary
- Total number of requests to the `/api/v1/similar` endpoint.


