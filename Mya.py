# Import necessary libraries
import openai
import pyttsx3
import speech_recognition as sr
import random

# Set OpenAI API key and model id
openai.api_key = "Input_your_api_key_here"
model_id = 'gpt-3.5-turbo'

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Change speech rate
engine.setProperty('rate', 180)

# Get the available voices
voices = engine.getProperty('voices')

# Choose a voice based on the voice id
engine.setProperty('voice', voices[1].id)

# Counter for interaction purposes
interaction_counter = 0

# Function to transcribe audio to text using Google Speech Recognition
def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except:
            print("")

# Function to perform ChatGPT conversation
def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    api_usage = response['usage']
    print('Total tokens consumed: {0}'.format(api_usage['total_tokens']))
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation

# Function to speak a given text using the text-to-speech engine
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Starting conversation with a predefined prompt
conversation = []
conversation.append({'role': 'user', 'content': 'chat with me as you be Friday AI from Iron Man, please make a one sentence phrase introducing yourself without saying something that sounds like this chat its already started'})
conversation = ChatGPT_conversation(conversation)
print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
speak_text(conversation[-1]['content'].strip())

# Function to generate a response for the assistant's activation
def activate_assistant():
    starting_chat_phrases = ["Yes sir, how may I assist you?", "Yes, What can I do for you?", ... ]  # (Truncated for brevity)
    continued_chat_phrases = ["yes", "yes, sir", "yes, boss", "I'm all ears"]

    random_chat = ""
    if(interaction_counter == 1):
        random_chat = random.choice(starting_chat_phrases)
    else:
        random_chat = random.choice(continued_chat_phrases)

    return random_chat

# Function to append a given text to the chat log
def append_to_log(text):
    with open("chat_log.txt", "a") as f:
        f.write(text + "\n")

# Main loop for continuous interaction
while True:
    # Wait for users to say "Friday"
    print("Say 'Friday' to start...")
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            if "friday" in transcription.lower():
                interaction_counter += 1
                # Record audio
                filename = "input.wav"
                readyToWork = activate_assistant()
                speak_text(readyToWork)
                print(readyToWork)

                # Capture audio and save it to a file
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    source.pause_threshold = 1
                    audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                    with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())

                # Transcribe audio to text
                text = transcribe_audio_to_text(filename)
                if text:
                    print(f"You said: {text}")
                    append_to_log(f"You: {text}\n")

                    # Generate response using ChatGPT
                    print(f"Friday says: {conversation}")

                    prompt = text
                    conversation.append({'role': 'user', 'content': prompt})
                    conversation = ChatGPT_conversation(conversation)

                    print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))

                    # Append assistant's response to the chat log
                    append_to_log(f"Mya: {conversation[-1]['content'].strip()}\n")

                    # Read the assistant's response using text-to-speech
                    speak_text(conversation[-1]['content'].strip())

        except Exception as e:
            continue
