import base64
import io
import cv2
import numpy as np
import matplotlib.pyplot as plt

from odoo import models, fields, api

# RoboFlow
from inference_sdk import InferenceHTTPClient, InferenceConfiguration

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="b2cdoHqW3C4PJBx2QBbD"
)

class AiDetection(models.Model):
    _name = 'ai.detection'
    _description = 'AI Detection Result'

    name = fields.Char(string="Name")
    image = fields.Binary(string="Original Image")
    result_image = fields.Binary(string="Detected Image", readonly=True)
    result_filename = fields.Char(string="Detected Filename")
    image_filename = fields.Char(string="Filename")
    uploaded_by = fields.Many2one('res.users', default=lambda self: self.env.user)
    upload_date = fields.Datetime(default=fields.Datetime.now)
    
    confidence = fields.Float(string="Confidence")  
    detected_at = fields.Datetime(string="Detected At", default=fields.Datetime.now)

    @api.model
    def create_detection(self, name, image_path):
        # Load image and encode original
        with open(image_path, 'rb') as f:
            original_img_data = f.read()
        encoded_original = base64.b64encode(original_img_data).decode('utf-8')

        # Inference config
        config = InferenceConfiguration(confidence_threshold=0.1)
        with CLIENT.use_configuration(config):
            result = CLIENT.infer(image_path, model_id="car-damage-detection-ha5mm/1")

        prediction = result["predictions"][0]
        confidence = prediction['confidence']

        # Draw bounding box
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        x, y, w, h = prediction["x"], prediction["y"], prediction["width"], prediction["height"]
        x1, y1 = int(x - w / 2), int(y - h / 2)
        x2, y2 = int(x + w / 2), int(y + h / 2)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Convert to base64
        buffer = io.BytesIO()
        plt.imsave(buffer, img, format='png')
        result_img_data = buffer.getvalue()
        encoded_result = base64.b64encode(result_img_data).decode('utf-8')

        # Create record in Odoo
        print("Creating detection with:")
        print({
            'name': name,
            'image_filename': image_path.split("/")[-1],
            'confidence': confidence,
            'image': encoded_original[:30] + "...",
            'result_image': encoded_result[:30] + "...",
            'result_filename': 'detected_' + image_path.split("/")[-1],
        })

        return self.create({
            'name': name,
            'image_filename': image_path.split("/")[-1],
            'confidence': confidence,
            'image': encoded_original,
            'result_image': encoded_result,
            'result_filename': 'detected_' + image_path.split("/")[-1],
        })