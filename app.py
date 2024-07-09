import os
import re
import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image as VertexImage
from flask import Flask, request, jsonify, render_template, send_file
from google.cloud import aiplatform
from PIL import Image, ImageDraw, ImageFont
import json
import logging
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Set Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = app.config['GOOGLE_APPLICATION_CREDENTIALS']

# Initialize Vertex AI
vertexai.init(project=app.config['VERTEX_PROJECT_ID'], location=app.config['VERTEX_LOCATION'])

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.content_length > app.config['MAX_CONTENT_LENGTH']:
        return jsonify({'error': 'File size exceeds the maximum limit'}), 400
    
    if file:
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        return jsonify({'message': 'File uploaded successfully', 'filename': file.filename}), 200

@app.route('/process', methods=['POST'])
def process_image():
    filename = request.json['filename']
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    logger.info(f"Processing image: {filename}")

    # Load the image using Vertex AI's Image class
    image_file = VertexImage.load_from_file(filepath)

    # Initialize Gemini API
    model = GenerativeModel(model_name="gemini-1.5-flash-001")
    
    # Prepare the prompt
    prompt = """
    Analyze this image of a web page design. Identify and locate the following components:
    - Buttons
    - Input fields
    - Links
    - Images
    - Text blocks
    - Navigation menus

    For each component, provide:
    1. The type of component
    2. A brief description
    3. The approximate location in the image (top-left coordinates, width, and height as percentages of the image dimensions)

    Format the response as a JSON array of components, each containing 'type', 'description', and 'location' fields.
    """

    # Generate content
    logger.info("Generating content with Gemini API")
    response = model.generate_content(
        [prompt, Part.from_image(image_file)],
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32
        }
    )

    logger.debug(f"Raw response: {response}")

    # Extract the JSON content from the response
    if hasattr(response.candidates[0].content, 'parts'):
        parts = response.candidates[0].content.parts
    else:
        raise AttributeError("Unexpected response structure")

    logger.debug(f"Type of parts: {type(parts)}")
    logger.debug(f"Length of parts: {len(parts)}")

    # Get the first (and only) Part object
    first_part = parts[0]
    logger.debug(f"Type of first part: {type(first_part)}")

    # Convert the Part object to a string
    part_str = str(first_part)
    logger.debug(f"Part as string: {part_str}")

    # Extract the text content from the string representation
    text_match = re.search(r'text: "(.*)"', part_str, re.DOTALL)
    if text_match:
        text_content = text_match.group(1)
        # Unescape the text content
        text_content = text_content.encode().decode('unicode_escape')
        logger.debug(f"Extracted text content: {text_content}")
    else:
        raise ValueError('Failed to extract text content from Part')

    # Extract JSON from the text content
    json_match = re.search(r'```json\n(.*?)\n```', text_content, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
        logger.debug(f"Extracted JSON string: {json_str}")
    else:
        raise ValueError('Failed to extract JSON from text content')

    # Parse the JSON string
    try:
        components = json.loads(json_str)
        logger.debug(f"Parsed components: {components}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        raise ValueError(f"Failed to parse JSON: {str(e)}")

    try:
        # Open the original image
        img = Image.open(filepath)
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        # Draw bounding boxes and labels
        for component in components:
            top = component['location']['top']
            left = component['location']['left']
            width = component['location']['width']
            height = component['location']['height']
            
            # Convert percentages to pixel values
            x1 = int(left * img.width / 100)
            y1 = int(top * img.height / 100)
            x2 = int((left + width) * img.width / 100)
            y2 = int((top + height) * img.height / 100)
            
            # Draw rectangle
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            
            # Draw label
            draw.text((x1, y1 - 10), component['type'], fill="red", font=font)

        # Save the processed image
        output_path = os.path.join(UPLOAD_FOLDER, 'processed_' + filename)
        img.save(output_path)

        logger.info(f"Processed image saved as {output_path}")

        return jsonify({
            'processed_image': 'processed_' + filename, 
            'components': components
        })

    except Exception as e:
        logger.exception(f"An error occurred during image processing: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/image/<filename>')
def serve_image(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), mimetype='image/png')

if __name__ == '__main__':
    app.run('localhost', port=8000, debug=True)