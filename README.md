# Retail Q&A Application

This application provides a question-answering system for retail products using the Cerebras API. It allows users to ask questions about products and receive AI-generated answers.

## Features

- Simple JSON-based product data storage
- AI-powered question answering using Cerebras API
- Clean and responsive frontend interface
- Dockerized deployment for easy setup
- Fallback answers when API is unavailable

## Directory Structure

```
retail-qa-app/
├── api/                  # Backend API service
│   ├── app.py            # Main Flask application
│   ├── Dockerfile        # Docker configuration for API
│   └── requirements.txt  # Python dependencies
├── data/                 # Data storage
│   └── products.json     # Product information
├── frontend/             # Frontend web interface
│   ├── Dockerfile        # Docker configuration for frontend
│   ├── index.html        # Main HTML page
│   └── nginx.conf        # Nginx configuration
├── docker-compose.yml    # Docker Compose configuration
├── setup.sh              # Setup script
├── test.sh               # Test script
└── README.md             # This documentation
```

## Prerequisites

- Docker and Docker Compose
- OpenRouter API key (optional, for Cerebras API access)

## Setup Instructions

1. Clone this repository:
   ```
   git clone <repository-url>
   cd retail-qa-app
   ```

2. Make the setup script executable:
   ```
   chmod +x setup.sh
   ```

3. Run the setup script:
   ```
   ./setup.sh YOUR_OPENROUTER_API_KEY
   ```
   Note: If you don't provide an API key, the application will use fallback answers.

4. Access the application:
   - Frontend: http://localhost:3000
   - API health check: http://localhost:5000/api/health

## Testing

To verify that the application is working correctly:

1. Make the test script executable:
   ```
   chmod +x test.sh
   ```

2. Run the test script:
   ```
   ./test.sh
   ```

This will test all API endpoints and functionality.

## API Endpoints

- `GET /api/health`: Health check endpoint
- `GET /api/products`: Get all products
- `GET /api/products/<product_id>`: Get a specific product
- `POST /api/ask`: Ask a question about products
  - Request body: `{"question": "What is the ModalAI VOXL 2?"}`
  - Optional: `{"question": "...", "productId": "voxl-2"}`

## Adding New Products

To add new products, edit the `data/products.json` file. Each product should have the following structure:

```json
{
  "productId": "unique-id",
  "name": "Product Name",
  "description": "Detailed description of the product",
  "category": "Product Category",
  "price": 999.99,
  "specifications": [
    "Specification 1",
    "Specification 2"
  ],
  "features": [
    "Feature 1",
    "Feature 2"
  ],
  "faqs": [
    "Q: Question? A: Answer.",
    "Q: Another question? A: Another answer."
  ]
}
```

## Stopping the Application

To stop the application:

```
docker-compose down
```

## Troubleshooting

- If the frontend cannot connect to the API, ensure that the API service is running and accessible at http://localhost:5000
- Check the Docker logs for any errors: `docker-compose logs`
- Verify that the OpenRouter API key is correctly set if you're using the Cerebras API

## License
Adaboost
[Specify your license here]
