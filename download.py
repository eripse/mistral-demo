# This file runs during container build time to get model weights built into the container
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, pipeline

def download_model():
    # do a dry run of loading the huggingface model, which will download weights
    model = AutoModelForCausalLM.from_pretrained("TheBloke/Mistral-7B-v0.1-AWQ")
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

if __name__ == "__main__":
    download_model()