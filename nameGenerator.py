from openai import OpenAI
from config import API_KEY


MODEL_ID = "gpt-4-1106-preview"
model_id = MODEL_ID


def generate_name(prompt):
    """
    Generates a succinct name for a prompt object using the OpenAI API.

    Args:
    prompt_object (dict): A dictionary containing the role and content of the prompt, e.g., {"role": "user", "content": "Example Content"}.
    api_key (str): The API key to authenticate with the OpenAI API.
    model_id (str): The identifier of the model to use for generating the name.

    Returns:
    str: The generated name for the prompt.
    """

    client = OpenAI(api_key=API_KEY)
    response = None

    # Use a while loop to continually request a messages for the API call

    while not response:
        try:
            # Construct messages for the API call and attempt to get a response from the OpenAI API

            response = client.chat.completions.create(
                model=model_id,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a friendly, helpful assistant. Please generate a succinct name for the conversation based on the following prompt.""",
                    },
                    prompt,
                ],
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    if response:
        return response.choices[0].message.content.strip()
