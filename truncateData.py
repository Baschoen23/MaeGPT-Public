import asyncio
from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient
from openai import OpenAI
from config import API_KEY

# Define the executor with a maximum of 1 worker
executor = ThreadPoolExecutor(max_workers=1)

# Define the model ID
model_id = "gpt-3.5-turbo"

# Define the API key
client = OpenAI(api_key=API_KEY)

# Define the global variables
conversation = []
prompt = ""

# Function to access the database and retrieve the conversation history
def access_db():
    # Create a MongoDB client
    client = MongoClient('localhost', 27017)
    # Access the database and collection
    db = client.MaeGPT
    collection = db.NewDBTest
    # Retrieve the conversation history
    data = collection.find()
    conversation_recall = []
    for block in data:
        for line in block['conversations']:
            conversation_recall.append(line)
    return conversation_recall




def get_prompt(conversation_history):
    prompt = ""
    for message in conversation_history:
        prompt += message["content"] + "\n"
    return {"role": "user", "content": prompt}

'''
# Original
# Function to get the prompt for the conversation
def get_prompt(prompt):
    # Append the user's prompt to the conversation
    conversation.append({'role': 'user', 'content': prompt})
    # Create a full prompt with the user's role and content
    full_prompt = {'role': 'user', 'content': prompt}
    return full_prompt
    '''

# Function to make the conversation call to the OpenAI API
def conversation_call():
    # Initialize the response variable
    response = None
    # Try to get a response from the OpenAI API
    while not response:
        try:
            # Make the conversation call
            response = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": "Your job is to truncate data. Please take the relevant parts of the following conversations, summarize and truncate the, and return the truncated data"},
                    get_prompt(access_db())
                ]
            )
        except Exception as e:
            # Print any exceptions that occur
            print(e)
            # Break out of the loop if an exception occurs
            break
    # Return the response
    return response

# Print the prompt and conversation call
print(get_prompt(access_db()))
print(conversation_call())




'''
def access_db():
    client = MongoClient('localhost', 27017)
    db = client.maegptConnected
    collection = db.NewDBTest
    data = collection.find()
    conversation_recall = []
    for block in data:
        for line in block['conversations']:
            conversation_recall.append(line['content'])
    return '\n'.join(conversation_recall)
    
    
def get_prompt(prompt):
    conversation.append({'role': 'user', 'content': prompt})
    full_prompt = {'role': 'user', 'content': {'type': 'text', 'value': prompt}}
    return full_prompt

'''








'''
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor
from config import API_KEY
from pymongo import MongoClient

#Asyncio executor thread definition
executor = ThreadPoolExecutor(max_workers=1)


#model_id = "gpt-4-1106-preview"
model_id = "gpt-4-0125-preview"
#model_id = "gpt-3.5-turbo-0125"
#model_id = "gpt-3.5-turbo-instruct"

# Global variables
conversation = []
prompt = ""

def access_db():
    print("Creating session doc")
    client = MongoClient('localhost', 27017)
    print("Client created")
    db = client.maegptConnected
    print("Db created")
    collection = db.NewDBTest
    data = collection.find()
    print("Collection accessed")
    conversationRecall = []
    for block in data:
        for line in block['conversations']:
            #print(line)
            conversationRecall.append(line)
    return conversationRecall

def get_prompt(prompt):
    conversation.append({'role': 'user', 'content': prompt})
    #print(conversation[1]['role'] + ":", conversation[-1]['content'])
    fullPrompt = {'role': 'user', 'content': prompt}
    return fullPrompt

def conversation_call():
    client = OpenAI(api_key=API_KEY)
    print("conversation_call started")
    #print(conversation)
    response = None
    counter = 0
    max_iterations = 1
    #print("conversation_call started")
    while not response:
        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": "Your job is to truncate data. Please take the relevant parts of the following conversations, summarize and truncate the, and return the truncaed data"},
                    get_prompt(access_db())
                ]
            )


        except Exception as e:
            print(e)
            #counter += 1
            #if counter >= max_iterations:
            #print('Reached maximum number of iterations.')
            break
        if response:
            #conversation.append(response.choices[0])
            return response

print(get_prompt(access_db()))
print(conversation_call())
'''

'''
            #print("Trying Response")
            response = openai.ChatCompletion.create(
                model=model_id,
                messages=conversation,
                temperature=0.5,
                max_tokens=1024,
                # n=1, #stop=None, #timeout=15, #frequency_penalty=0, #presence_penalty=0
            )
            '''