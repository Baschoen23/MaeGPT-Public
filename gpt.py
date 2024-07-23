from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor
import config
from config import API_KEY
from instructions import assistantInstruct, adventureInstruct, codeBot, modelCompareInstruct
from instructions import achillesComparisonsWithHistoryInstruct, achillesComparisonsInstruct, \
    achillesEvaluateMemoriesInstruct, achillesFillInInstruct, achillesEvaluate, achillesEnterprisePrompts
from instructions import berylliumCompareInstruct, berylliumCompareInstructUpdate
from instructions import siaInstruct, siaPlus5Instruct, siaCodingMultiTurnInstruct, siaEvaluate3Instruct
from instructions import aiChatbotQualInstruct
from instructions import persephoneCompareInstruct
from instructions import andromedaCompareInstruct
from instructions import ravenCompareInstruct, ravenTalkToAChatbot
from instructions import akiraInstruct
from instructions import heraInstruct, heraInstruct7Dimension, heraInstruct10Dimension
from instructions import cesiumInstruct
from instructions import puffinInstruct
from instructions import resumeInstruct


#Asyncio executor thread definition
executor = ThreadPoolExecutor(max_workers=1)

# Global variables
conversation = []
prompt = ""


model1 = achillesComparisonsInstruct
model2 = achillesComparisonsWithHistoryInstruct
model3 = achillesEnterprisePrompts
model4 = achillesEvaluate
model5 = achillesEvaluateMemoriesInstruct
model6 = achillesFillInInstruct
model7 = aiChatbotQualInstruct
model8 = akiraInstruct
model9 = andromedaCompareInstruct
model10 = assistantInstruct
model11 = berylliumCompareInstruct
model12 = berylliumCompareInstructUpdate
model13 = cesiumInstruct
model14 = codeBot
model15 = puffinInstruct
model16 = modelCompareInstruct
model17 = persephoneCompareInstruct
model18 = ravenCompareInstruct
model19 = ravenTalkToAChatbot
model20 = siaCodingMultiTurnInstruct
model21 = siaEvaluate3Instruct
model22 = siaInstruct
model23 = siaPlus5Instruct
model24 = heraInstruct
model25 = heraInstruct7Dimension
model26 = heraInstruct10Dimension
model27 = None
model28 = resumeInstruct

currentInstructions = model10

#model_id = "gpt-3.5-turbo"
#model_id = "gpt-4-1106-preview"
#model_id = "gpt-4-0125-preview"
model_id = "gpt-4o"

def get_prompt(prompt):
    conversation.append({'role': 'user', 'content': prompt})
    #print(conversation[1]['role'] + ":", conversation[-1]['content'])
    fullPrompt = {'role': 'user', 'content': prompt}
    return fullPrompt

def conversation_call(conversation):
    """
    Makes a call to the OpenAI API to generate a response to the given conversation.

    Args:
        conversation (dict): The conversation to generate a response for.

    Returns:
        response (dict): The response from the OpenAI API.
    """
    client = OpenAI(api_key=API_KEY)
    print("conversation_call started")

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": currentInstructions + "\n"}, conversation
            ]
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None