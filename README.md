# Flask Chatbot

A simple chatbot application built with Flask and Python. This project demonstrates the use of Flask for creating REST APIs, along with LangChain for handling conversational AI and vector stores.

## Features

- **Chatbot Interaction**: Users can interact with the chatbot using POST requests.
- **URL Storage**: Save URLs and vectorize their content for the chatbot.
- **JWT Authentication**: Secure endpoints with JSON Web Tokens.
- **Vector Stores**: Utilize LangChain to handle document vectors and responses.

## Requirements

- Python 3.8+
- Flask
- Flask-JWT-Extended
- LangChain
- LangChain Community
- LangChain OpenAI
- Pickle

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo.git
    ```

2. Navigate to the project directory:

    ```bash
    cd your-repo
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Environment Variables**: Ensure you set up the following environment variables for JWT secret key and database URI.

    ```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development
    export JWT_SECRET_KEY=your_jwt_secret_key
    export DATABASE_URL=your_database_url
    ```

2. **Database Setup**: Initialize the database by creating the necessary tables. You can do this by running Flask migrations or creating tables manually.

## Usage

1. **Start the Flask Server**:

    ```bash
    flask run
    ```

2. **Endpoints**:

    - **GET /**: Returns a welcome message.
    - **POST /api/create-JWT**: Generates a JWT token for authentication. Requires a `username` in the request body.
    - **POST /api/save-urls**: Saves URLs and updates the vector store. Requires `urls`, `customer_userid`, and `botname` in the request body. Requires JWT authentication.
    - **POST /api/chat**: Sends a message to the chatbot and retrieves a response. Requires `text`, `customer_userid`, `botname`, and `sender` in the request body. Requires JWT authentication.


## Contributing

Feel free to fork the repository, make improvements, and submit pull requests. For any issues or feature requests, please open an issue on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **[LangChain](https://langchain.com/)**: For providing powerful tools for document processing and conversational AI.
- **[Flask](https://flask.palletsprojects.com/en/2.1.x/)**: For creating the web application framework.
