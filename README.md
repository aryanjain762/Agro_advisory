# Agricultural AI Platform

## Overview
The **Agricultural AI Platform** is a web-based solution designed to provide AI-powered insights and solutions for farmers. The platform offers two key features:
1. **Farm Recommendations** - Provides AI-driven recommendations for crops, fertilizers, and farming practices.
2. **Crop Disease Detection** - Uses AI image analysis to detect plant diseases and suggest treatment solutions.

## Features
- **AI-based Farm Advisory**: Offers expert recommendations based on farm details such as soil type, irrigation methods, and location.
- **Crop Disease Detection**: Uses image analysis to detect crop diseases and provide treatment suggestions.
- **Interactive Web Interface**: A visually appealing front-end for users to interact with the platform.

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python), Groq API
- **AI Model**: Llama-3.2-90b-vision-preview (for image analysis)
- **Database**: None (stateless API-based approach)
- **Hosting**: Local/Cloud deployment options

## Installation
### Prerequisites
- Python 3.8+
- Flask
- Flask-CORS
- PIL (Pillow)
- Groq API Key

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/aryanjain762/Agro_advisory.git
   cd Agro_advisory
   ```
2. Install dependencies:
   ```bash
   pip install flask flask-cors pillow
   ```
3. Set up the environment variable for Groq API:
   ```bash
   export GROQ_API_KEY="your_api_key_here"
   ```
4. Run the Flask application:
   ```bash
   python agro.py
   ```
5. Open `agro.html` in a web browser.

## API Endpoints
### 1. Get Farm Recommendations
**Endpoint:** `POST /get-recommendations`
- **Request Body (JSON):**
  ```json
  {
    "landSize": 10,
    "soilType": "Loamy",
    "irrigation": "Drip",
    "location": "California",
    "cropType": "Wheat",
    "additional": "Organic farming preferred"
  }
  ```
- **Response:** AI-generated farm recommendations.

### 2. Crop Disease Detection
**Endpoint:** `POST /analyze`
- **Request Body:** Multipart form with an image file.
- **Response:** AI-generated disease analysis and treatment suggestions.

## Developer
Developed by **Aryan Jain**.

## License
This project is licensed under the MIT License.

