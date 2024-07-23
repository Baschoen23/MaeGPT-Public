import openai
from openai import OpenAI
from config import API_KEY
from gpt import get_prompt

'''
model_id = "gpt-4-0125-preview"
#model_id = "davinci-002"
conversation = get_prompt("I'm thinking about designing my database for long term memory storage for a chatbot. So I have three tables, names, convos, and ID's. Each of the name and convos table have key ID and the ID table has key Name. Basically the program will create a session doc with a key, name and ID. when I select a conversation in the chat interface Iwould like to be able to recall that conversation. Is my database schema good where I separate the names, convos and ID's or should each doc including all elements just be saved in a table called docs and then recalled with key: ID. Ultimately I will want to be able to recall from all documents at once like an ingest so if one is better for that let's go towards that")
#client = OpenAI(api_key=API_KEY)
def generate_name(prompt):
    client = OpenAI(api_key=API_KEY)
    openai.api_key = API_KEY
    print("Generating name")
    # print(conversation)
    response = None
    counter = 0
    max_iterations = 1
    while not response:
        try:
            response = openai.completions.create(
                model=model_id,
                messages= prompt
            )
            if response:
                print(response.choices[0].message.content.strip())
                return response.choices[0].message.content.strip()
        except Exception as e:
            print(e)
            break


print(generate_name(conversation))
'''




#model_id = "gpt-4-0125-preview"
model_id = "davinci-002"
prompt = "Please create a succinct chat title for the following prompt: \"I'm thinking about designing my database for long term memory storage for a chatbot. So I have three tables, names, convos, and ID's. Each of the name and convos table have key ID and the ID table has key Name. Basically the program will create a session doc with a key, name and ID. when I select a conversation in the chat interface Iwould like to be able to recall that conversation. Is my database schema good where I separate the names, convos and ID's or should each doc including all elements just be saved in a table called docs and then recalled with key: ID. Ultimately I will want to be able to recall from all documents at once like an ingest so if one is better for that let's go towards that\""
#client = OpenAI(api_key=API_KEY)
def generate_name(prompt):
    client = OpenAI(api_key=API_KEY)
    openai.api_key = API_KEY
    print("Generating name")
    # print(conversation)
    response = None
    counter = 0
    max_iterations = 1
    while not response:
        try:
            response = openai.completions.create(
                model=model_id,
                prompt=prompt,
                # You can include other parameters here as needed

            )
            if response:
                message_content = response.choices[0].text.strip()
                print(message_content)
                # You can return or process the message_content as needed
        except Exception as e:
            print(e)


print(generate_name(prompt))




davinciObject = {
  "model": "davinci-002",
  "prompt": "Translate the following English text to French: 'Hello, how are you?'",
  "temperature": 0.7,
  "max_tokens": 60,
  "top_p": 1.0,
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0
}


'''
    while not response:
        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": "You are a friendly, helpful assistant. Please generate a name for the conversation based on the following prompt."},
                    prompt
                ]
            )
        except Exception as e:
            print(e)
            # counter += 1
            # if counter >= max_iterations:
            # print('Reached maximum number of iterations.')
            break
        if response:
            # conversation.append(response.choices[0])
            print(response.choices[0].message.content.strip())
            return response.choices[0].message.content.strip()
'''

#print(generate_name(conversation))


#{"role": "user", "content": "I need a name for the conversation."},

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