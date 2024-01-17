import asyncio

from rasa.core.agent import Agent


class MyRasa:
    def __init__(self):
        # Load the trained Rasa model
        model_path = "rasa/models"

        # Create a Rasa agent
        self.agent = Agent.load(model_path)

    def process(self, user_input):
        async def parse(text):
            return await self.agent.handle_text(text)

        # Send user input to Rasa
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(parse(user_input))

        # Extract and return the bot's response text
        if result:
            return result[0]['text']
        else:
            return "Sorry, I didn't understand that."


if __name__ == "__main__":
    myRasa = MyRasa()
    response = myRasa.process("Hi")
    print("Bot:", response)
    response = myRasa.process("Bye")
    print("Bot:", response)

