import openai
import config
import typer
from rich import print
from rich.table import Table

def main():
    # Set the OpenAI API key
    openai.api_key = config.api_key

    print("[bold green]ChatGPT API in Python[/bold green]")

    # Create a table using Rich to display available commands
    table = Table("Command", "Description")
    table.add_row("exit", "Exit the application")
    table.add_row("new", "Start a new conversation")
    print(table)

    # Initial context for the translation assistant
    context = {"role": "system", "content": "You are a translation assistant from Spanish to English"}
    messages = [context]

    # Main application loop
    while True:
        content = __prompt()

        # Restart the conversation if the user types "new"
        if content.lower() == "new":
            messages = [context]
            content = __prompt()

        # Add the user's message to the message history
        messages.append({"role": "user", "content": content})

        # Generate a response using the GPT model
        response = openai.chat.completions.create(
            messages=messages,
            model="gpt-4-turbo",
        )

        # Get the content of the assistant's response
        response_content = response.choices[0].message.content

        # Add the assistant's response to the message history
        messages.append({"role": "assistant", "content": response_content})

        # Print the assistant's response
        print(f"[bold green]> [/bold green] [green]{response_content}[/green]")

def __prompt() -> str:
    # Prompt the user to enter a message
    prompt = typer.prompt("\nWhat do you want to talk about?")

    # Check if the user wants to exit the application
    if prompt.lower() == "exit":
        exit_confirm = typer.confirm("Are you sure?")
        if exit_confirm:
            raise typer.Abort()
        else:
            return __prompt()  # Prompt again if exit is not confirmed

    return prompt

if __name__ == "__main__":
    typer.run(main)
