from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
from PIL import Image
import io
import logging
from groq import Groq

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize Groq client
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    logger.error("GROQ_API_KEY environment variable is not set")
    raise ValueError("GROQ_API_KEY environment variable is not set")

client = Groq(api_key=GROQ_API_KEY)

# Function to generate text-based farm recommendations
def generate_prompt(farm_data):
    return f"""You are an expert agricultural advisor. Based on the following farm details, provide specific recommendations for crops and agrochemical products that would yield the best results. Include specific product names, application methods, and timing where relevant.

Farm Details:
- Land Size: {farm_data['landSize']} acres
- Soil Type: {farm_data['soilType']}
- Irrigation Method: {farm_data['irrigation']}
- Location: {farm_data['location']}
- Desired Crop Type: {farm_data['cropType']}
- Additional Information: {farm_data['additional']}

Provide your recommendations in the following markdown format:

# Crop Recommendations
[List specific crop varieties that would work well]

# Soil Preparation
[Specific steps and products for soil preparation]

# Fertilizer Recommendations
[Specific fertilizer products and application schedules]

# Pest Management
[Specific pesticide recommendations and application guidelines]

# Irrigation Schedule
[Detailed irrigation recommendations]

# Expected Yield
[Projected yield estimates and timeline]

Please be specific with product names and application rates while ensuring all recommendations are environmentally responsible and follow agricultural best practices."""

@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    farm_data = request.json
    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are an expert agricultural advisor specializing in crop selection and agrochemical recommendations. Provide detailed, practical advice based on the farm details provided."},
                {"role": "user", "content": generate_prompt(farm_data)}
            ],
            temperature=0.7,
            max_tokens=2048
        )
        return jsonify({"status": "success", "recommendations": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Function to encode an image to base64
def encode_image_to_base64(image_file):
    try:
        img = Image.open(image_file)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    except Exception as e:
        logger.error(f"Error in encode_image_to_base64: {str(e)}")
        raise

# Function to analyze a crop image
def analyze_image(base64_image):
    try:
        prompt = """Analyze this image of a crop plant and identify any diseases present. Please provide:
        1. Disease name (if any)
        2. Confidence level
        3. Recommended treatment
        4. Prevention measures
        If the plant appears healthy, please indicate that as well."""
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ],
            model="llama-3.2-90b-vision-preview",
            max_tokens=1000
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in analyze_image: {str(e)}")
        raise

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        base64_image = encode_image_to_base64(image_file)
        analysis_result = analyze_image(base64_image)
        return jsonify({'result': analysis_result})
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
