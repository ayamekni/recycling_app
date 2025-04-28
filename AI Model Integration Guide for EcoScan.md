# AI Model Integration Guide for EcoScan

This guide explains how to integrate and use the AI bottle detection and classification model with your EcoScan recycling application.

## Model Architecture

The EcoScan bottle recycling system uses a transfer learning approach based on MobileNetV2 for efficient bottle material classification. The model can:

1. **Detect bottles** in images
2. **Classify material types** (PET, HDPE, Glass, Aluminum, etc.)
3. **Determine recyclability**
4. **Estimate value** and points for rewards

## Project Structure

The AI model integration consists of these components:

- `services/bottle_agent.py` - Main agent class for bottle analysis
- `services/bottle_scan.py` - Service that integrates the agent with Flask
- `scripts/train_model.py` - Utility for training custom models
- `models/` - Directory for storing trained models

## Getting Started

### Prerequisites

Make sure you have the following packages installed:

```bash
pip install tensorflow numpy opencv-python pillow matplotlib pandas
```

### Using the Pre-trained Model

1. Place your trained model file in the `models/` directory
2. Configure the model path in `config.py`:

   ```python
   # AI Model Configuration
   MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models/bottle_detection_model.h5')
   ```

3. Use the bottle scanning service in your routes:

   ```python
   from services.bottle_scan import analyze_bottle_image
   
   # In your route handler
   result = analyze_bottle_image(image_path)
   ```

### Training Your Own Model

To train a custom model with your data:

1. Organize your dataset in class folders:

   ```
   dataset/
   ├── PET/
   │   ├── image1.jpg
   │   ├── image2.jpg
   │   └── ...
   ├── HDPE/
   │   └── ...
   ├── Glass/
   │   └── ...
   └── ...
   ```

2. Run the training script:

   ```bash
   python scripts/train_model.py train --dataset path/to/dataset --output models/my_model.h5 --epochs 20
   ```

3. Test your model:

   ```bash
   python scripts/train_model.py test --model models/my_model.h5 --image path/to/test_image.jpg
   ```

## Agent Configuration

You can adjust the agent behavior in `config.py`:

```python
# AI Model Configuration
MODEL_PATH = 'path/to/model.h5'
DETECTION_THRESHOLD = 0.7  # Minimum confidence threshold
USE_MOCK_MODEL = False     # Set to True to use random predictions for testing
```

## Material Classification

The system recognizes the following material types:

| ID | Material | Recyclable | Points | Value Range |
|----|----------|------------|--------|-------------|
| 0  | PET      | Yes        | 10     | $0.05-0.15  |
| 1  | HDPE     | Yes        | 12     | $0.10-0.20  |
| 2  | PVC      | No         | 5      | $0.03-0.07  |
| 3  | LDPE     | Yes        | 7      | $0.05-0.10  |
| 4  | PP       | Yes        | 10     | $0.08-0.15  |
| 5  | PS       | No         | 6      | $0.04-0.09  |
| 6  | Glass    | Yes        | 15     | $0.15-0.25  |
| 7  | Aluminum | Yes        | 20     | $0.20-0.30  |
| 8  | Other    | No         | 3      | $0.01-0.05  |

## Response Format

The model returns results in this format:

```python
{
    'success': True,
    'is_bottle': True,
    'is_recyclable': True,
    'material_type': 'PET',
    'material_id': 0,
    'estimated_value': 0.12,
    'points_earned': 10,
    'confidence': 0.92
}
```

## Offline Mode

If no model is available, the system falls back to random predictions for demonstration purposes. This allows you to test the UI without a trained model.

## Adding New Material Types

To add new material types, update the `MATERIAL_TYPES` dictionary in the `