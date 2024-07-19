from app import create_app
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./dev.env")
OPEN_API_KEY = os.getenv("open_api_key")




app = create_app()




def set_openai_key(api_key):
    """Set the OpenAI API key in the environment variable.
    Args:
    key (str): The OpenAI API key to set.
    """
    os.environ["OPENAI_API_KEY"] = f"{api_key}"


if __name__ == "__main__":
    set_openai_key(OPEN_API_KEY)
    app.run(debug=True)

