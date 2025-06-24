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
    _rec_name = 'name'
    _order = 'upload_date desc'

    name = fields.Char(string="Name")
    image = fields.Binary(string="Original Image", required=True)
    result_image = fields.Binary(string="Detected Image")
    image_filename = fields.Char(string="Filename")
    result_filename = fields.Char(string="Detected Filename")
    uploaded_by = fields.Many2one('res.users', string="Uploaded By", default=lambda self: self.env.user)
    upload_date = fields.Datetime(string="Upload Date", default=fields.Datetime.now)
    detected_at = fields.Datetime(string="Detected At")
    confidence = fields.Float(string="Confidence")
    active = fields.Boolean(default=True)

    # For testing or scripted bulk detection
    @api.model
    def create_detection(self, name, image_path):
        with open(image_path, 'rb') as img_file:
            files = {'file': (os.path.basename(image_path), img_file, 'image/jpeg')}
            try:
                response = requests.post("http://127.0.0.1:9000/detect", files=files)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                raise ValueError(f"❌ Error contacting AI server: {e}")

        result = response.json()

        result_image_b64 = result.get("result_image")
        confidence = result.get("confidence")
        result_filename = result.get("result_filename")

        with open(image_path, 'rb') as f:
            original_img_data = f.read()
        encoded_original = base64.b64encode(original_img_data).decode("utf-8")

        return self.create({
            'name': name,
            'image': encoded_original,
            'image_filename': os.path.basename(image_path),
            'confidence': confidence,
            'result_image': result_image_b64,
            'result_filename': result_filename,
            'detected_at': datetime.now(),
        })

    # Called from UI button
    def action_detect_image(self):
        for record in self:
            if not record.image:
                raise UserError("⚠️ Please upload an image before running detection.")

            image_data = base64.b64decode(record.image)
            image_path = f"/tmp/{record.image_filename or 'uploaded.jpg'}"

            # Step 1: Save the image temporarily
            with open(image_path, "wb") as temp_file:
                temp_file.write(image_data)

            try:
                # Step 2: Open file and send to API
                with open(image_path, 'rb') as img_file:
                    files = {
                        'file': (record.image_filename or "uploaded.jpg", img_file, 'image/jpeg')
                    }
                    response = requests.post("http://127.0.0.1:9000/detect", files=files)
                    response.raise_for_status()
            except requests.exceptions.RequestException as e:
                raise UserError(f"💥 Detection API failed: {e}")
            finally:
                # Step 3: Now safe to delete the file
                if os.path.exists(image_path):
                    os.remove(image_path)

            result = response.json()

            if "error" in result:
                raise UserError(f"⚠️ AI Service Error: {result['error']}")

            record.result_image = result["result_image"]
            record.result_filename = result["result_filename"]
            record.confidence = result["confidence"]
            record.detected_at = datetime.now()


    # CRON job
    @api.model
    def cron_example_action(self):
        try:
            _logger.info("⏰ [CRON] AI Detection cleanup started at %s", datetime.now())

            pending_detections = self.search([('result_image', '=', False)])
            _logger.info("🔎 Found %s pending detections to process.", len(pending_detections))

            if len(pending_detections) > 50:
                _logger.warning("⚠️ High backlog: %s unprocessed detections!", len(pending_detections))

            # Archive detections older than 90 days
            old_entries = self.search([('upload_date', '<', datetime.now() - timedelta(days=90))])
            old_entries.write({'active': False})
            _logger.info("📦 Archived %s old detection records.", len(old_entries))

        except Exception as e:
            _logger.error("❌ CRON job error: %s", str(e))
            raise UserError(f"CRON job failed: {e}")
