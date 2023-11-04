
<div align="center">

# OUP Language Engineer Test

![CI testing](https://github.com/knoriy/OUP_LanguageEngineerTest/workflows/OUP%20LE%20Test/badge.svg?branch=master&event=push)


</div>

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
python src/oup_le_task.py /path/to/corpus.json
```

This will parse the file `corpus.json` and output the lemma analysis to a JSON file (`output.json`).

## Tests

Ensure that everything is functiong as expected:

```bash
pytest src/
```

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
      "sentence_text": "2019 жылы 27 желтоқсанда Президент",
      "tokens": [
        {
          "id": "1",
          "text": "2019",
          "lemma": "2019",
          "pos": "NUM",
          "feats": "NumType=Ord",
        },
        // ... more tokens
      ]
    }
    // ... more sentences
  ]
}
```

## Deployment

This tool could be deployed on a server provided by cloud providor such as AWS or inhouse servers. In this instance we will discuss two approahced, containersised microservices and AWS's Lambda service.

Deploying this code would require additional changes to allows for ease of access utlaising tools such as Flask or FastAPI. I discuss some of these changes in the appropriate section below.

### Storage

### Serverless - AWS Lambda

A simple and faster solution is utalsing AWS Lambda service using the container approach below. or

### Docker

The application can be containerised using Docker, which simplifies deployment and scaling. Here is a basic guide on how to do this:

1. Create a webserver wrapper
    1.1 Modify your application to be served over a web server. I would recoment using FastAPI as it is fully compatable with Pydantic.
    1.2 Implement an API endpoint that will receive the corpus data through HTTP requests and return the analysis results.

2. Dockerise the application:

    ```dockerfile
    # ./Dockerfile
    # Using official python image as base for our image
    FROM python:3.7-slim
    # Set the working directory in the container
    WORKDIR /app
    # Copy the current directory contents into the container at /app
    COPY . /app
    # Install any needed packages specified in requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt
    # Command to run the application using Uvicorn
    CMD ["uvicorn", "oup_le_task:app", "--host", "0.0.0.0", "--port", "80"]
    ```

3. Build Docker image

    ````bash
    docker build -t oup-le-test .
    ````

4. Run container

    ```bash
    docker run -p 80:80 oup-le-test
    ```

    Both inhouse and cloud providers can be used to deploy this container.

### Continuous Integration/Continuous Deployment (CI/CD)

For automated deployment, one could set up a CI/CD pipeline using tools like GitHub Actions. The pipeline should:

- Build the Docker image.
- Run tests.
- Deploy the Docker image to the production environment.

Any push to the main branch of the repository will trigger this pipeline, ensuring that the latest version of the program is automatically deployed.
