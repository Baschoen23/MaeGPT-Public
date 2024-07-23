
try:
    import os
    import time
    import sys
    import random
    import datetime
    import openai
    import asyncio
    from concurrent.futures import ThreadPoolExecutor
    import qdarkstyle
    from bs4 import BeautifulSoup
    from functools import partial
    import pymongo
    from bson.objectid import ObjectId
    import bson
    import json

    from PyQt5.QtCore import Qt, pyqtBoundSignal, pyqtSignal, QObject, QEvent, QThread, QUrl, QTimer
    from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QInputDialog, QTextEdit, QDialog, QFileDialog
    from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QToolBar, QTextBrowser, QLineEdit, QMenuBar, QAction, QLabel
    from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush, QMovie, QTextCursor

    import config
    from config import API_KEY
    from gpt import conversation_call, get_prompt
    from textToSpeech import text_to_speech
    from vision import gptVisionCall
    from assistantsOpenAI import assistant_message_create
    from assistantsOpenAI import assistant_thread_call
    from speechToText import speech_to_text
    from imageGeneration import image_gen
    from imageGeneration import image_gen_2
    from dbAccess import save_to_db
    from dbAccess import create_session_doc
    from dbAccess import update_db
    from dbAccess import get_names_from_db
    from dbAccess import access_db
    from dbAccess import increment_conversation_count
    from stringGenerator import generate_string
    from recordAudio import audioRecorder
    #from testingChatResponses import save_instructions_handler, save_text_to_file
    #from nameGeneratorCompletionDavinci import generate_name

    class YourClass(QObject):
        update_word_signal = pyqtSignal(str)

        def __init__(self):
            super().__init__()
            self.update_word_signal.connect(self.updateWordByWord)


    with open("conversation.json", "w") as file:
        file.close()

    class CircularButton(QPushButton):
        def __init__(self, parent=None):
            super(CircularButton, self).__init__(parent)
            self.setStyleSheet('''QPushButton {
                            border-radius: 50%
                            }
                            ''')
            #QPushButton background-color: lightblue; border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; padding: 6px; color: black, {border-radius: 50%}") #%dpx; }" % (self.width() / 2))
            #self.setMinimumWidth(100)
            #self.setMinimumHeight(100)


    #background-color: lightblue;

    stylesheetMainButtons = """
    QPushButton {
        background-color: rgba(0, 175, 225, 1);
        background-color: lightblue;
        border-style: outset;
        border-width: 2px;
        border-radius: 20px;
        border-color: beige;
        font: bold 14px;
        padding: 6px;
        color: black;
        width: 50px;
        height: 40px;
    }
    
    QPushButton:pressed {
        background-color: rgba(150, 150, 150, .5)
        border-style: inset;
    }
    """
    ##add8e6;

    stylesheetToolbarButtons = """
    QPushButton {
        background-color: rgba(200, 210, 210, .5);
        border-style: outset;
        border-width: 2px;
        border-radius: 25px;
        border-color: beige;
        font: bold 14px;
        padding: 6px;
        color: black;
        width: 50px;
        height: 40px;
    }
    
    QPushButton:pressed {
        background-color: #add8e6;
        border-style: inset;
    }
    """

    buttonStyle = '''
            QPushButton{
            color: red;
            background-color:rgba(0, 0, 250, .5);
            }'''


    class InstructionsDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Input Instructions")

            layout = QVBoxLayout()

            # Text edit area
            self.text_edit = QTextEdit()
            layout.addWidget(self.text_edit)

            # Button layout (horizontal)
            button_layout = QHBoxLayout()

            # Save button
            save_button = QPushButton("Save")
            save_button.clicked.connect(self.save_instructions)
            button_layout.addWidget(save_button)

            # Cancel button
            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(self.close)  # Close the dialog
            button_layout.addWidget(cancel_button)

            layout.addLayout(button_layout)  # Add the button layout to the main layout
            self.setLayout(layout)

        def save_instructions(self):
            text = self.text_edit.toPlainText()
            file_name = "instructions.txt"
            with open(file_name, 'w') as f:
                f.write(text)
            self.close()


    '''
    class InstructionsDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Input Instructions")

            layout = QVBoxLayout()
            self.text_edit = QTextEdit()
            layout.addWidget(self.text_edit)

            save_button = QPushButton("Save")
            save_button.clicked.connect(self.save_instructions)
            layout.addWidget(save_button)

            self.setLayout(layout)

        def save_instructions(self):
            text = self.text_edit.toPlainText()
            file_name = "instructions.txt"  # Fixed filename
            with open(file_name, 'w') as f:
                f.write(text)
            self.close()
            '''




    class mainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.initUI()
            self.setWindowTitle("MaeGPT")


        def initUI(self):

            self.linkButtonFlipper = 0

            self.executor = ThreadPoolExecutor(max_workers=1)

            self.displayWindow = displayWindow()
            self.setCentralWidget(self.displayWindow)
            self.setGeometry(300, 100, 800, 700)
            self.mainToolbar = QToolBar("Main Toolbar")
            self.addToolBar(Qt.LeftToolBarArea, self.mainToolbar)
            self.mainToolbar.setMovable(False)

            self.historyButton = CircularButton("History")
            self.historyButton.clicked.connect(self.handle_history_button)
            self.historyButton.setStyleSheet(stylesheetToolbarButtons)

            self.linksButton = QPushButton("Links")
            self.linksButton.clicked.connect(self.handle_links_button)
            self.linksButton.setStyleSheet(stylesheetToolbarButtons)

            self.saveButton = QPushButton('Save', self)
            self.saveButton.clicked.connect(self.save_conversation)
            self.saveButton.setStyleSheet(stylesheetToolbarButtons)

            self.clearButton = QPushButton('Erase', self)
            self.clearButton.clicked.connect(self.clear_conversation)
            self.clearButton.setStyleSheet(stylesheetToolbarButtons)

            self.aioGptButton = QPushButton("AIOGPT")
            self.aioGptButton.clicked.connect(self.handle_aio_gpt_button)
            self.aioGptButton.setStyleSheet(stylesheetToolbarButtons)

            self.openAIKeyButton = QPushButton("Key")
            self.openAIKeyButton.clicked.connect(self.handle_open_ai_key_button)
            self.openAIKeyButton.setStyleSheet(stylesheetToolbarButtons)

            self.instructButton = QPushButton("Instruct")
            self.instructButton.clicked.connect(self.open_dialog)
            self.instructButton.setStyleSheet(stylesheetToolbarButtons)

            self.newSessionButton = QPushButton("Instruct")
            self.newSessionButton.clicked.connect(self.handle_new_session_button)
            self.newSessionButton.setStyleSheet(stylesheetToolbarButtons)

            self.mainToolbar.addWidget(self.historyButton)
            self.mainToolbar.addWidget(self.linksButton)
            self.mainToolbar.addWidget(self.saveButton)
            self.mainToolbar.addWidget(self.clearButton)
            self.mainToolbar.addWidget(self.openAIKeyButton)
            self.mainToolbar.addWidget(self.instructButton)
            # self.mainToolbar.addWidget(self.aioGptButton)

            '''
            self.historyList = []
            for doc in get_names_from_db():
                self.historyList.append(doc['name'])
            #print(self.historyList)
            '''

        def save_instructions_handler(self):  # Assuming this is within your main GUI class
            print("Save Instructions Button Clicked")
            # 1. Create the Dialog
            print("I'm here too")
            dialog = QDialog(self)
            print("Dialog Window Created")  # Make the dialog a child of your main window
            dialog.setWindowTitle("Input Instructions")

            print("Dialog Created")
            # 2. Layout for Text Input
            text_edit = QTextEdit(dialog)
            layout = QVBoxLayout(dialog)
            layout.addWidget(text_edit)

            print("Text Edit Created")
            # 3. Button for Saving and Closing
            save_button = QPushButton("Save & Close", dialog)
            layout.addWidget(save_button)

            print("Save Button Created")
            # 4. Dialog Display and Event Handling
            dialog.exec_()  # Show the dialog modally (blocks until closed)

            print("Dialog Executed")
            # Save to File when "Save & Close" is clicked
            save_button.clicked.connect(self.save_text_to_file(text_edit.toPlainText()))
            print("Instructions saved")

        def save_text_to_file(self, instructions_text):
            # Get file path from the user (optional)
            #file_path, _ = QFileDialog.getSaveFileName(self, "Save Instructions", "instructions.txt", "Text Files (*.txt)")
            file_path = "instructions.txt"
            print("Save Text to File Started")
            print(file_path)

            if file_path:  # User didn't cancel
                try:
                    with open(file_path, "w") as file:
                        file.write(instructions_text)
                except Exception as e:  # Catch potential errors
                    print(f"Error saving instructions: {e}")

        def open_dialog(self):
            dialog = InstructionsDialog()
            dialog.exec_()  # Show the dialog modally




        def save_conversation(self):
            #print(self.conversationBox.toPlainText())
            print('Save_conversation called')
            with open(str(datetime.datetime.now().strftime("%Y-%m-%d_[%H;%M;%Ss]-")) + 'MaeGPT-' + str(random.randint(1, 10000)) + ".txt",'w') as file:
                print('File Opened')
                file.write(self.displayWindow.conversationBox.toPlainText())
                html_content = self.displayWindow.linkBox.toHtml()
                file.write('\n' + 'Links:' + '\n')
                soup = BeautifulSoup(html_content, 'html.parser')
                for a in soup.find_all('a', href=True):
                    file.write(a['href'] + '\n')
                #file.write(self.linkBox.toHtml())
                print('File Written')

        def clear_conversation(self):
            self.displayWindow.conversationBox.clear()
            increment_conversation_count()

        def handle_links_button(self):
            if self.linkButtonFlipper == 0:
                self.displayWindow.linkBox.show()
                self.linkButtonFlipper = 1
            else:
                self.displayWindow.linkBox.hide()
                self.linkButtonFlipper = 0

        def handle_aio_gpt_button(self):
            #handle_aio_gpt_call()
            pass

        def handle_open_ai_key_button(self):
            try:
                api_key, ok = (QInputDialog.getText(self, "Input", 'Enter API Key'))  #, 'Input Dialog', 'Enter your API key:'))
                if ok and api_key:
                    openai.api_key = api_key
                    print(api_key)
                    config.API_KEY = api_key
                    with open('config.py', 'w') as config_file:
                        config_file.write(f"API_KEY = '{api_key}'")
            except Exception as e:
                self.displayWindow.conversationBox.append('Please set your API Key')

        def handle_history_button(self):
            if self.linkButtonFlipper == 0:
                self.displayWindow.historyBox.clear()
                for name in get_names_from_db():
                    self.displayWindow.historyBox.append(name + "\n")
                    self.displayWindow.historyBox.append("________________\n")
                self.displayWindow.historyBox.show()
                self.linkButtonFlipper = 1
            else:
                self.displayWindow.historyBox.hide()
                self.linkButtonFlipper = 0

        def handle_new_session_button(self):
            self.displayWindow.conversationBox.clear()




    class displayWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.initUI()
            self.executor = ThreadPoolExecutor(max_workers=4)
            self.visionButtonFlipper = 0
            self.session_id = generate_string()
            with open("session_id.txt", "a+") as file:
                file.writelines(self.session_id + "\n")
                file.close()
            #print(type(self.session_id))
            #print(self.session_id)
            self.dbCounter = 0
            self.prompt = ""

        def initUI(self):
            self.setGeometry(300, 300, 800, 600)
            self.setWindowTitle('Basic PyQt5 Window')

            self.sendButton = QPushButton('Send', self)
            self.sendButton.setStyleSheet(stylesheetMainButtons)
            self.sendButton.clicked.connect(self.send_message)

            self.voiceInputButton = QPushButton("Voice")
            self.voiceInputButton.setStyleSheet(stylesheetMainButtons)
            self.voiceInputButton.setCheckable(True)
            self.voiceInputButton.clicked.connect(self.handle_voice_input_button)

            self.visionInputButton = QPushButton("Vision")
            self.visionInputButton.setStyleSheet(stylesheetMainButtons)
            self.visionInputButton.clicked.connect(self.handle_vision_input_button)

            self.imageInputButton_2 = QPushButton("Dall-e-2")
            self.imageInputButton_2.setStyleSheet(stylesheetMainButtons)
            #self.imageInputButton_2.setStyleSheet("QPushButton{color: black}")
            self.imageInputButton_2.clicked.connect(self.handle_image_gen_button_2)

            self.imageInputButton = QPushButton("Dall-e-3")
            self.imageInputButton.setStyleSheet(stylesheetMainButtons)
            self.imageInputButton.clicked.connect(self.handle_image_gen_button)

            self.assistantInputButton = QPushButton("Ask Assistant")
            self.assistantInputButton.setStyleSheet(stylesheetMainButtons)
            self.assistantInputButton.clicked.connect(self.handle_assistant_input_button)

            self.conversationBox = QTextBrowser(self)
            self.conversationBox.setReadOnly(True)
            self.conversationBox.setAcceptRichText(True)
            self.conversationBox.setOpenExternalLinks(True)
            self.conversationBox.setOpenLinks(True)
            #self.conversationBox.append("Hi there! I'm Mae! What can I do for you?" + "\n ________________________________\n")
            self.conversationBox.append("Welcome to MaeGPT" + "\n________________________________\n")
            #text_to_speech("Hi there! I'm Mae! What can I do for you?")

            self.textEditor = QTextEdit(self)
            self.textEditor.setAcceptRichText(True)
            self.textEditor.setMinimumHeight(150)

            self.buttonLayout = QHBoxLayout()

            self.buttonLayout.addWidget(self.sendButton)
            self.buttonLayout.addWidget(self.voiceInputButton)
            self.buttonLayout.addWidget(self.visionInputButton)
            self.buttonLayout.addWidget(self.imageInputButton_2)
            self.buttonLayout.addWidget(self.imageInputButton)
            self.buttonLayout.addWidget(self.assistantInputButton)

            self.linkBox = QTextBrowser(self)
            self.linkBox.setGeometry(15, 15, 200, 300)
            self.linkBox.setReadOnly(True)
            self.linkBox.setOpenLinks(True)
            self.linkBox.setOpenExternalLinks(True)
            self.linkBox.hide()

            self.historyBox = QTextBrowser(self)
            self.historyBox.setGeometry(15, 15, 200, 300)
            self.historyBox.setReadOnly(True)
            self.historyBox.setOpenLinks(True)
            self.historyBox.setOpenExternalLinks(True)
            self.historyBox.hide()

            #self.imageURLBox = QInputDialog(self).getText(self, "Input", 'Enter Image URL')
            self.imageURLBox = QInputDialog(self)
            self.imageURLBox.setLabelText("Input or paste an image url: ")
            self.imageURLBox.setFixedSize(500, 100)
            self.imageURLBox.setOkButtonText("Submit")
            self.imageURLBox.hide()
            #self.imageURLBox.setGeometry(20, 20, 400, 100)
            #self.imageURLBox.setText('Please input an image url: ')
            #self.imageURLBox.setReadOnly(False)
            #self.imageURLBox.setOpenLinks(True)
            #self.imageURLBox.setOpenExternalLinks(True)


            self.mainLayout = QVBoxLayout()

            self.mainLayout.addWidget(self.conversationBox, 4)
            self.mainLayout.addWidget(self.textEditor, 1)
            self.mainLayout.addLayout(self.buttonLayout)

            self.setLayout(self.mainLayout)

            if self.textEditor.hasFocus() == True:
                self.input_box_focus()

        def send_message(self):
            """
            Sends a message to the AI assistant and updates the conversation box.
            """
            try:
                # Append the user's message to the conversation box
                self.conversationBox.append(self.textEditor.toPlainText())
                self.conversationBox.append("________________________________\n\n")

                # Create a JSON object with the user's message
                jsonData = {'content': self.textEditor.toPlainText()}

                # If this is the first message, create a new document in the database
                if self.dbCounter == 0:
                    create_session_doc(self.session_id, jsonData, get_prompt(self.textEditor.toPlainText()))
                    self.dbCounter += 1
                # Otherwise, update the existing document
                else:
                    update_db(self.session_id, jsonData)

                # Retrieve the conversation history from the database
                newData = access_db()
                instructionPrompt = ""

                # Create a prompt for the AI assistant by concatenating the conversation history
                for line in newData:
                    instructionPrompt += str(line) + "\n"

                # Submit the prompt to the AI assistant and handle the response
                future = self.executor.submit(conversation_call, get_prompt(instructionPrompt))
                future.add_done_callback(partial(self.handle_conversation_result))

                # Scroll to the bottom of the conversation box
                self.scrollBar = self.conversationBox.verticalScrollBar()
                self.scrollBar.setValue(self.scrollBar.maximum())

                # Clear the text editor
                self.textEditor.clear()
            except Exception as e:
                print(f"An error occurred: {e}")


        def perform_conversation_call_async(self, prompt):
            print("Conversation call async started")
            result = conversation_call(get_prompt(prompt))
            print("Result obtained")
            print(result)
            return result

        def updateWordByWord(self, word):
            """
            Updates the conversation box by appending the given word.

            Args:
                word (str): The word to append to the conversation box.
            """
            for char in word.split(" "):
                if char:
                    self.conversationBox.insertPlainText(char)
                    QApplication.processEvents()
                    time.sleep(0.009)
                elif not char:
                    self.conversationBox.insertPlainText(" ")
                    QApplication.processEvents()
                    time.sleep(0.009)
                else:
                    pass
            '''
            try:
                # Move the cursor to the end of the conversation box
                cursor = self.conversationBox.textCursor()
                cursor.movePosition(QTextCursor.End)
                self.conversationBox.setTextCursor(cursor)

                self.typing_timer = QTimer()
                self.typing_timer.setInterval(int(random.uniform(50, 100)))  # in milliseconds
                self.typing_timer.timeout.connect(self.insert_next_character)
                self.typing_timer.start()

                self.word_to_insert = list(word)

                #print("Word to insert: " + str(self.word_to_insert))
            except Exception as e:
                print(f"An error occurred: {e}")
                '''



        def insert_next_char(self):
            if self.word_list:
                self.conversationBox.insertPlainText(self.word_list.pop(0))
            else:
                self.timer.stop()
                # Scroll to the bottom of the conversation box
                self.conversationBox.verticalScrollBar().setValue(self.conversationBox.verticalScrollBar().maximum())


        def insert_next_character(self):
            if self.word_to_insert:
                # Insert the next character
                print(self.word_to_insert)
                self.conversationBox.insertPlainText(self.word_to_insert.pop(0))
            else:
                # Stop the timer when the word has been fully inserted
                self.typing_timer.stop()
                # Scroll to the bottom of the conversation box
                self.conversationBox.verticalScrollBar().setValue(self.conversationBox.verticalScrollBar().maximum())

        async def restart_event_loop(self):
            loop = asyncio.get_event_loop()

            # Cancel all running tasks
            tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
            for task in tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

            # Stop the current event loop
            loop.stop()

            # Create a new event loop
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            new_loop.create_task(main())
            new_loop.run_forever()


        def handle_conversation_result(self, future):
            try:
                print("Handle Conversation Result Started")

                response = future.result()
                print(response)
                data = response.choices[0].message.model_dump_json()
                print(data)
                jsonData = json.loads(data)

                if self.dbCounter == 0:
                    create_session_doc(self.session_id, jsonData, self.textEditor.toPlainText())
                    self.dbCounter += 1
                    print("Doc created")
                else:
                    update_db(self.session_id, jsonData)
                    print("Doc updated")

                plain_text_response = response.choices[0].message.content
                print(plain_text_response)
                self.conversationBox.append(plain_text_response + "\n_______________________________\n")

                #updates words
                '''
                for char in response.choices[0].message.content:
                    try:
                        self.updateWordByWord(char)
                        char = ''
                    except MemoryError:
                        print(
                            f"Memory error occurred while processing character '{char}'. Skipping to the next character.")
                    except Exception as e:
                        print(f"An error occurred: {e}")
                    #for char in word:
                    '''

                # Move the cursor to the end of the text box
                cursor = self.conversationBox.textCursor()
                cursor.movePosition(QTextCursor.End)
                self.conversationBox.setTextCursor(cursor)
            except Exception as e:
                print("An error occurred" + str(e))
                self.close()
                asyncio.run(main())
                QApplication.exit()

                #asyncio.run(self.restart_event_loop())

        def handle_voice_input_button(self):
            if self.voiceInputButton.isChecked():
                self.voiceInputButton.setStyleSheet("QPushButton { color: red}")
                self.voiceInputButton.setText("Recording")
                self.audioReturner = audioRecorder()
                self.future = self.executor.submit(speech_to_text, True,
                                                   self.audioReturner)  # , self.handle_voice_input_secondary)
            else:
                self.future = self.executor.submit(speech_to_text, False, self.audioReturner)

        def handle_voice_input_callback(self, future):
            self.voiceInputButton.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 175, 225, 1);
                background-color: lightblue;
                border-style: outset;
                border-width: 2px;
                border-radius: 20px;
                border-color: beige;
                font: bold 14px;
                padding: 6px;
                color: black;
                width: 50px;
                height: 40px;
            }

            QPushButton:pressed {
                background-color: rgba(150, 150, 150, .5)
                border-style: inset;
            }
            """)
            self.voiceInputButton.setText("Voice")
            if future.result() is not None:
                print(str(list)(future.result())[0][1])
                self.textEditor.append(str(list(future.result())[0][1]))

        def update_text_editor(self, future):
            self.textEditor.clear()
            self.textEditor.append(str(list(self.future.result())[1]))


        def append_voice_input_started(self):
            self.textEditor.append("Voice Input Started: Recording")

        def clear_text_editor(self):
            self.textEditor.clear()

        def handleVisionInputSecondary(self, future):
            #print("handleVisionInputSecondary started")
            #print(future.result())
            self.conversationBox.append(future.result() + "\n_______________________________\n")

        def handle_vision_input_button(self):
            # Create a QInputDialog to get the image URL from the user
            visionInputDialog = QInputDialog(self)
            visionInputDialog.setLabelText("Input or paste an image url: ")
            visionInputDialog.setFixedSize(500, 100)

            # Get the image URL from the user
            imageURL, ok = visionInputDialog.getText(self, 'Vision', 'Enter or paste an Image URL or Image File Path: ')

            # If the user clicks OK and enters a URL, proceed with the vision input
            if ok and imageURL:
                # Submit the vision input task to the executor
                future = self.executor.submit(gptVisionCall, self.textEditor.toPlainText(), imageURL)

                # Clear the text editor
                self.textEditor.clear()

                # Add a callback to handle the result of the vision input task
                future.add_done_callback(self.handleVisionInputSecondary)

        def handle_image_gen_button_2(self):
            print("Hello World")
            imagePrompt = self.textEditor.toPlainText()
            self.conversationBox.append("Image Gen Started with Dall-e-2: " + imagePrompt + "\n_______________________________\n")
            print(imagePrompt)
            future = self.executor.submit(image_gen_2, imagePrompt)
            self.update_text_editor()
            future.add_done_callback(self.image_gen_update_2)

        def handle_image_gen_button(self):
            imagePrompt = self.textEditor.toPlainText()
            self.conversationBox.append("Image Gen Started with Dall-e-3: " + imagePrompt + "\n_______________________________\n")
            print(imagePrompt)
            future = self.executor.submit(image_gen, imagePrompt)
            self.update_text_editor()
            future.add_done_callback(self.image_gen_update)



        def image_gen_update_2(self, future):
            print("image_gen_update started")
            try:
                # Handles Dall-e-2
                imageLinks = future.result()
                print("imageLinks Created")
                print(imageLinks)
                self.linkBox.append("<a href=\"" + imageLinks[0] + "\">Image 1</a>| <a href=\"" + imageLinks[1] + "\">Image 2</a>")  # + "<a href=\"" + self.imageLinks[2] + "\">Image 3</a>")
                self.conversationBox.append("Finished, check the links menu to view your image link! " + "\n ________________________________\n")
                self.linkBox.append(str("<br>______________<br>"))
            except Exception as e:
                print(f"Error during image generation: {e}")

        def image_gen_update(self, future):
            print("image_gen_update started")
            try:
                imageLink = future.result()
                self.linkBox.append("<a href=\"" + imageLink + "\">Image</a>")
                self.conversationBox.append("Finished, check the links menu to view your image links! " + "\n ________________________________\n")
                self.linkBox.append(("<br>______________<br>"))
            except Exception as e:
                print(f"Error during image generation: {e}")

        def handle_assistant_input_button(self):
            self.conversationBox.append(self.textEditor.toPlainText() + "\n_______________________________\n")
            assistant_message_create(self.textEditor.toPlainText())
            self.textEditor.clear()
            future = self.executor.submit(assistant_thread_call)
            future.add_done_callback(self.handle_assistant_input_callback)

        def handle_assistant_input_callback(self, future):
            self.conversationBox.append(future.result() + "\n_______________________________\n")


        def update_text_editor(self):
            self.textEditor.clear()



    async def main():
        app = QApplication(sys.argv)
        dark_stylesheet = qdarkstyle.load_stylesheet(qt_api='pyqt5')
        app.setStyleSheet(dark_stylesheet)
        window = mainWindow()
        window.show()
        sys.exit(app.exec_())
        #await asyncio.sleep(0.1)
        #await asyncio.restart_event_loop()


    if __name__ == '__main__':
        asyncio.run(main())

except Exception as e:
    asyncio.run(main())
    print("Error: " + str(e))
    #mainWindow.displayWindow.conversationBox.append("An error occurred: " + str(e) + "\n_______________________________\n")
    pass