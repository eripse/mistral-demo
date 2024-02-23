import json
from typing import TypedDict
from potassium import Potassium, Request, Response
import threading


from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, pipeline
import torch

app = Potassium("my_app")

class Context(TypedDict):
    model: AutoModelForCausalLM
    tokenizer: AutoTokenizer
    streamer: TextIteratorStreamer

# @app.init runs at startup, and loads models into the app's context
@app.init
def init():
    model = AutoModelForCausalLM.from_pretrained("TheBloke/Mistral-7B-v0.1-AWQ")
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
    model.to(torch.device("cuda"))
   
    context = {
        "model": model,
        "tokenizer": tokenizer,
    }

    return context

# @app.handler runs for every call
@app.handler("/")
def handler(context: dict, request: Request) -> Response:
    prompt = request.json.get("prompt")
    model = context["model"]
    tokenizer = context["tokenizer"]
    streamer = TextIteratorStreamer(tokenizer)

    model_inputs = tokenizer([prompt], return_tensors="pt").to(torch.device("cuda"))

    def run_model():
        _ = model.generate(**model_inputs, streamer=streamer, max_new_tokens=100, do_sample=True)

    t = threading.Thread(target=run_model)
    t.start()

    def generate_text():
        for new_text in streamer:
            if new_text == "":
                continue
            payload = {
                "text": new_text
            }

            json_string = json.dumps(payload) + "\n"
            json_bytes = json_string.encode("utf-8")
            yield json_bytes



    return Response(
        body=generate_text(),
        headers={
            "Content-Type": "application/json"
        }
    )

if __name__ == "__main__":
    app.serve()
