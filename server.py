# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from ctransformers import AutoModelForCausalLM
import logging

# Set logging level info
logging.basicConfig(level=logging.INFO)
# init logger
logger = logging.getLogger(__name__)
logger.info("Starting up..")


app = FastAPI()

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

temperature = 0.1
top_p = 0.5
context_length = 4096
max_new_tokens = 4096
chat_model = ChatModel(temperature, top_p, max_new_tokens, context_length)

# Function for generating LLaMA2 response
def generate_llama2_response(messages):
    prompt_input = ""
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\\n\\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\\n\\n"
    output = chat_model(f"prompt {string_dialogue} {prompt_input} Assistant: ")
    return output

class ChatRequest(BaseModel):
    text: str
    
class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    messages = []
    logger.info(f"request: {request.text}")
    messages.append({"role": "user", "content": request.text})
    response = generate_llama2_response(messages)
    logger.info(f"response: {response}")
    return {"response": response}

@app.get("/health")
async def health():
    return {"health": "ok"}