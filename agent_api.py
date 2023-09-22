from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import AgentTokenBufferMemory
from langchain.schema.messages import SystemMessage
from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import mysql.connector
import random
import string
import os
from flask import Flask,request, jsonify
from dotenv import load_dotenv
app = Flask(__name__)

"""# Create LLM and Embedding Model"""


load_dotenv()
apikey = os.getenv("API_KEY")

embeddings_openai = OpenAIEmbeddings(openai_api_key = apikey)

llm_openai = ChatOpenAI(openai_api_key = apikey,
                        temperature=0
                        )

"""# Import vector database"""

path = "./vector_database"

if os.path.exists(path):
  vector_store = FAISS.load_local(
      path,
      embeddings_openai
  )
else:
  print(f"Missing files. Upload index.faiss and index.pkl files to {path} directory first")

retriever = vector_store.as_retriever()

"""# Intiate mysql database"""

db_config = {
    'host': os.getenv("DATABASE_HOST"),      # Replace with your database host
    'user': os.getenv("DATABASE_USER"),       # Replace with your database username
    'password': os.getenv("DATABASE_PASSWORD"),  # Replace with your database password
    'database': os.getenv("DATABASE_NAME")   # Replace with your database name
}

def connect_to_database():
    return mysql.connector.connect(**db_config)

"""# Insert messages to database"""

def insert_agent_data(memory_key, human_text, ai_text):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = "INSERT INTO agent (memory_id, human, ai) VALUES (%s,%s,%s)"
    data = (memory_key, human_text, ai_text)
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    conn.close()

"""# Memory database retrieval"""

def retrieve_agent_memory(memory_id):
  conn = connect_to_database()
  cursor = conn.cursor()
  query = "SELECT human,ai FROM agent WHERE memory_id = %s"
  cursor.execute(query, (memory_id,))
  result = cursor.fetchall()
  cursor.close()
  conn.close()
  flattened_tuple = tuple(item for tup in result for item in tup)
  return flattened_tuple

"""# Memory adder to agent"""

def memory_adder(newagent, memory_tuple):
  for i in range (len(memory_tuple)):
    if i % 2 == 0:
      newagent.memory.chat_memory.add_user_message(memory_tuple[i])
    else:
      newagent.memory.chat_memory.add_ai_message(memory_tuple[i])

"""# Check if memory key exist in database"""

def count_msg_id(topic_id):

    connection = connect_to_database()
    cursor = connection.cursor()

    query = """
    SELECT COUNT(DISTINCT memory_id) AS memory_count
    FROM agent
    WHERE memory_id = %s;
    """
    cursor.execute(query, (topic_id,))
    result = cursor.fetchone()

    count_msg = result[0]

    cursor.close()
    connection.close()

    return count_msg

"""# Define tool"""

tool = create_retriever_tool(
    retriever,
    "search_about_telkom",
    "Always use this for every question for searching any context. Do Searches and returns sources of solution and product from Telkom.",
)
tools = [tool]

"""# Agent Prompt template version"""

system_message = SystemMessage(
    content=(
        """You are a "TelkomBot". A friendly bot helper for Telkom Indonesia.
        You can greet users "Hello, I am TelkomBot, do you question about Telkom Indonesia?".
        You have tool with name 'search_about_telkom' to find information about telkom with the sources.
        Your job is to provide information about the product or services of Telkom Indonesia.
        You can ask users what they need to know about Telkom Indonesia.
        Every question must be answer with tools. If answer not in tools, say "I'm sorry, i can not answer your question"
        You are not allowed to give information except information you have from available tools which is 'search_about_telkom'.
        If user ask you question or told you something outside of your job as bot helper for Telkom Indonesia product/services, refuse to answer.
        You respond in a short,informative, and in a very conversational friendly style."""

    )
)

def generate_random_topic_id(length=12):
    characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choice(characters) for _ in range(length))
    return random_id

def create_agent(bot_id):
  memory_key=bot_id
  memory = AgentTokenBufferMemory(memory_key=memory_key, llm=llm_openai)
  prompt = OpenAIFunctionsAgent.create_prompt(
          system_message=system_message,
          extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)]
      )
  agent = OpenAIFunctionsAgent(llm=llm_openai, tools=tools, prompt=prompt)
  agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True,
                                    return_intermediate_steps=True)
  return agent_executor

api_pass = os.getenv("API_PASS")

# restfulapi
@app.route('/telkom-bot/topic_id=<string:params>', methods=['POST'])
def engine(params):

  headers = request.headers
  auth = headers.get("x-api-key")

  data = request.json
  prompt = data.get('input')

  if auth == api_pass:

    count = count_msg_id(params)
    m_key = params
    if count > 0:
      
      agent_executor = create_agent(bot_id=m_key)
      
      memory_list = retrieve_agent_memory(m_key)
      memory_adder(agent_executor, memory_list)

      model_response = agent_executor({"input": f"{prompt}"})['output']
      response = {"output": model_response}
      
      insert_agent_data(m_key, prompt, model_response)

      return jsonify(response)
    
    else:
      agent_executor = create_agent(bot_id=m_key)

      model_response = agent_executor({"input": f"{prompt}"})['output']
      response = {"output": model_response}
      
      insert_agent_data(m_key, prompt, model_response)

      return jsonify(response)
    
  else:
    response = {"output":"ERROR: Unauthorized"}
    return jsonify(response)
    
app.run(port = 8080, host = '0.0.0.0')