# The Telkom Assistant Bot Wtih GPT-3.5 Large Language Model (LLM) 

## Project Description
This project aims to create an assistant bot that leverages the large language model GPT-3.5 (Large Language Model) to provide information about Telkom based on data from the telkom.co.id website. This bot will be deployed as a REST API with the ability to store user and bot conversations in a MySQL database.

##  Implementation Steps
Here are the implementation steps for this project:

**1. Understanding GPT-3.5 LLM:**
This project utilizes the GPT-3.5-turbo language model accessed through the OpenAI API.

**2. Integration with Telkom.co.id Data:**
Web scraping from the telkom.co.id website using the BeautifulSoup web scraping library.

**3. Development of Assistant Bot:**
The LangChain library is used to create an LLM assistant capable of answering user questions based on data fetched from telkom.co.id.

**4. Deployment as a REST API:**
Deploy the assistant bot as a REST API using the Flask framework.

**5. MySQL Database:**
A MySQL database is used to store user and bot conversations.

**6. topic_id Parameter:**
The API has a topic_id parameter used to identify user and bot conversations. This parameter also serves to allow users to continue previous conversations.

## How to use API (Python)
```
import requests

# your prompt
prompt = "hello"

data = data = {'input': prompt}

# topic_id should be something random
topic_id = 'fnf87dqbfof'

# API url
url = f"https://telkomsite-engine-2uittvl6zq-as.a.run.app/telkom-bot/topic_id={topic_id}"

# request to api
response = requests.post(url, json=data)
# print(response)
response_dict = response.json()
model_response = response_dict['output']

print(model_response)
```

> The current state of the RestAPI lacks password protection, and there is a possibility that it will be password protected in the future.

## Getting Started
Web App: [https://telkombot.maulayaradhibilla.com/](https://telkombot.maulayaradhibilla.com/)

Web Repostiory: [https://github.com/Billl-11/TelkomSites-Bot](https://github.com/Billl-11/TelkomSites-Bot)
