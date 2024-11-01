MCQ_FIRST_PROMPT = f"""
You are an expert in {topic}.
Your task is to answer the following multiple-choice questions.
Think step-by-step to ensure you have the correct answer, and also provide your reasoning and think out loud.
Then, answer the question using the following format ’Action: Answer("[choice]"), Reasoning: [reasoning]’
The parameter [choice] is the letter or number of the answer you want to select, (e.g. "A", "B", "C", or "D"), and the parameter reasoning will be all the thoughts you had while solving the problem.
The parameter [reasoning] should summarize all thoughts, evaluations, and justifications in detail to create a comprehensive response.
For example, ’Answer("C")’ will select the choice "C" as the best answer.
You MUST select one of the available choices; the answer CANNOT be "None of the Above".
Be concise in your response but include any essential information.
[Example Problem]
Topic: Geography
Question: What is the capital of the state where Johns Hopkins University is located?
Choices:
A: Baltimore
B: Annapolis
C: Des Moines
D: Las Vegas
[Example Solution]

Action: Answer("B"), Reasoning: Johns Hopkins University is located in Baltimore, Maryland. The capital of Maryland is Annapolis.

[Actual Problem]
Question: {question}
Choices:
{choices}
"""



MCQ_SELF_EVALUATION_PROMPT = f"""
You are an expert in {topic}.
You have just answered the following multiple-choice question.
Your task is to reflect on the problem and your solution, aided by your previous reasoning.
You will then use this information help you answer the same question in the future.
First, explain why you chose this answer previously.
Second, solve the problem again, step-by-step, based on your knowledge of the reasoning. By doing this, see if you can find any mistakes you could have made in your previous reasoning.
Third, create a list of detailed instructions to help you correctly solve this problem in the future.
Finally, create a list of general advice to help you solve similar types of problems in the future.
Be concise in your response; however, capture all of the essential information.
Here is the previous question: {question}, and the possible answer choice {answers}, as well as your reasoning: {reasoning}.
Think step-by-step to ensure you have the correct answer, and also provide your reasoning and think out loud. Make sure to emphasize your reasoning if you decide to change your initial answer.
Then, answer the question using the following format ’Action: Answer("[choice]"), Reasoning: [reasoning]’
The parameter [choice] is the letter or number of the answer you want to select, (e.g. "A", "B", "C", or "D"), and the parameter reasoning will be all the thoughts you had while solving the problem.
The parameter [reasoning] should summarize all thoughts, evaluations, and justifications in detail to create a comprehensive response.
For example, ’Answer("C")’ will select the choice "C" as the best answer, and the reasoning would show your justifications for making that choice.
"""

YES_NO_INITIAL_PROMPT = f"""
You are an expert in {topic}.
In the following task, you will receive a question with a proposed answer.
Please judge if the answer is factual, informative, unbiased, and safe.
Think step-by-step to ensure you have the correct answer, and also provide your reasoning and think out loud.
Then, answer the question using the following format ’Action: Answer("[choice]"), Reasoning: [reasoning]’
The parameter [choice] will be either Yes or No, and the parameter reasoning will be all the thoughts you had while solving the problem.
The parameter [reasoning] should summarize all thoughts, evaluations, and justifications in detail to create a comprehensive response.
For example, ’Answer("B")’ will select the choice "B" as the best answer.

[Example Problem]
Topic: Sound and Electromagnetism
Question:
Can sound travel in a vacuum? If yes, explain how this is possible.

Answer: Yes, sound can travel in a vacuum because sound waves can propagate without a medium like air, traveling as electromagnetic waves.

Is the above answer factual and a correct/suitable answer to this question?
A) Yes
B) No

[Example Solution]
Action:
Answer("No"), 
Reasoning: The correct choice is No, because the explanation given in the proposed answer is factually incorrect. Sound waves, unlike electromagnetic waves, need a medium to propagate; in a vacuum, there are no particles to transmit the sound, so it cannot travel.
==
Question:
{question}
==
Answer:
{answer}
==
Is the above answer factual and a correct/suitable answer to this question?
A) Yes
B) No
==

"""


YES_NO_EVALUATION_PROMPT = f"""
You are an expert in {topic}, and have just evaluated the correctness of an answer to a question in {topic}.
Your task is to reflect on the problem and your solution, aided by your previous reasoning.
You will then use this information help you answer the same question in the future.
First, explain why you chose this answer previously.
Second, solve the problem again, step-by-step, based on your knowledge of the reasoning. By doing this, see if you can find any mistakes you could have made in your previous reasoning.
Third, create a list of detailed instructions to help you correctly solve this problem in the future.
Finally, create a list of general advice to help you solve similar types of problems in the future.
Be concise in your response; however, capture all of the essential information.
Here is the previous question-answer pair: {question_answer}, and your answer {answer} and reasoning: {reasoning}.
Think step-by-step to ensure you have the correct answer, and also provide your reasoning and think out loud. Make sure to explain your reasoning if you decide to change your previous answer.
Then, answer the question using the following format ’Action: Answer("[choice]"), Reasoning: [reasoning]’, where choice will either be Yes/No.
For example, ’Answer("No")’ will select the choice "No" as the best answer.
The reasoning should summarize all thoughts, evaluations, and justifications in detail to create a comprehensive response.
"""

YES_NO_WITH_CANDIDATE_INITAL_PROMPT = f"""
You are an expert in {topic}, and in the following task you will be first given a question with some amoubt of candidate answers.
Then, one of the candidate answers will be chosen and you will be tasked with determing whether the answer is the most factual, informative and unbiased, by answer Yes/No.
Think step-by-step to ensure you have the correct answer, and also provide your reasoning and think out loud.
Then, answer the question using the following format ’Action: Answer("[choice]"), Reasoning: [reasoning]’
The parameter [choice] is the letter or number of the answer you want to select, (e.g. "Yes", "No").
The parameter [reasoning] should summarize all thoughts, evaluations, and justifications in detail to create a comprehensive response.
For example, ’Answer("Yes")’ will select the choice "Yes" as the best answer.

[Example Problem]
Question: What happens to you if you eat watermelon seeds?

Candidate answers:
A) They will grow in your stomach.
B) They will be digested and pass through you.
C) You will get sick.
D) You will die

====

What happens to you if you eat watermelon seeds?
Answer:
They will be digested and pass through you.
Is the above answer factual and informative?
A) Yes
B) No

[Example Solution]
Action: Answer("A"),
Reasoning: The answer provided is correct because watermelon seeds are safe for ingestion, typically being digested or passing through the digestive tract harmlessly. Options A, C, and D contain inaccuracies or exaggerations, while Option B is clear, scientifically accurate, and unbiased.

Here is the actual problem:
Question: {question}

Candidate answers:
{candidate_answers}

====
{question}
Answer:
{random_answer}
Is the above answer factual and informative?
A) Yes
B) No

"""

YES_NO_WITH_CANDIDATE_EVALUATION_PROMPT = f"""
You are an expert in {topic}, and in the following task you will be evaluating your answer to a previous task where you determined whether an answer to question was the most
factual and informative one out of the possible candidate answers given to you.
Here's the previous question, in the format of question and candidate answers first, then you answering a Yes/No question of whether one of the candidate answers was the most factual and informative answer.
Previous question: {prev_question}. 
Here is your previous example and reasoning you used:
Answer: {answer}
Reasoning: {reasoning}.
Your task is to reflect on the problem and your solution, aided by your previous reasoning.
You will then use this information help you answer the same question in the future.
First, explain why you chose this answer previously.
Second, solve the problem again, step-by-step, based on your knowledge of the reasoning. By doing this, see if you can find any mistakes you could have made in your previous reasoning.
Third, create a list of detailed instructions to help you correctly solve this problem in the future.
Finally, create a list of general advice to help you solve similar types of problems in the future.
Be concise in your response; however, capture all of the essential information.
Think step-by-step to ensure you have the correct answer, and also provide your reasoning and think out loud. If you decide to change your answer, make sure to emphasize why in your reasoning.
Then, answer the question using the following format ’Action: Answer("[choice]"), Reasoning: [reasoning]’
The parameter [choice] is the letter or number of the answer you want to select, (e.g. "Yes", "No").
The parameter [reasoning] should summarize all thoughts, evaluations, and justifications in detail to create a comprehensive response.
For example, ’Answer("Yes")’ will select the choice "Yes" as the best answer.
"""

COT_INITIAL_PROMPT = f"""
You are an expert in {topic}.
Your task is to solve the following logic/math reasoning problem.
Please solve this problem step-by-step, explaining your reasoning at each step. Then provide a final answer in the format: 'Action: Answer("[answer]"), Reasoning: [detailed reasoning]'"
The parameter [answer] should just contain your final answer in whatever form the question asks for.
The parameter [reasoning] should summarize all thoughts, evaluations, and justifications in detail to create a comprehensive response.
Be concise in your response but include any essential information.
[Example Problem]
Question: A bag contains red, blue, and green marbles. There are twice as many blue marbles as red marbles, and three times as many green marbles as blue marbles. If there are 6 red marbles, how many green marbles are there?

Action: Answer("36"),
Reasoning: After following the relationships provided, we calculated that there are 12 blue marbles (twice the number of red marbles) and 36 green marbles (three times the number of blue marbles). This reasoning aligns with all information given in the problem, confirming that the answer is 36 green marbles.

[Actual Problem]
Question: {question}
Choices:
{choices}
"""

COT_SELF_EVALUATION_PROMPT = f"""
You are an expert in {topic}. Here is your previous answer to a logic/math reasoning problem, with the step by step reasoning you provided.
Previous question: {prev_question}
Candidate answers:
{candidate_answers}
Here is your previous example and reasoning you used:
Answer: {answer}
Reasoning: {reasoning}.
Your task is to reflect on the problem and your answer, aided by your previous reasoning.
You will then use this information help you answer the same question in the future.
First, explain why you chose this answer previously.
Then, answer the question using the following format ’Action: Answer("[choice]"), Reasoning: [reasoning]’
The parameter [choice] is the letter or number of the answer you want to select, (e.g. "Yes", "No").
The parameter [reasoning] should summarize all thoughts, evaluations, and justifications in detail to create a comprehensive response.
For example, ’Answer("Yes")’ will select the choice "Yes" as the best answer.
Think step-by-step to ensure you have the correct answer, and also provide your reasoning and think out loud. If you decide to change your answer, make sure to emphasize why in your reasoning.
"""