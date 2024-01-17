import asyncio

from rasa import model
from rasa.core.agent import Agent

# Load the trained Rasa model
model_path = "models"
latest_model = model.get_latest_model(model_path)

# Create a Rasa agent
agent = Agent.load(model_path)
print("HERE")

async def parse(text):
    response = await agent.handle_text(text)
    return response

# Define a function to interact with the chatbot
def get_bot_response(user_input):
    # Send user input to Rasa
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(parse('Hi'))

    # Extract and return the bot's response text
    if responses:
        print("HERE", responses)
        return responses[0]['text']
    else:
        return "Sorry, I didn't understand that."


# Example usage
user_input = "Hi"
bot_response = get_bot_response(user_input)
print("Bot:", bot_response)
