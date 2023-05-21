import openai

def generate_gpt_response(prompt, model="gpt-4", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert programmer with multiple centuries of experience programming. Your job is to be as helpful as possible."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
    )
    return response.choices[0].message['content']

def generate_gpt_response_with_context(prompt, context, model="gpt-4", temperature=1):
    context.append({
        "role": "user",
        "content": prompt
    })
    response = openai.ChatCompletion.create(
        model=model,
        messages=context,
        temperature=temperature,
    )
    context.append({
        "role": "assistant",
        "content": response.choices[0].message['content']
    })
    return response.choices[0].message['content']

def calculate_context_characters(context):
    total_chars = 0
    for message in context:
        total_chars += len(message['content'])
    return total_chars

def reset_context_if_needed(context, prompt):
    if (calculate_context_characters(context) + len(prompt) > 15000):
        formatted_context = generate_formatted_context(context)
        context_prompt = f"Summarize everything you know about the repository based on this conversation in 3 paragraphs: {formatted_context}"
        response = generate_gpt_response_with_context(context_prompt)                
        print("\033[36m\nReset memory: " + response + "\033[0m" + "\n")

        # Reset context with the response
        context = [
            {
                "role": "assistant",
                "content": response
            }
        ]
    return context

def generate_formatted_context(context):
    formatted_context = ''
    for message in context:
        role = message['role']
        content = message['content']
        formatted_context += f"{role}: {content}\n"
    return formatted_context