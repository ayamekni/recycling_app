# recycling_app
# EcoScan - Bottle Recycling Web Application

EcoScan is a full-stack web application built with Flask, HTML, CSS, and Tailwind CSS that enables users to scan and identify recyclable bottles, track their recycling activities, and earn rewards for their environmental contributions.

## Key Features

1. **User Authentication**
   - Secure registration and login system
   - User profiles with recycling history and statistics

2. **Bottle Scanning and Recognition**
   - Upload images from your device
   - Take live photos using the device camera
   - AI-powered bottle recognition (integration ready)
   - Material type identification
   - Recyclability assessment
   - Value estimation

3. **Personal Dashboard**
   - Visual statistics and recycling performance metrics
   - Weekly activity tracking
   - Material breakdown analysis
   - Points and rewards system

4. **Interactive Maps**
   - Nearby recycling points visualization
   - User geolocation integration

5. **Educational Resources**
   - Recycling tips and best practices
   - Links to environmental articles
   - Inspirational quotes

6. **Modern UI/UX**
   - Responsive design for mobile and desktop
   - Sleek animations and transitions
   - Intuitive user flow
   - Real-time feedback

## Technical Architecture

### Backend (Flask)

The application follows a structured MVC-like architecture:

- **Models**: Database schemas for users and bottle scans
- **Routes**: API endpoints for authentication, scanning, and dashboard data
- **Services**: Business logic for bottle analysis and user rewards
- **Templates**: Jinja2 templates for rendering HTML views

### Frontend

- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **JavaScript**: Interactive features like camera access, charts, and maps
- **Chart.js**: Data visualization for recycling statistics
- **Google Maps API**: Location-based services

### AI Integration

The application is designed to easily integrate with an AI model for bottle recognition:

- Placeholder implementation for demonstration
- Ready for real model integration (TensorFlow, PyTorch, etc.)
- Configurable prediction threshold and confidence scoring

## Project Structure

```
recycling_app/
│
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models/                # Database models
│   ├── user.py            # User model
│   └── bottle.py          # Bottle scan model
│
├── routes/                # API routes
│   ├── auth.py            # Authentication routes
│   ├── bottle.py          # Bottle recycling routes
│   └── dashboard.py       # Dashboard routes
│
├── services/              # Business logic
│   └── bottle_scan.py     # Integration with AI model
│
├── static/                # Static assets
│   ├── css/
│   ├── js/
│   └── images/
│
└── templates/             # HTML templates
    ├── base.html          # Base template
    ├── index.html         # Home page
    ├── auth/              # Authentication templates
    ├── bottle/            # Bottle scanning templates
    └── dashboard/         # Dashboard templates
```

## Getting Started

### Prerequisites

- Python 3.8+
- Flask
- SQLAlchemy
- OpenCV (for image processing)
- Google Maps API key (for location services)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ecoscan.git
cd ecoscan
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export SECRET_KEY=your_secret_key
export GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

5. Run the application:
```bash
flask run
```

6. Access the application at http://localhost:5000

## AI Integration Guide

To integrate your own bottle recognition model:

1. Replace the placeholder implementation in `services/bottle_scan.py`
2. Load your trained model
3. Update the preprocessing function to match your model's requirements
4. Implement the prediction logic based on your model's output format

Example integration with TensorFlow:

```python
import tensorflow as tf

# Load model
model = tf.keras.models.load_model('path_to_your_model.h5')

def analyze_bottle_image(image_path):
    # Preprocess image
    img = preprocess_image(image_path)
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    
    # Run prediction
    prediction = model.predict(img)
    
    # Extract results based on your model architecture
    is_recyclable = prediction[0][0] > 0.5
    material_type = get_material_type(prediction)
    estimated_value = calculate_value(material_type)
    
    # Return result
    return {
        'is_recyclable': is_recyclable,
        'material_type': material_type,
        'estimated_value': estimated_value,
        'confidence': float(prediction[0][0])
    }
```

## Customization and Extension

The application is designed to be easily extended with additional features:

- **Social Sharing**: Add functionality to share recycling achievements
- **Gamification**: Enhance the rewards system with badges and leaderboards
- **Community Features**: Add user forums or community challenges
- **Mobile App**: Convert to a mobile application using frameworks like React Native

## License

This project is licensed under the MIT License - see the LICENSE file for details.