"""
Retail Q&A Application API
A simplified Flask API for answering questions about retail products using Cerebras API.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import requests
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load product data from JSON file
def load_products():
    """
    Load product data from the JSON file.
    
    Returns:
        dict: The product data
    """
    try:
        with open('../data/products.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading products: {e}")
        return {"products": []}

# Cerebras API for question answering
def ask_cerebras(question, context):
    """
    Generate an answer using the Cerebras API.
    
    Args:
        question (str): The question to answer
        context (str): The context information to use for answering
        
    Returns:
        str: The generated answer
    """
    try:
        api_key = os.environ.get("OPENROUTER_API_KEY")
        model = os.environ.get("CEREBRAS_MODEL", "cerebras/qwen-3-32b")
        
        if not api_key:
            logger.warning("OPENROUTER_API_KEY not set, using fallback answers")
            return get_fallback_answer(question, context)
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful retail assistant. Answer questions about products based on the provided information."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
            ],
            "temperature": 0.2,
            "max_tokens": 300
        }
        
        logger.info(f"Sending request to Cerebras API for question: {question}")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            answer = result["choices"][0]["message"]["content"]
            logger.info(f"Received answer from Cerebras API: {answer[:100]}...")
            return answer
        else:
            logger.warning(f"Unexpected response from Cerebras API: {result}")
            return get_fallback_answer(question, context)
    except Exception as e:
        logger.error(f"Error calling Cerebras API: {e}")
        logger.error(traceback.format_exc())
        return get_fallback_answer(question, context)

def get_fallback_answer(question, context_json):
    """
    Generate a fallback answer when the Cerebras API fails.
    
    Args:
        question (str): The question to answer
        context_json (str): The context information as a JSON string
        
    Returns:
        str: The fallback answer
    """
    try:
        # Parse the context JSON
        if isinstance(context_json, str):
            context = json.loads(context_json)
        else:
            context = context_json
        
        # Check if we're dealing with a list of products or a single product
        products = []
        if isinstance(context, list):
            products = context
        elif isinstance(context, dict):
            if "products" in context:
                products = context["products"]
            else:
                products = [context]
        
        # Look for relevant information in the products
        question_lower = question.lower()
        
        # Check for product-specific questions
        for product in products:
            product_name = product.get("name", "").lower()
            product_id = product.get("productId", "").lower()
            
            # If the question mentions this product
            if product_name in question_lower or product_id in question_lower:
                # Check FAQs first
                for faq in product.get("faqs", []):
                    faq_parts = faq.split("A: ")
                    if len(faq_parts) > 1 and faq_parts[0].strip().lower().replace("q: ", "") in question_lower:
                        return faq_parts[1].strip()
                
                # If no matching FAQ, return product description
                if "what is" in question_lower or "tell me about" in question_lower:
                    return product.get("description", "I don't have information about this product.")
                
                # Check for specific attributes
                if "price" in question_lower:
                    return f"The {product.get('name')} costs ${product.get('price', 0):.2f}."
                
                if "specification" in question_lower or "specs" in question_lower:
                    specs = product.get("specifications", [])
                    if specs:
                        return f"The {product.get('name')} specifications include: {', '.join(specs)}."
                
                if "feature" in question_lower:
                    features = product.get("features", [])
                    if features:
                        return f"The {product.get('name')} features include: {', '.join(features)}."
        
        # Generic fallback
        return "I don't have enough information to answer that question. Please try asking about a specific product or feature."
    
    except Exception as e:
        logger.error(f"Error generating fallback answer: {e}")
        logger.error(traceback.format_exc())
        return "I'm sorry, I couldn't find an answer to your question."

# Error handler
@app.errorhandler(Exception)
def handle_exception(e):
    """
    Global exception handler to ensure JSON responses.
    
    Args:
        e: The exception
        
    Returns:
        tuple: JSON response and status code
    """
    logger.error(f"Unhandled exception: {str(e)}")
    logger.error(traceback.format_exc())
    return jsonify({"error": str(e)}), 500

# API routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status
    """
    return jsonify({"status": "healthy"})

@app.route('/api/products', methods=['GET'])
def get_products():
    """
    Get all products.
    
    Returns:
        list: All products
    """
    data = load_products()
    return jsonify(data["products"])

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """
    Get a specific product by ID.
    
    Args:
        product_id (str): The product ID
        
    Returns:
        dict: The product data or error
    """
    data = load_products()
    for product in data["products"]:
        if product["productId"] == product_id:
            return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route('/api/ask', methods=['POST', 'OPTIONS'])
def ask_question():
    """
    Answer a question about products.
    
    Returns:
        dict: The answer or error
    """
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
        
    try:
        logger.info(f"Received question request: {request.data}")
        
        # Parse JSON data
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        question = data.get("question", "")
        if not question:
            return jsonify({"error": "No question provided"}), 400
            
        product_id = data.get("productId", None)
        
        # Get product context
        product_context = ""
        products_data = load_products()
        
        if product_id:
            # Find specific product
            for product in products_data["products"]:
                if product["productId"] == product_id:
                    product_context = json.dumps(product)
                    break
            if not product_context:
                return jsonify({"error": f"Product with ID {product_id} not found"}), 404
        else:
            # Use all products as context
            product_context = json.dumps(products_data["products"])
        
        # Generate answer
        answer = ask_cerebras(question, product_context)
        
        return jsonify({"answer": answer})
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
