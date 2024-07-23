import base64
import requests
import json
from config import API_KEY

def toBase64(imagePath):
    # Open the JPEG file.
    with open(imagePath.lstrip("file:///"), 'rb') as image_file:
        # Read the file.
        image_data = image_file.read()

        # Encode the binary data to base64.
        image_base64 = base64.b64encode(image_data)

        # Convert bytes to a string.
        image_base64_string = image_base64.decode('utf-8')

    #print(image_base64_string)
    return image_base64_string




# Function to encode the image
#def encode_image(image_path):
#  with open(image_path, "rb") as image_file:
#    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
#image_path = "path_to_your_image.jpg"

# Getting the base64 string
#base64_image = encode_image(image_path)

def callVisionBase64(prompt, image_path):
    base64_image = toBase64(image_path)

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json()['choices'][0]['message']['content'])
    output = response.json()['choices'][0]['message']['content']
    return output