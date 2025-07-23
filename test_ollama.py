import subprocess

# Your test input
user_text = """
Today I fixed some issues with Apache, helped colleagues, worked on the new dashboard feature, and tested the VPN connection.
"""

# The prompt for the AI
prompt = f"""
Extract a list of individual tasks from the following work summary. Return as numbered list:
{user_text}
"""

# Run the local LLM (mistral) using Ollama
result = subprocess.run(
    ["ollama", "run", "mistral"],
    input=prompt.encode(),
    stdout=subprocess.PIPE
)

# Get and print the AI's reply
output = result.stdout.decode()
print("\n--- AI Output ---")
print(output)
