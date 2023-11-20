
from openai import OpenAI

client = OpenAI(api_key="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")



def create_email(user_prompt):

    system_prompt = """
    you are a restuarnt owner, providing replies to your customer by reading their replies
    """

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
                ]
    )
    return completion.choices[0].message.content 

    
