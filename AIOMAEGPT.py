    #Add internet search funcionality
    ##search google
    ##return first result
    ##read first result
    ##return completion based off of first result contents + user input and GPT training


    # Add long term memory (associate name of conversation with session ID for internal long term memory instead of using my own DB?
    # Add voice funcionality (speech to text & text to speech)
    # Use gpt to create a name for convo based on convo history
    # Create regenerate response funcionality
    # Image functionality
    # Lock text box that displays conversations
    # Organize tkinter configurations into consistent code design rules


# Import Libraries
import openai
import gpt as gpt
import tkinter as tk
import asyncio
from asyncio import Future
from concurrent.futures import ThreadPoolExecutor
from config import API_KEY

executor = ThreadPoolExecutor(max_workers=1)

def conversation_call_async(prompt, nconversation):
    # This is a non-blocking version of send_prompt that runs in a separate thread.
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(executor, conversationCall, prompt, nconversation)
    future.add_done_callback(on_prompt_response)

def on_prompt_response(future):
    response = future.result()


# Global Variables
global wholeConversation
global conversation
global prompt
global nightModeButtonState

wholeConversation = []
conversation = []
prompt = []
nightModeButtonState = 1
conversation.append({'role': 'assistant', 'content': 'How may I help you?'})
slateGrey = 112, 128, 144
offWhite = 245, 245, 245

def clearTextBox():
    text.delete(1.0, tk.END)

def clearConversation():
    global conversation
    conversation = []
    ({'role': 'assistant', 'content': 'How may I help you?\n'})
    conversation.append({'empty': 'pair'})
    conversation.append({'role': 'assistant', 'content': 'How may I help you?\n'})
    chat_window.insert(tk.END, '\n>{0}: {1}\n____________\n'.format(conversation[1]['role'].strip(),
                                                                    conversation[-1]['content'].strip()))

def send_message():
    global prompt
    prompt = text.get(1.0, tk.END)
    return prompt

def conversationCall(prompt, nconversation):
    global wholeConversation
    nconversation.append({'role': 'user', 'content': prompt})
    chat_window.insert(tk.END, '\n>{0}: {1}\n____________\n'.format(nconversation[1]['role'].strip(),
                                                                    nconversation[-1]['content'].strip()))
    wholeConversation.append(
        '\n>{0}: {1}\n____________\n'.format(nconversation[1]['role'].strip(), nconversation[-1]['content'].strip()))
    gpt.ChatGPT_conversation(nconversation)
    # Append new message to chat window
    chat_window.insert(tk.END, '\n>{0}: {1}\n____________\n'.format(nconversation[0]['role'].strip(),
                                                                    nconversation[-1]['content'].strip()))
    wholeConversation.append(
        '\n>{0}: {1}\n____________\n'.format(nconversation[0]['role'].strip(), nconversation[-1]['content'].strip()))
    # Scroll chat window to the bottom
    chat_window.see(tk.END)


def get_input(fileObj):
    input_text = fileObj.get()
    print(input_text)
    return input_text


def save_file(entry_obj, conversation):
    newName = get_input(entry_obj)
    with open(newName + '.txt', 'w') as file:
        for line in conversation:
            file.write(line)
        file.close()

# Add
def print_conversation(conversation):
    nameWindow = tk.Tk()
    nameWindow.title("Save File Dialog")
    nameWindow.configure(bg='black', height=20, width=50, padx=10, pady=10)
    nameWindow.resizable(width=False, height=False)

    fileLabel = tk.Label(nameWindow, text="Please enter a name for your conversation:", bg='black', fg='white')
    fileLabel.grid(row=0, column=1)

    fileEntry = tk.Entry(nameWindow, width=50)
    fileEntry.grid(row=1, column=1)

    saveButton = tk.Button(nameWindow, text="Save", command=lambda: (save_file(fileEntry, conversation), nameWindow.destroy()))
    saveButton.configure(bg='white', fg='black', height=1, width=6, padx=0, pady=0)
    saveButton.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=0)


def flip_button(value):
    if value == 1:
        value = 0
        return value
    elif value == 0:
        value = 1
        return value


def toggleNightMode(buttonState):
    global nightModeButtonState
    if buttonState == 1:
        window.configure(bg='white')
        chat_window.configure(bg='slateGrey', fg='black', highlightbackground='black', highlightcolor='black')
        chatLabel.configure(bg='white', fg='black')
        text.configure(bg='white', fg='black', highlightbackground='blue', highlightcolor='blue')
        text_editor.configure(bg='white', fg='black', highlightbackground='blue', highlightcolor='blue')
        text_editor_organizer.configure(bg='slateGrey', highlightbackground='black', highlightcolor='black')
        text_editor_label.configure(bg='slateGrey', fg='black')
        formatBox.configure(bg='slateGrey', highlightthickness=1, highlightbackground='black', highlightcolor='black')
        send_button.configure(bg='white', fg='black')
        buttonGrid.configure(bg='slateGrey', highlightthickness=1, highlightbackground='black', highlightcolor='black')
        button1.configure(bg='white', fg='black')
        button2.configure(bg='white', fg='black')
        button3.configure(bg='white', fg='black')
        nightModeButton.configure(bg='black', fg='white', text=('Night Mode'))
        buttonState = flip_button(buttonState)
        print('Changed to light mode ' + str(buttonState))
    elif buttonState == 0:
        window.configure(bg='black')
        chat_window.configure(bg='black', fg='green', highlightbackground='grey', highlightcolor='grey')
        chatLabel.configure(bg='black', fg='white')
        text.configure(bg='slateGrey', fg='black', highlightbackground='purple', highlightcolor='purple')
        text_editor.configure(bg='slateGrey', fg='black', highlightbackground='purple', highlightcolor='purple')
        text_editor_organizer.configure(bg='black', highlightbackground='grey', highlightcolor='grey')
        text_editor_label.configure(bg='black', fg='white')
        formatBox.configure(bg='black', highlightbackground='grey', highlightcolor='grey', highlightthickness='1')
        send_button.configure(bg='black', fg='white')
        buttonGrid.configure(bg='black', highlightbackground='grey', highlightcolor='grey', highlightthickness='1')
        button1.configure(bg='black', fg='white')
        button2.configure(bg='black', fg='white')
        button3.configure(bg='black', fg='white')
        nightModeButton.configure(bg='white', fg='black', text=('Day Mode'))
        buttonState = flip_button(buttonState)
        print('Changed to dark mode ' + str(buttonState))
    nightModeButtonState = buttonState
    return nightModeButtonState


# Create a new window
window = tk.Tk()
window.title('Chatbot')
window.configure(bg='black')
window.configure(width=200, height=200)
window.resizable(width=True, height=True)


for i in range(2):
    counter = 3
    window.rowconfigure(i, weight=1)
    counter -= 1
window.columnconfigure(i, weight=1)


# Add a chat window
chat_window = tk.Text(window, state='normal', height=25, width=80, padx=10, pady=10, bg='black', wrap=tk.WORD)
chat_window.configure(bg='black', fg='green', highlightthickness=3, highlightbackground='grey', highlightcolor='green', cursor="arrow")
chat_window.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
chat_window.insert(tk.END, '\n>{0}: {1}\n____________\n'.format(conversation[-1]['role'].strip(),
                                                                conversation[-1]['content'].strip()))
wholeConversation.append(
    '\n>{0}: {1}\n____________\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
chatLabel = tk.Label(window, text="_________ Welcome to MaezyGPT! _________")
chatLabel.configure(bg='black', fg='white', font=('Helvetica', 12, 'bold'))
chatLabel.grid(row=0, column=0, sticky='n')

text_editor_organizer = tk.Text(window, height=25, width=25, padx=10, pady=10, bg='black')
text_editor_organizer.configure(highlightthickness=3, highlightbackground='grey', highlightcolor='grey', cursor="arrow")
text_editor_organizer.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
text_editor_organizer.columnconfigure(0, weight=1)
text_editor = tk.Text(text_editor_organizer, height=25, width=25, padx=4, pady=2, bg='slateGrey', fg='black',
                      highlightthickness=1, highlightbackground='purple', highlightcolor='purple', wrap='word', cursor="plus")
text_editor.insert(tk.END, '\n')
text_editor.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
text_editor_label = tk.Label(text_editor_organizer, text='Text Editor')
text_editor_label.configure(bg='black', fg='white', font=('Times New Roman', 10, 'bold'))
text_editor_label.grid(row=0, column=0)


formatBox = tk.Text(window, height=10, width=55, padx=10, pady=5, bg='black', cursor="arrow")
formatBox.grid(row=3, column=0, padx=10, pady=10)


text = tk.Text(formatBox, height=3, width=50, padx=10, pady=10, bg='grey', wrap=tk.WORD, highlightthickness=1,
               highlightbackground="purple", highlightcolor="purple", cursor="plus")
text.configure(bg='slateGrey', fg='black', )
text.grid(row=1, column=0, padx=0, pady=1, sticky='sew')


send_button = tk.Button(formatBox, text="Send", command=lambda: (send_message(), conversation_call_async(prompt, conversation), clearTextBox()))
send_button.configure(height=2, width=5, bg='black', fg='white', cursor="hand2")
send_button.grid(row=1, column=2, padx=10, pady=10, ipadx=5, ipady=5, sticky='e')
send_button.bind('<1>', lambda event: send_message())


buttonGrid = tk.Text(window, height=2, width=30, padx=10, pady=5, bg='black', cursor="arrow")
buttonGrid.grid(row=2, column=0)


button1 = tk.Button(buttonGrid, text='Save')
button1.configure(height=1, width=25, padx=1, pady=1, bg='black', fg='white', cursor="hand2")
button1.configure(command=lambda: (print_conversation(wholeConversation)))
button1.grid(row=0, column=0, sticky='ew')


button2 = tk.Button(buttonGrid, text='Regenerate')
button2.configure(height=1, width=10, padx=10, pady=15, bg='black', fg='white', cursor="arrow",
                  command=lambda: (send_message(), conversationCall(prompt, conversation), clearTextBox()))
#button2.grid(row=0, column=1)

button3 = tk.Button(buttonGrid, text='Clear')
button3.configure(command=lambda: (chat_window.delete(1.0, tk.END)))  # clearConversation()))
button3.configure(height=1, width=25, padx=1, pady=1, bg='black', fg='white', cursor="hand2")
button3.grid(row=0, column=1, sticky='ew')

nightModeButton = tk.Button(window, text='Day Mode')
nightModeButton.configure(height=1, width=15, cursor="hand2", command=lambda: (toggleNightMode(nightModeButtonState)))
nightModeButton.grid(row=3, column=1, padx=20, pady=20, sticky='se')

# Start the main event loop for the window
window.mainloop()

banana = True
while banana:
    if prompt == 'bananas expired' or prompt == 'bananas gone bad' or prompt == 'bananas bad' or prompt == 'bananas rotten' or prompt == 'bananas moldy' or prompt == 'expired bananas':
        break