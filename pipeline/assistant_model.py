# You can add future GPT/OpenAI integration here
# For now, this is just a placeholder
def get_assistant_response(query):
    if "optimize" in query.lower():
        return "Try turning off non-essential appliances during peak hours."
    else:
        return "Sorry, I can only handle simple keyword queries for now."
