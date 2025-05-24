#!/bin/bash

# Test script for the Retail Q&A Application
# This script tests the API endpoints and functionality

# Check if curl is installed
if ! command -v curl &> /dev/null; then
    echo "curl is required to run this test script."
    echo "Please install it and try again."
    exit 1
fi

# Define API URL
API_URL="http://localhost:5000"

# Test health endpoint
echo "Testing API health endpoint..."
HEALTH_RESPONSE=$(curl -s $API_URL/api/health)
if [[ $HEALTH_RESPONSE == *"healthy"* ]]; then
    echo "✅ Health check passed!"
else
    echo "❌ Health check failed: $HEALTH_RESPONSE"
    exit 1
fi

# Test products endpoint
echo "Testing products endpoint..."
PRODUCTS_RESPONSE=$(curl -s $API_URL/api/products)
if [[ $PRODUCTS_RESPONSE == *"ModalAI VOXL 2"* ]]; then
    echo "✅ Products endpoint passed!"
else
    echo "❌ Products endpoint failed: $PRODUCTS_RESPONSE"
    exit 1
fi

# Test specific product endpoint
echo "Testing specific product endpoint..."
PRODUCT_RESPONSE=$(curl -s $API_URL/api/products/voxl-2)
if [[ $PRODUCT_RESPONSE == *"ModalAI VOXL 2"* ]]; then
    echo "✅ Specific product endpoint passed!"
else
    echo "❌ Specific product endpoint failed: $PRODUCT_RESPONSE"
    exit 1
fi

# Test question answering
echo "Testing question answering..."
QUESTION_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d '{"question":"What is the ModalAI VOXL 2?"}' $API_URL/api/ask)
if [[ $QUESTION_RESPONSE == *"answer"* ]]; then
    echo "✅ Question answering passed!"
    echo "Answer: $(echo $QUESTION_RESPONSE | sed 's/.*"answer":"\([^"]*\)".*/\1/')"
else
    echo "❌ Question answering failed: $QUESTION_RESPONSE"
    exit 1
fi

echo ""
echo "All tests passed! The API is functioning correctly."
echo "You can now access the frontend at: http://localhost:3000"
