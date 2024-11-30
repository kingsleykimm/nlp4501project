#!/usr/bin/env python
# coding: utf-8

# In[1]:


from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("Llama-3.1-8B-Instruct")
model = AutoModelForCausalLM.from_pretrained("Llama-3.1-8B-Instruct", device_map='auto')
# In[3]:


from datasets import load_dataset

ds = load_dataset("truthfulqa/truthful_qa", "multiple_choice")['validation'].with_format('torch')


# In[4]:


# In[5]:


from prompts import *


# In[6]:


import torch
def entropy_function(tens):
    tens = torch.nn.functional.softmax(tens[0])
    return -(tens @ torch.log(tens))


# In[9]:


import time
alpha = 'ABCDEFGHIJKLMNOPQSTUVWXYZ'

ent, n_1_ent = 0, 0
num_resp = 0
acc, n_1_acc = 0, 0
for ind, item in enumerate(ds):
    start_time = time.time()
    q = item['question']
    choices = item['mc1_targets']['choices']
    labels = item['mc1_targets']['labels']
    correct_answer = alpha[torch.nonzero(labels, as_tuple=True)[0][0]]
    print(correct_answer)
    # format choices
    for ans in range(len(choices)):
        choices[ans] = alpha[ans] + ": " + choices[ans]
    choices = "\n".join(choices)
    prompt = MCQ_FIRST_PROMPT.format(question=q, choices=choices)
    conversation = [
        {
            "role" : "user",
            "content" : prompt
        }
    ]
    formatted_chat = tokenizer.apply_chat_template(conversation, tokenize=True, return_tensors="pt", add_generation_prompt=True)
    # print(formatted_chat)
    # batch = tokenizer(
    #     text=formatted_chat,
    #     padding=True,
    #     return_tensors='pt'
    # )
    formatted_chat = formatted_chat.to('cuda')
    out = model.generate(formatted_chat, output_logits=True, max_new_tokens=384, return_dict_in_generate=True)
    sequences, first_logits = out.sequences, out.logits
    output = tokenizer.batch_decode(sequences, skip_special_tokens=True)[0]
    output = output.strip()
    assistant_response = output.split('assistant')[1]
    answer_ind = assistant_response.find('Answer')
    if answer_ind == -1:
        continue
    reasoning_ind = assistant_response.find('Reasoning')
    # print(output)
    # softmax = torch.nn.functional.softmax(logits[-2])
    # word = torch.argmax(softmax).item()
    # print(tokenizer.convert_ids_to_tokens(word))

    # usually the answer token is going to be logits[-2] since logits[-1] is an <eot_token_id>
    # print(output)
    
    # find index of answer, find index of reasoning
    answer = assistant_response[answer_ind:]
    reasoning = assistant_response[reasoning_ind:answer_ind]
    # print(answer, reasoning)
    
    self_eval_prompt = MCQ_SELF_EVALUATION_PROMPT.format(question=q + '\n' + choices, answer = answer, reasoning=reasoning)
    self_evaluation_conversation = [
        {
            "role" : "user",
            "content" : self_eval_prompt
        }
    ]
    self_chat = tokenizer.apply_chat_template(self_evaluation_conversation, tokenize=True, return_tensors='pt', add_generation_prompt=True)
    self_chat = self_chat.to('cuda')
    out = model.generate(self_chat, output_logits=True, max_new_tokens=384, return_dict_in_generate=True)
    self_eval_sequences, self_eval_logits = out.sequences, out.logits
    n_1_output = tokenizer.batch_decode(self_eval_sequences, skip_special_tokens=True)[0].strip()
    n_1_output = output.strip()
    # print(output)
    answer_ind = output.find('Answer')
    if answer_ind == -1:
        continue
    # softmax = torch.nn.functional.softmax(logits[-2])
    # word = torch.argmax(softmax).item()
    # print(tokenizer.convert_ids_to_tokens(word))

    # get the answer
    print(output[-1], n_1_output[-1])
    ent += entropy_function(first_logits[-2])
    n_1_ent += entropy_function(self_eval_logits[-2])
    acc += 1 if output[-1] == correct_answer else 0
    n_1_acc += 1 if n_1_output[-1] == correct_answer else 0
    num_resp += 1
    print(f"Iteration time: {time.time() - start_time}")


print(f"First ent {ent / num_resp}, N=1 Ent {n_1_ent / num_resp}")
print(f"First acc {acc / num_resp}, N=1 Acc {n_1_acc / num_resp}")



    
    



# In[ ]:




