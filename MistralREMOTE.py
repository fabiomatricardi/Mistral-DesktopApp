import streamlit as st
from mistralai import Mistral
import warnings
warnings.filterwarnings(action='ignore')
import datetime
import random
import string
from PIL import Image


import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

verbosity = False
nCTX = '32k'
sTOPS = ['<eos>']
modelname = "Mistral AI"
model = 'mistral-small-latest'
# Set the webpage title
st.set_page_config(
    page_title=f"Your LocalGPT ✨ with {modelname}",
    page_icon="🌟",
    layout="wide")

if "hf_model" not in st.session_state:
    st.session_state.hf_model = "mistral-small-latest"
# Initialize chat history for the LLM
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize the ChatMEssages for visualization only
if "chatMessages" not in st.session_state:
    st.session_state.chatMessages = []

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.1

if "maxlength" not in st.session_state:
    st.session_state.maxlength = 500

if "numOfTurns" not in st.session_state:
    st.session_state.numOfTurns = 0

if "maxTurns" not in st.session_state:
    st.session_state.maxTurns = 11  #must be odd number, greater than equal to 5

def writehistory(filename,text):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(text)
        f.write('\n')
    f.close()

def genRANstring(n):
    """
    n = int number of char to randomize
    """
    N = n
    res = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=N))
    return res
#

@st.cache_resource 
def create_chat(apikey):   
# Set HF API token  and HF repo
    from mistralai import Mistral
    #APIK = 'jspAEJOmr87tF7R7yMmgYyEgKbQDKR0c'
    client = Mistral(api_key=apikey)
    modelname = "Mistral AI"
    print(f'Loaded remote model {modelname}...')
    return client


# create THE SESSIoN STATES
if "logfilename" not in st.session_state:
## Logger file
    logfile = f'{genRANstring(5)}_log.txt'
    st.session_state.logfilename = logfile
    #Write in the history the first 2 sessions
    writehistory(st.session_state.logfilename,f'{str(datetime.datetime.now())}\n\nYour own LocalGPT with 🌀 {modelname}\n---\n🧠🫡: You are a helpful assistant.')    
    writehistory(st.session_state.logfilename,f'🌀: How may I help you today?')


#AVATARS
av_us =  Image.open(resource_path('user.png'))  #'🧑‍💻'    #'images/user.png'  # './man.png'  #"🦖"  #A single emoji, e.g. "🧑‍💻", "🤖", "🦖". Shortcodes are not supported.
av_ass =  Image.open(resource_path('assistant.png'))   #'Ⓜ️'   #'images/assistant.png'   #'./robot.png'

### START STREAMLIT UI
# Create a header element
st.image(Image.open(resource_path('mistralai.png')), width=700)### st.image('images/mistralai.png',use_container_width=True)
#st.code(intro, language=None)
mytitle = f'> *🌟 {modelname} with {nCTX} tokens Context window* - Turn based Chat available with max capacity of :orange[**{st.session_state.maxTurns} messages**].'
st.markdown(mytitle, unsafe_allow_html=True)


# CREATE THE SIDEBAR
with st.sidebar:
    st.image(Image.open(resource_path('mistral-banner.png')), width=250)
    mistral_api_key = st.text_input("OpenRouter API Key", key="or_api_key", type="password")
    "[Get a Mistral.ai API key](https://console.mistral.ai/)"
    st.session_state.temperature = st.slider('Temperature:', min_value=0.0, max_value=1.0, value=0.65, step=0.01)
    st.session_state.maxlength = st.slider('Length reply:', min_value=150, max_value=2000, 
                                           value=550, step=50)
    st.session_state.turns = st.toggle('Turn based', value=True, help='Activate Conversational Turn Chat with History', 
                                       disabled=False, label_visibility="visible")
    st.markdown(f"*Number of Max Turns*: {st.session_state.maxTurns}")
    actualTurns = st.markdown(f"*Chat History Lenght*: :green[Good]")
    statstime = st.markdown(f'⏳ gen.time: 0 sec')
    btnClear = st.button("Clear History",type="primary", use_container_width=True)
    st.markdown(f"**Logfile**: {st.session_state.logfilename}")

# Display chat messages from history on app rerun
for message in st.session_state.chatMessages:
    if message["role"] == "user":
        with st.chat_message(message["role"],avatar=av_us):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"],avatar=av_ass):
            st.markdown(message["content"])
# Accept user input
if myprompt := st.chat_input("What is an AI model?"):
    if not mistral_api_key:
        st.info("Please add your valid Mistral.ai API key to continue.")
        st.stop()
    llm = create_chat(mistral_api_key)
    st.session_state.messages.append({"role": "user", "content": myprompt})
    st.session_state.chatMessages.append({"role": "user", "content": myprompt})
    st.session_state.numOfTurns = len(st.session_state.messages)
    # Display user message in chat message container
    with st.chat_message("user", avatar=av_us):
        st.markdown(myprompt)
        usertext = f"user: {myprompt}"
        writehistory(st.session_state.logfilename,usertext)
        # Display assistant response in chat message container
    with st.chat_message("assistant",avatar=av_ass):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            start = datetime.datetime.now()
            response = ''
            conv_messages = []
            if st.session_state.turns:
                if st.session_state.numOfTurns > st.session_state.maxTurns:
                    conv_messages = st.session_state.messages[-st.session_state.maxTurns:]
                    actualTurns.markdown(f"*Chat History Lenght*: :red[Trimmed]")
                else:    
                    conv_messages = st.session_state.messages
            else:
                conv_messages.append(st.session_state.messages[-1])
            full_response = ""
            response = llm.chat.complete(
                model=model,
                messages=conv_messages,
                temperature=st.session_state.temperature,
                max_tokens=st.session_state.maxlength)
            full_response = response.choices[0].message.content              

            delta = datetime.datetime.now() - start
            totalseconds = delta.total_seconds()
            statstime.markdown(f'⏳ gen.time: {int(totalseconds)} sec')
            toregister = full_response + f"""
```
⏳ generation time: {delta}
```"""    
            message_placeholder.markdown(full_response)
            asstext = f"assistant: {toregister}"
            writehistory(st.session_state.logfilename,asstext)       
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.session_state.chatMessages.append({"role": "assistant", "content": full_response})
        st.session_state.numOfTurns = len(st.session_state.messages)