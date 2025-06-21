from odoo import http
from odoo.http import request
import requests, base64, tempfile
import logging
import os

_logger = logging.getLogger(__name__)

class AiDetectionController(http.Controller):

    @http.route('/ai/ping', type='http', auth='public')
    def ping(self, **kwargs):
        return "✅ AI Controller is active"

    @http.route('/ai/routes', type='http', auth='public', csrf=False)
    def debug_routes(self, **kwargs):
        return "✅ This controller is active"

    @http.route('/ai/upload', type='http', auth='user', methods=['POST'], csrf=False)
    def upload_image_for_detection(self, **kwargs):
        image_file = request.httprequest.files.get('image')
        name = kwargs.get('name', 'Unnamed Detection')
        _logger.info(f"🧾 Files received: {list(request.httprequest.files.keys())}")
        _logger.info(f"🧾 Form data received: {kwargs}")

        if not image_file:
            return request.make_response("No image uploaded", status=400)

        _logger.info(f"🧪 Received image file: {image_file.filename}")
        _logger.info(f"🧪 Detection name: {name}")

        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        temp.write(image_file.read())
        temp.flush()

        try:
            with open(temp.name, 'rb') as img:
                image_bytes = img.read()

            files = {'file': (image_file.filename, image_bytes, 'image/jpeg')}
            response = requests.post("http://localhost:9000/detect/", files=files)
            response.raise_for_status()

        except Exception as e:
            _logger.error(f"❌ Error during FastAPI call: {e}")
            return request.make_response("Detection failed", status=500)

        os.unlink(temp.name)

        result = response.json()

        record = request.env['ai.detection'].sudo().create({
            'name': name,
            'image': base64.b64encode(image_bytes).decode(),
            'result_image': base64.b64decode(result['result_image']),
            'confidence': result['confidence'],
            'image_filename': image_file.filename,
            'result_filename': result['result_filename'],
        })

        return request.redirect(f'/web#model=ai.detection&id={record.id}&view_type=form')
