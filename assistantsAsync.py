import asyncio
from openai import OpenAI
from config import API_KEY

client = OpenAI(api_key=API_KEY)

# Create the assistant synchronously
assistant = client.beta.assistants.create(
    name="Intune Assistant",
    instructions="You are a Microsoft Intune support agent. Write and run code to answer questions about Microsoft Intune.",
    model="gpt-4-1106-preview"
        #tools=[{"type": "code_interpreter"}]
)

async def assistantTest():
    loop = asyncio.get_running_loop()

    thread = await loop.run_in_executor(None, client.beta.threads.create)

    message = await loop.run_in_executor(None, lambda: client.beta.threads.messages.create(
        thread_id=thread.id,
        role='user',
        content="How do I enroll a device?",
    ))

    run = await loop.run_in_executor(None, lambda: client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as Lord Galaxy and answer the questions.",
    ))

    run = await loop.run_in_executor(None, lambda: client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    ))

    messages = await loop.run_in_executor(None, lambda: client.beta.threads.messages.list(
        thread_id=thread.id
    ))

    return messages

async def handle_assistant_call():
    print("handle_assistant_call started")
    response = await assistantTest()
    print(response)

async def main():
    try:
        await handle_assistant_call()
    except Exception as e:
        print("Error: " + str(e))

# Run the main function in the asyncio event loop
asyncio.run(main())