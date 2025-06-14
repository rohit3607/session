import os
from dotenv import load_dotenv
from pyrogram import Client

# Load environment variables from .env file if present
load_dotenv()

def get_input_or_env(variable_name, prompt):
    value = os.getenv(variable_name)
    if not value:
        value = input(prompt)
    return value

# Function to generate the session string
def export_session_string():
    # Get API ID
    API_ID = get_input_or_env("API_ID", "Enter your API ID: ")

    # Get API Hash
    API_HASH = get_input_or_env("API_HASH", "Enter your API Hash: ")

    # Get phone number
    PHONE_NUMBER = get_input_or_env("PHONE_NUMBER", "Enter your phone number (with country code): ")

    # Use a safe writable directory
    session_dir = os.path.join(os.path.expanduser("~"), "pyrogram_sessions")
    os.makedirs(session_dir, exist_ok=True)
    SESSION_STRING = os.path.join(session_dir, "my_session")

    session_file = f"{SESSION_STRING}.session"

    try:
        app = Client(
            name=SESSION_STRING,
            api_id=API_ID,
            api_hash=API_HASH,
            phone_number=PHONE_NUMBER
        )

        with app:
            session_string = app.export_session_string()
            print("Session string generated successfully!\n")
            print("Your session string is:\n")
            print(session_string)

            # Send session string to "Saved Messages"
            app.send_message("me", f"Your generated session string:\n\n`{session_string}`")
            print("Session string has been sent to your 'Saved Messages'.")

        # Delete session file AFTER client context closes
        if os.path.exists(session_file):
            os.remove(session_file)
            print(f"\nSession file '{session_file}' has been deleted.")
        else:
            print(f"\nSession file '{session_file}' not found.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
if __name__ == "__main__":
    export_session_string()