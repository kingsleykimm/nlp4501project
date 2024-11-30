import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import math
import pandas as pd

# Define the model name for LLaMA 3.1 8B
MODEL_NAME = "meta-llama/Llama-3.1-8B"

# Download and load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16).cuda()

# Function to compute perplexity, entropy, and logits
def evaluate_prompt(prompt, model, tokenizer):
    # Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    input_ids = inputs["input_ids"]

    # Get model outputs
    with torch.no_grad():
        outputs = model(**inputs, labels=input_ids)
        logits = outputs.logits
        loss = outputs.loss  # Cross entropy loss

    # Calculate perplexity
    perplexity = math.exp(loss.item())

    # Get probabilities for each token
    logits_softmax = torch.nn.functional.softmax(logits, dim=-1)
    last_token_logits = logits[:, -1, :]
    last_token_probs = logits_softmax[:, -1, :]

    # Calculate entropy for the distribution of the last token
    entropy = -torch.sum(last_token_probs * torch.log(last_token_probs + 1e-10)).item()

    # Get the most probable token (predicted answer)
    predicted_token_id = torch.argmax(last_token_probs, dim=-1).item()
    predicted_token = tokenizer.decode(predicted_token_id)

    return {
        "perplexity": perplexity,
        "entropy": entropy,
        "logits_last_token": last_token_logits[0].cpu().numpy(),
        "predicted_token": predicted_token
    }

# Example dataset (replace this with the actual GSM8K dataset)
questions = [
    "temp placehold for the questions downloaded from GSM8K dataset"
]

# Storage for results
results = []

# Loop through each question in the dataset
for i, question in enumerate(questions):
    # Construct the prompt
    prompt = f"""
    Use the prompts found in the varunstuff/varunprompts.py file
    """

    # Evaluate the prompt
    evaluation = evaluate_prompt(prompt, model, tokenizer)

    # Store results in a 2D array (list of lists)
    results.append([
        i,  # Question index
        question,  # Original question
        evaluation["perplexity"],  # Perplexity
        evaluation["entropy"],  # Entropy
        evaluation["predicted_token"],  # Predicted answer
        evaluation["logits_last_token"].tolist()  # Logits for the last token
    ])

# Convert results into a DataFrame for better visualization
columns = ["Index", "Question", "Perplexity", "Entropy", "Predicted Answer", "Logits Last Token"]
df = pd.DataFrame(results, columns=columns)

# Display the results
print(df)


