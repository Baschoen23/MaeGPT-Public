import time
from openai import OpenAI
from config import API_KEY



client = OpenAI(api_key=API_KEY)


'''
file = client.files.create(
    file=open("C:\\Users\\basch\Desktop\Cristen School\history-education-pss-vietnam-stakes-transcription 1.pdf", "rb"),
    purpose='assistants'
)
'''

'''
file2 = client.files.create(
    file=open("C:\\Users\\basch\Desktop\Cristen School\history-education-pss-vietnam-stakes-transcription.pdf", "rb"),
    purpose='assistants'
)
'''

'''
assistant = client.beta.assistants.create(
    name="Expert Pair Programmer",
    instructions="You are a sarcastic but helpful programming expert, please refer to any programming documentation you have knowldge of including documents for retreival and your own training data. Write and run code to assist with your analysis.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o-mini",
    #file_ids=[file.id, file2.id]
)
'''



def assistant_message_create(prompt):
    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    # thread_messages = client.beta.threads.messages.list(str(thread.id))
    # print(thread_messages.data)

def assistant_thread_call():
        thread = client.beta.threads.create()

        assistant = client.beta.assistants.create(
            name="Expert Pair Programmer",
            instructions="You are a sarcastic but helpful programming expert, please refer to any programming documentation you have knowldge of including documents for retreival and your own training data. Write and run code to assist with your analysis.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4o-mini"
        )
            #file_ids=[file.id, file2.id]

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions="Your name is Mae. Please address the user as Brendan and answer the questions.",

        )

        while not run.status == "completed":
            try:
                run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
                )
                print(run.status)
            except Exception as e:
                print("Error: " + str(e))
            print("Done")

        run = client.beta.threads.runs.retrieve(
          thread_id=thread.id,
          run_id=run.id
        )

        #print(client.beta.threads.messages.list(thread_id=thread.id).data[0].content[0].text.value)
        return client.beta.threads.messages.list(thread_id=thread.id).data[0].content[0].text.value