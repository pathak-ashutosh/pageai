# PAGE-AI

PAGE-AI is an AI-powered web design analysis tool that uses Google's Vertex AI to detect and analyze components in web page designs.

## Project Overview

PAGE-AI takes an image of a web page design as input and uses the Gemini model from Vertex AI to identify various components such as buttons, input fields, links, images, and text blocks. It then generates a processed image with bounding boxes around these components and provides detailed information about each detected element.

## Features

- Upload web page design images
- AI-powered component detection
- Visual output with bounding boxes
- Detailed component information including type, description, and location

For a overview and future roadmap, please refer to the [project scope](https://github.com/pathak-ashutosh/pageai/SCOPE.md).

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.9+
- A Google Cloud account with Vertex AI API enabled
- A service account key with necessary permissions for Vertex AI

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/PAGE-AI.git
   cd PAGE-AI
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Google Cloud credentials:
   - Place your service account key JSON file in the project root
   - Create a `.env` file in the project root with the following content:
     ```bash
     GOOGLE_APPLICATION_CREDENTIALS=./your-service-account-key.json
     VERTEX_PROJECT_ID=your-project-id
     VERTEX_LOCATION=us-central1
     VERTEX_MODEL_NAME=gemini-1.5-flash-001
     ```
   Replace `your-service-account-key.json` and `your-project-id` with your actual values.

## Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Upload an image of a web page design

4. View the processed image with detected components and their details

## Project Structure

- `app.py`: Main Flask application
- `config.py`: Configuration settings
- `requirements.txt`: Project dependencies
- `uploads/`: Directory for uploaded and processed images
- `templates/`: HTML templates
- `example/`: Example processed images

## Contributing

Contributions to PAGE-AI are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a pull request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - ashutoshpathak[[[at]]]thenumbercrunchdotcom

Project Link: [https://github.com/pathak-ashutosh/PageAI](https://github.com/pathak-ashutosh/pageai)

## Acknowledgements

- [Google Vertex AI](https://cloud.google.com/vertex-ai)
- [Flask](https://flask.palletsprojects.com/)
- [Pillow](https://python-pillow.org/)
