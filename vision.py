from openai import OpenAI
from visionBase64 import callVisionBase64
from config import API_KEY

client = OpenAI(api_key=API_KEY)

#image_url_2 =  s
#print(image_url_2)

def gptVisionCall(prompt, image_url):
    #print("gptVisionCall started")
    #image_url = image_url
    try:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        #print("gptVisionCall finished")
        #print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        #print(e)
        try:
           return callVisionBase64(prompt, image_url)
        except Exception as e:
            print(e)

#gptVisionCall("Please describe this photo", "C:\\Users\\basch\Desktop\Lord_Bishnu-Shesh_Narayan.JPG")


'''
response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What kind of trees are in the background of this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/8/87/Img-zle19vrzOHjhMrmO6q2WkFlW.png" #"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                    },
                },
            ],
        }
    ],
    max_tokens=300,
)

print(response.choices[0].message.content)'''