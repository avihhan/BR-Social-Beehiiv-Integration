# Beehiiv Integration Backend

A Python backend service that integrates with the Beehiiv API to handle email subscriptions and send welcome emails. This service is designed to be deployed on Google Cloud Functions with automated deployment via GitHub Actions.

## Features

- ✅ Subscribe users to Beehiiv newsletter via API
- 
- ✅ Send welcome emails automatically through Beehiiv
- ✅ Handle existing subscribers gracefully
- ✅ RESTful API endpoints
- ✅ Google Cloud Functions deployment ready
- ✅ GitHub Actions CI/CD pipeline
- ✅ Environment-based configuration

## API Endpoints

### POST /subscribe
Subscribe a user to the newsletter

**Request Body:**
```json
{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "source": "website"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully subscribed to newsletter",
  "subscriber_id": "sub_123456"
}
```

### GET /health
Health check endpoint

### GET /publication-info
Get information about the Beehiiv publication

## Setup Instructions

### 1. Beehiiv API Setup

1. Log in to your Beehiiv dashboard
2. Go to Settings > API
3. Generate an API key
4. Note your Publication ID

### 2. Environment Configuration

Copy the example environment file and fill in your values:

```bash
cp env.example .env
```

Update the following variables:
- `BEEHIIV_API_KEY`: Your Beehiiv API key
- `BEEHIIV_PUBLICATION_ID`: Your publication ID

### 3. Local Development

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 4. Google Cloud Functions Deployment

#### Option A: Manual Deployment

1. Set up Google Cloud SDK
2. Authenticate: `gcloud auth login`
3. Set your project: `gcloud config set project YOUR_PROJECT_ID`
4. Deploy:
```bash
gcloud functions deploy beehiiv-integration \
  --runtime=python311 \
  --trigger=http \
  --allow-unauthenticated \
  --source=. \
  --entry-point=main \
  --set-env-vars="BEEHIIV_API_KEY=your_key,BEEHIIV_PUBLICATION_ID=your_id"
```

#### Option B: GitHub Actions (Recommended)

1. Set up the following secrets in your GitHub repository:
   - `GCP_PROJECT_ID`: Your Google Cloud project ID
   - `GCP_SA_KEY`: Service account key (JSON format)
   - `BEEHIIV_API_KEY`: Your Beehiiv API key
   - `BEEHIIV_PUBLICATION_ID`: Your publication ID

2. Push to the main branch to trigger deployment

### 5. Frontend Integration

Update your React frontend to call the new backend:

```javascript
const subscribeToNewsletter = async (email, firstName, lastName) => {
  try {
    const response = await fetch('YOUR_CLOUD_FUNCTION_URL/subscribe', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        first_name: firstName,
        last_name: lastName,
        source: 'website'
      })
    });
    
    const result = await response.json();
    
    if (result.success) {
      console.log('Successfully subscribed!');
    } else {
      console.error('Subscription failed:', result.message);
    }
  } catch (error) {
    console.error('Network error:', error);
  }
};
```

## Project Structure

```
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── cloudbuild.yaml        # Cloud Build configuration
├── .github/
│   └── workflows/
│       └── deploy.yml     # GitHub Actions workflow
├── env.example            # Environment variables template
└── README.md             # This file
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BEEHIIV_API_KEY` | Your Beehiiv API key | Yes |
| `BEEHIIV_PUBLICATION_ID` | Your publication ID | Yes |
| `ENVIRONMENT` | Environment (development/production) | No |

## Error Handling

The API handles various error scenarios:

- Invalid email addresses
- Network connectivity issues
- Beehiiv API errors
- Already subscribed users
- Missing configuration

## Logging

The application uses Python's built-in logging module. In Cloud Functions, logs are automatically sent to Google Cloud Logging.

## Security

- API keys are stored as environment variables
- HTTPS is enforced in production
- Input validation using Pydantic models
- No sensitive data in logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

MIT License
