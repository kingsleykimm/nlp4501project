from transformers import AutoTokenizer, AutoModelForCausalLM
from datasets import load_dataset
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--dataset_name", type=str, help="dataset name")

args = parser.parse_args()

ds = load_dataset("openai/gsm8k", "main")
train = ds['train'].with_format('torch')

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-70B-Instruct")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-70B-Instruct")

for item in ds:
    print(item)
    break