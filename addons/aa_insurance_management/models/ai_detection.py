from odoo import models, fields, api
import requests
import os
import base64  
import logging
from datetime import datetime, timedelta
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
class AiDetection(models.Model):
    _name = 'ai.detection'
    _description = 'AI Detection Result'

    name = fields.Char(string="Name")
    image = fields.Binary(string="Original Image")
    result_image = fields.Binary(string="Detected Image")
    result_filename = fields.Char(string="Detected Filename")
    image_filename = fields.Char(string="Filename")
    uploaded_by = fields.Many2one('res.users', default=lambda self: self.env.user)
    upload_date = fields.Datetime(default=fields.Datetime.now)
    confidence = fields.Float(string="Confidence")
    detected_at = fields.Datetime(string="Detected At", default=fields.Datetime.now)

    @api.model
    def create_detection(self, name, image_path):
        # image to FastAPI
        with open(image_path, 'rb') as img_file:
            files = {'file': (os.path.basename(image_path), img_file, 'image/jpeg')}
            try:
                response = requests.post("http://127.0.0.1:9000/detect", files=files)
                #response = requests.post("http://localhost:9000/detect", 
                #files=files)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                raise ValueError(f"Error contacting AI server: {e}")

        result = response.json()

        # result
        result_image_b64 = result.get("result_image")
        confidence = result.get("confidence")
        result_filename = result.get("result_filename")

        # original image
        with open(image_path, 'rb') as f:
            original_img_data = f.read()
        encoded_original = base64.b64encode(original_img_data).decode("utf-8")

        # record 
        return self.create({
            'name': name,
            'image_filename': os.path.basename(image_path),
            'confidence': confidence,
            'image': encoded_original,
            'result_image': result_image_b64,
            'result_filename': result_filename,
        })
    @api.model
    def cron_example_action(self):
        try:
            _logger.info("[CRON] AI Detection job started at %s", datetime.now())

            # Step 1: result image n arai garaagui huleegdej baigaa zurguud
            pending_detections = self.search([('result_image', '=', False)])
            _logger.info("Found %s pending detections to process.", len(pending_detections))

            # Step 2: het ih detection-uuudaiig shalgah
            if len(pending_detections) > 50:
                _logger.warning("More than 50 unprocessed detections! Consider scaling the AI endpoint.")

            # Step 3: Archive old entries (e.g., older than 90 days)
            old_entries = self.search([('upload_date', '<', datetime.now() - timedelta(days=90))])
            old_entries.write({'active': False})
            _logger.info("Archived %s old AI detection records.", len(old_entries))


        except Exception as e:
            _logger.error(" Error in AI Detection cron job: %s", str(e))
            raise UserError(f"CRON job failed: {e}")



        