from odoo import http
from odoo.http import request
import tempfile

class AiDetectionController(http.Controller):

    @http.route('/ai/upload', type='http', auth='user', methods=['POST'], csrf=False)
    def upload_image_for_detection(self, **kwargs):
        image_file = kwargs.get('image')
        name = kwargs.get('name', 'Unnamed Detection')
        result_filename = fields.Char(string="Detected Filename")


        if not image_file:
            return request.make_response("No image uploaded.", status=400)

        # Save to temp file
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        temp.write(image_file.read())
        temp.flush()

        # Call your detection logic
        detection = request.env['ai.detection'].sudo().create_detection(name, temp.name)

        return request.redirect('/web#model=ai.detection&id=%s&view_type=form' % detection.id)
