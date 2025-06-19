from odoo import models, fields
from inference_sdk import InferenceHTTPClient, InferenceConfiguration
import base64, io
from PIL import Image, ImageDraw
import numpy as np

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="b2cdoHqW3C4PJBx2QBbD"
)

class AiDetectionWizard(models.TransientModel):
    _name = 'ai.detection.wizard'
    _description = 'AI Image Detection Wizard'

    image = fields.Binary(string="Upload Image", required=True)
    image_filename = fields.Char(string="Filename")
    result_image = fields.Binary(string="Detection Result", readonly=True)
    record_id = fields.Many2one('ai.detection', string="Output Record")

    def process_image(self):
        raw = base64.b64decode(self.image)
        # Save temp file
        tmp = io.BytesIO(raw)
        config = InferenceConfiguration(confidence_threshold=0.1)
        with CLIENT.use_configuration(config):
            result = CLIENT.infer("", file=tmp, model_id="car-damage-detection-ha5mm/1")

        # Open image with PIL
        img = Image.open(io.BytesIO(raw)).convert("RGB")
        draw = ImageDraw.Draw(img)
        for pred in result["predictions"]:
            x, y, w, h = pred["x"], pred["y"], pred["width"], pred["height"]
            x1, y1 = x - w/2, y - h/2
            x2, y2 = x + w/2, y + h/2
            draw.rectangle([x1, y1, x2, y2], outline=(0,255,0), width=3)

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        self.result_image = base64.b64encode(buf.getvalue())

        # Save to permanent model
        record = self.env['ai.detection'].create({
            'name': self.image_filename,
            'image': self.image,
            'result_image': self.result_image,
        })
        self.record_id = record.id
        return {'type': 'ir.actions.act_window',
                'res_model': 'ai.detection',
                'res_id': record.id,
                'view_mode': 'form',
                'target': 'new'}
