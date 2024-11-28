# Claude Search Assistant

An intelligent chatbot application that combines the power of Claude 3 Haiku with real-time web search capabilities, built with FastAPI and React.

## Overview

Claude Search Assistant is a web-based chatbot that enhances Claude's capabilities with real-time web search functionality using the SERP API. This integration allows the chatbot to provide up-to-date information while maintaining Claude's conversational abilities.

## Features

- **Real-time Web Search**: Integrates SERP API to fetch current information from the internet
- **Intelligent Response System**: Uses Claude 3.5 Haiku to determine when to use web search vs. model knowledge
- **Simple Web Interface**: Clean and responsive React-based chat interface
- **Session Management**: Maintains conversation history within sessions
- **Rate Limiting**: Built-in protection against excessive API usage
- **Real-time Date Display**: Shows current date for context awareness

## Technology Stack

### Backend
- FastAPI (Python web framework)
- LangChain (For tool integration and chat management)
- Anthropic's Claude 3 Haiku
- SERP API (For web search capabilities)
- AWS Bedrock (For Claude API access)

### Frontend
- React
- Modern CSS with flexbox
- Real-time updates

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js and npm
- AWS account with Bedrock access
- SERP API key
- Anthropic API key

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend/app
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the backend/app directory with the following variables:
```
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=your_aws_region
SERP_API_KEY=your_serp_api_key
```

5. Start the backend server:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the frontend directory:
```
REACT_APP_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm start
```

## Usage Examples

1. **Basic Questions**
   - The chatbot will use Claude's knowledge base for general questions
   - Example: "What is the capital of France?"

2. **Current Events**
   - The system will automatically use web search for time-sensitive queries
   - Example: "What are the latest developments in AI technology?"

3. **Real-time Information**
   - Perfect for getting up-to-date information
   - Example: "What's the weather like in New York right now?"

4. **Combined Knowledge**
   - The system can blend Claude's knowledge with current web data
   - Example: "Compare historical and current inflation rates"

## API Rate Limits

- The API is limited to 5 requests per minute per IP address
- Implement appropriate error handling in your applications

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m 'Add YourFeature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Submit a pull request

## License

This project is open-source and available under the MIT License.

## Future Improvements

- Add support for multiple search engines
- Implement user authentication
- Add support for file uploads and processing
- Enhance error handling and retry mechanisms
- Add support for streaming responses
- Implement conversation summarization
- Add support for multiple language inputs

## Troubleshooting

Common issues and solutions:

1. **API Connection Issues**
   - Verify your environment variables are set correctly
   - Check your AWS credentials and permissions
   - Ensure SERP API key is valid

2. **Rate Limiting**
   - Implement exponential backoff in your requests
   - Consider caching frequent queries

3. **Web Search Not Working**
   - Verify SERP API key and quota
   - Check network connectivity
   - Review API response logs

For additional support, please open an issue in the GitHub repository.