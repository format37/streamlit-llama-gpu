import streamlit as st
import os
from ctransformers import AutoModelForCausalLM
import logging

# Set logging level info
logging.basicConfig(level=logging.INFO)
# init logger
logger = logging.getLogger(__name__)
logger.info("Starting up..")

# App title
st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")

@st.cache_resource()
def ChatModel(temperature, top_p, max_new_tokens, context_length):
# Load model from local file 
    model = AutoModelForCausalLM.from_pretrained(
        './models/luna-ai-llama2-uncensored.ggmlv3.q8_0.bin',
        model_type='llama',
        temperature=temperature, 
        top_p = top_p,
        gpu_layers=50,
        max_new_tokens=max_new_tokens,
        context_length=context_length,
        )
    
    return model

# Replicate Credentials
with st.sidebar:
    st.title('🦙💬 Llama 2 Chatbot')

    # Refactored from <https://github.com/a16z-infra/llama2-chatbot>
    st.subheader('Models and parameters')
    
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=2.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    # context_length = st.sidebar.slider('context_length', min_value=64, max_value=4096, value=4096, step=8)
    # max_new_tokens = st.sidebar.slider('max_new_tokens', min_value=64, max_value=4096, value=1024, step=8)
    context_length = 4096
    max_new_tokens = 4096
    chat_model = ChatModel(temperature, top_p, max_new_tokens, context_length)
    # st.markdown('📖 Learn how to build this app in this [blog](#link-to-blog)!')

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\\n\\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\\n\\n"
    output = chat_model(f"prompt {string_dialogue} {prompt_input} Assistant: ")
    return output

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
