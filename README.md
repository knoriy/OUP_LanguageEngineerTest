# OUP Language Engineer Test

This project is a set of tools for parsing and analysing linguistic data from a corpus. Pydantic models are used to ensure ensures strong type checking and validation, essential for maintaining data integrity in natural language processing tasks.

## Setup

To set up the project environment:

```bash
git clone https://github.com/knoriy/OUP_LanguageEngineerTest.git
cd OUP_LanguageEngineerTest
```
Ensure that you have Python 3.7+ installed on your system. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

The project can be run from the command line. Please ensure your corpus data is in a JSON format as specified in the sample input schema.

```bash
python oup_le_task.py /path/to/corpus.json
```

This will parse the file `corpus.json` and output the lemma analysis to a JSON file (`output.json`).

## Input Data Format

The expected input is a JSON file containing parsed sentences with tokens. Each token should have the following attributes:

- **text**: The surface form of the token.
- **lemma**: The lemma or base form of the token.
- **pos**: The part of speech tag.
- **feats**: Optional additional linguistic features.

Example:

```json
{
  "sentences": [
      {
      "sentence_text": "Example text",
      "tokens": [
        {
          "id": 1,
          "text": "Example",
          "lemma": "example",
          "pos": "NOUN",
          "feats": "Number=Sing"
        }
        // ... more tokens
      ]
    }
    // ... more sentences
  ]
}
```

## Deployment

This tool could be deployed on a server provided by cloud providor such as AWS or inhouse servers. In this instance we will discuss two approahced, containersised microservices and AWS Lambda service.


## Storage

## Docker

The application can be containerised using Docker, which simplifies deployment and scaling. Here is a basic guide on how to do this:

1. Dockerise the application:

    ```dockerfile
    # ./Dockerfile
    # Use an official Python runtime as a parent image
    FROM python:3.7-slim

    # Set the working directory in the container
    WORKDIR /app

    # Copy the current directory contents into the container at /usr/src/app
    COPY . .

    # Install any needed packages specified in requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt

    # Run service when the container launches
    CMD ["python", "./oup_le_task.py"]
    ```

2. Build Docker image

    ````bash
    docker build -t oup-le-test .
    ````

3. Run container

    ```bash
    docker run -it --rm --name running-corpus-analyzer corpus-data-analyzer
    ```

## AWS Lambda


## Access