import openai
import asyncio
from config import API_KEY




'''
def image_gen(prompt):
  try:
    myImage = openai.Image.create(
      prompt=prompt,
      n=2,
      size="1024x1024",
    )

    imageLinks = [image['url'] for image in myImage['data']]
    print(imageLinks)

  except Exception as e:
    print(f"Error in image_gen: {e}")

image_gen('a white siamese cat')
'''

def image_gen(prompt):
  try:
    print("image_gen started")

    myImage = openai.Image.create(
      prompt=prompt,
      n=2,
      size="1024x1024",
    )
    '''
    from openai import OpenAI
    client = OpenAI(api_key=API_KEY)

    myImage = client.images.generate(
      model="dall-e-3",
      prompt="a white siamese cat",
      size="1024x1024",
      quality="standard",
      n=1,
    )

    image_url = myImage.data[0].url
    print("image_gen finished")
    print(image_url)
    '''

    imageLinks = []
    imageLinks.append(list(myImage['data'][0].values())[0])
    imageLinks.append(list(myImage['data'][1].values())[0])
    #print(imageLinks[0] + "\n" + imageLinks[1])

    print(imageLinks)

  except Exception as e:
    print(f"Error in image_gen: {e}")

image_gen('a white siamese cat')