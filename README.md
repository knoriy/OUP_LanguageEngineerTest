
<div align="center">

# 🛠️📚 OUP Language Engineer Test 📚🛠️

[![OUP LE Test](https://github.com/knoriy/OUP_LanguageEngineerTest/actions/workflows/ci-testing.yml/badge.svg)](https://github.com/knoriy/OUP_LanguageEngineerTest/actions/workflows/ci-testing.yml)


</div>

This project is a set of tools for parsing and analysing linguistic data from a corpus. Pydantic models ensure strong type checking and validation, which is essential for maintaining data integrity in natural language processing tasks.

## 🚀 Setup

To set up the project environment, clone this repository and navigate into it:

```bash
git clone https://github.com/knoriy/OUP_LanguageEngineerTest.git
cd OUP_LanguageEngineerTest
```

Ensure that you have Python 3.7+ installed on your system. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

## 🧑‍💻 Usage

The project can be run from the command line. Please ensure your corpus data is in a JSON format as specified in the sample input schema.

```bash
python src/oup_le_task.py /path/to/corpus.json
```

This will parse the file `corpus.json` and output the lemma analysis to a JSON file (`output.json`).

## 🧪 Tests

Ensure that everything is functioning as expected:

```bash
pytest src/
```

## 📄 Input Data Format

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

## 🌐 Deployment

This tool could be deployed on a server provided by a cloud provider such as AWS or in-house servers. In this instance, we will discuss two approaches: containerised microservices and AWS's Lambda service.

Deploying this code would require additional changes to allow for ease of access utilising tools such as Flask or FastAPI. I discuss some of these changes in the appropriate section below.

### Serverless - AWS Lambda

In this instance, we will utilise AWS lambda, an efficient and scaleable solution within the AWS ecosystem. We use both Docker containers or package our code for execution. To do so, we must configure our Lambda function and set up any triggers, such as Amazon S3 events or HTTP endpoints, through Amazon API Gateway.

```python
# oup_lambda_handler.py
def lambda_handler(event, context):
    try:
        corpus_data = event.get('corpus_data')
        lemmas_dict = get_lemmas(corpus_data)
        return {
            'statusCode': 200,
            'body': json.dumps(lemmas_dict, ensure_ascii=False, indent=2)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

#### 🌟 Benefits of AWS Lambda

- **Scalability**: AWS Lambda automatically scales your application by running code in response to each trigger; it can handle a few daily requests to thousands per second.
- **Cost-Effective**: You pay only for the compute time you consume, which makes it cost-effective for applications with variable usage.
- **Event-Driven**: It integrates with AWS services to run code in response to events, such as file uploads to S3 or HTTP requests via API Gateway.
- **Serverless**: No servers to manage as AWS handles the infrastructure, which means less operational overhead.

### 🐳 Docker

The application can also be containerised using Docker, which simplifies deployment and improves reproducibility:

Note: If we use an in-house server, we must create a webserver wrapper.
    1. Modify your application to be served over a web server. I would recommend using FastAPI as it is fully compatible with Pydantic.
    2. Implement an API endpoint to receive the corpus data through HTTP requests and return the analysed results.

Dockerise the application:

```dockerfile
# ./Dockerfile
# Using official python image as the base for our image
FROM python:3.7-slim
WORKDIR /app
# Copy scripts into the container at /app
COPY src/ /app
# Copy and install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

CMD ["oup_lambda_handler.lambda_handler"]
```

#### 🌟 Benefits of Using Docker with AWS Lambda

- **Consistent Environment**: Your Lambda function runs in the same environment locally and in the cloud, reducing the "it works on my machine" problem.
- **Complex Dependencies**: If your application requires complex dependencies or specific versions of system libraries, a Docker container can encapsulate all of these.
- **Custom Runtimes**: Docker allows you to use runtimes not natively supported by AWS Lambda through custom images.

### Continuous Integration/Continuous Deployment (CI/CD)

For automated deployment, one could set up a CI/CD pipeline using tools like GitHub Actions. The pipeline should:

- Build the Docker image.
- Run tests.
- Deploy the Docker image to the production environment.

Any push to the main branch of the repository will trigger this pipeline, ensuring that the latest version of the program is automatically deployed.
