import time
from langchain_core.messages import AIMessage, HumanMessage
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from flask import jsonify, current_app as app
from flask import request
from .utils import get_vectorstore_from_urls, get_response, serialize_vector_store, deserialize_vector_store, get_doc_from_urls
from . import db
from .models import OpenAPIChatbot,ChatHistory, Customers

# vector_stored_data = None
# chat_history = []

@app.route('/', methods=['GET'])
def get_api():
    return jsonify({'message': 'Welcome to the Flask REST API!'})

@app.route('/api/save-urls', methods=['POST'])
@jwt_required()
def save_urls():
    # global vector_stored_data
    current_user = get_jwt_identity()
    customer = Customers.query.filter_by(Username=current_user).first()
    if not customer:
        return jsonify({'error': 'Unauthorized'}), 401


    print(current_user)
    data = request.get_json()
    urls = data.get("urls")
    # customer_userid = data.get("customer_userid")
    customer_userid = customer.UserId
    botname = data.get("botname")
    if not urls:
        return jsonify({"error": "Missing 'urls'"}), 400
    if not customer_userid:
        return jsonify({"error": "Missing 'customer_userid'"}), 400
    if not botname:
        return jsonify({"error": "Missing 'botname'"}), 40
    
    print("URLs received:", urls)
    # vector_stored_data = get_vectorstore_from_urls(urls)
    # print("Vector store data:", vector_stored_data)
    document = get_doc_from_urls(urls)
    print(document)
    print(type(document))
    # return "test"


    if document is None:
        return jsonify({"error": "Failed to save URLs"}), 500
    document_pickle = serialize_vector_store(document)
    print(document_pickle)
    chatbot = OpenAPIChatbot.query.filter_by(customer_userid=customer_userid, botname=botname   ).first()
    if chatbot is None:
        chatbot = OpenAPIChatbot(customer_userid=customer_userid, urls=urls, botname=botname, vectorstore=document_pickle)
        db.session.add(chatbot)
    else:
        chatbot.urls = urls
        chatbot.vectorstore = document_pickle

    db.session.commit()
    return jsonify({"message": "URL saved and vector store data updated"}), 201

@app.route('/api/chat', methods=['POST'])
@jwt_required()
def chat():
    current_user = get_jwt_identity()
    customer = Customers.query.filter_by(Username=current_user).first()
    if not customer:
        return jsonify({'error': 'Unauthorized'}), 401

    # global chat_history
    data = request.get_json()
    text = data.get("text")
    # customer_userid = data.get("customer_userid")
    customer_userid = customer.UserId

    botname = data.get("botname")
    sender = data.get("sender")
    print("Text received:", text)
    if sender is None or len(sender) <=0:
        return jsonify({"error": "Missing 'sender'"}), 400
    if not text :
        return jsonify({"error": "Missing 'text'"}), 400
    if not customer_userid:
        return jsonify({"error": "Missing 'customer_userid'"}), 400
    if not botname:
        return jsonify({"error": "Missing 'botname'"}), 400

    chatbot = OpenAPIChatbot.query.filter_by(customer_userid=customer_userid, botname=botname).first()
    if chatbot is None:
        return jsonify({"error": "User not found"}), 404

    vector_stored_pickle = chatbot.vectorstore
    # start_time = time.time()
    vector_stored_data = deserialize_vector_store(vector_stored_pickle)
    print("Vector store data:", vector_stored_data)
    # end_time = time.time()
    # print(f"time for  deserialize_vector_store {end_time-start_time} sec")


    messages = ChatHistory.query.filter_by(customer_userid=customer_userid, sender=sender,bot_id=chatbot.id).all()
    print(messages)
    chat_history =[]
    for msg in messages:
        chat_history.append(HumanMessage(content=msg.user_message))
        chat_history.append(AIMessage(content=msg.bot_response))

    
    # start_time = time.time()

    answer = get_response(text, vector_store=vector_stored_data, chat_history=chat_history)
    print("Answer generated:", answer)
    # end_time = time.time()
    # print(f"time for  get_response {end_time-start_time} sec")


    
    if answer is None:
        return jsonify({"error": "Failed to get response"}), 500
     # Save chat history
    chat_entry = ChatHistory(customer_userid=customer_userid, user_message=text, bot_response=answer,sender=sender,bot_id=chatbot.id)
    db.session.add(chat_entry)
    db.session.commit() 

    # chat_history.append(HumanMessage(content=text))
    # chat_history.append(AIMessage(content=answer))
    print(chat_history)
    return jsonify({"message": answer}), 201
    

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/create-JWT', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    
    customer = Customers.query.filter_by(Username=username).first()

    if customer:
        # Assuming you only want to verify the existence of the username
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'error': 'User not found'}), 401
