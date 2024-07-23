import openai
from openai import OpenAI
from config import API_KEY



def image_gen_2(prompt):
  try:
    print("image_gen started")
    client = OpenAI(api_key=API_KEY)
        # Dall-e-2 call
    myImage_2 = client.images.generate(
      model="dall-e-2",
      prompt=prompt,
      size="1024x1024",
      quality="standard",
      n=2,
      )
    image_url_1, image_url_2 = myImage_2.data[0].url, myImage_2.data[1].url
    print(image_url_1, image_url_2)
    image_urls = [image_url_1, image_url_2]
    return image_urls

  except Exception as e:
    print(f"Error in image_gen: {e}")

def image_gen(prompt):
  try:
    print("image_gen started")

    client = OpenAI(api_key=API_KEY)

    myImage_3 = client.images.generate(
      model="dall-e-3",
      prompt=prompt,
      size="1024x1024",
      quality="standard",
      n=1
    )
    image_url = myImage_3.data[0].url
    print("image_gen finished")
    return image_url

  except Exception as e:
    print(f"Error in image_gen: {e}")




'''
    # Dall-e-2 call
    myImage_2 = client.images.generate(
      model="dall-e-2",
      prompt=prompt,
      size="1024x1024",
      quality="standard",
      n=2,
    )

    image_url_1, image_url_2 = myImage_2.data[0].url, myImage_2.data[1].url
    print(image_url_1, image_url_2)
    '''







'''
    # Depracated dall-e call
    myImage = openai.Image.create(
      prompt=prompt,
      n=2,
      size="1024x1024",
    )
    
    imageLinks = []
    imageLinks.append(list(myImage['data'][0].values())[0])
    imageLinks.append(list(myImage['data'][1].values())[0])
    #print(imageLinks[0] + "\n" + imageLinks[1])

    return imageLinks
    '''









'''
def on_prompt_response(future):
  response = future.result()
  return response
'''

'''
def image_gen_async():
  print("image_gen_async started")
  try:
    loop = asyncio.get_event_loop()
  except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
  print("loop started")
  future = asyncio.run(image_gen())
  print("future completed")
  return future
'''