import html
import logging
import os
import tempfile

from werkzeug.utils import secure_filename

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

MAX_UPLOAD_BYTES = 2 * 1024 * 1024 * 1024  # 2 GiB


def _render_upload_page(flipbook, error=None):
    err_html = ''
    if error == 'nofile':
        err_html = '<div class="alert alert-danger">No file was selected.</div>'
    elif error == 'notapdf':
        err_html = '<div class="alert alert-danger">Only .pdf files are accepted.</div>'
    elif error:
        err_html = '<div class="alert alert-danger">Upload failed.</div>'

    max_mb = MAX_UPLOAD_BYTES // (1024 * 1024)
    title = html.escape(flipbook.name or 'Flipbook')
    slug = html.escape(flipbook.slug or '')
    back_url = f'/odoo/action-tgm_flipbook.action_tgm_flipbook/{flipbook.id}'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Upload PDF — {title}</title>
<link rel="stylesheet" href="/web/static/lib/bootstrap/dist/css/bootstrap.css"/>
<style>
  body {{ background: #f6f5f1; padding-top: 2rem; }}
  .card {{ box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 0; }}
  progress {{ height: 14px; width: 100%; }}
</style>
</head>
<body>
<div class="container" style="max-width: 720px;">
  <div class="card p-4">
    <h2 class="mb-1">Upload PDF</h2>
    <p class="text-muted">Catalogue: <b>{title}</b> <span class="ms-2"><code>{slug}</code></span></p>
    {err_html}
    <form method="POST" enctype="multipart/form-data" id="flipbook-upload-form">
      <div class="mb-3">
        <label class="form-label" for="pdf">PDF file</label>
        <input type="file" name="pdf" id="pdf" accept=".pdf,application/pdf" class="form-control" required/>
        <div class="form-text">Max {max_mb} MB. Streams in chunks — your browser won't freeze.</div>
      </div>
      <div class="mb-3">
        <progress id="upload-progress" value="0" max="100" style="display:none;"></progress>
        <div id="upload-status" class="text-muted small mt-1"></div>
      </div>
      <div class="d-flex gap-2">
        <button type="submit" class="btn btn-primary">Upload</button>
        <a href="{back_url}" class="btn btn-link">Back</a>
      </div>
    </form>
  </div>
</div>
<script>
(function () {{
  var form = document.getElementById('flipbook-upload-form');
  form.addEventListener('submit', function (e) {{
    e.preventDefault();
    var fileInput = form.querySelector('input[type=file]');
    if (!fileInput.files.length) return;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', window.location.pathname, true);
    var progress = document.getElementById('upload-progress');
    var status = document.getElementById('upload-status');
    var submitBtn = form.querySelector('button[type=submit]');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Uploading…';
    progress.style.display = 'block';
    xhr.upload.onprogress = function (ev) {{
      if (!ev.lengthComputable) return;
      var pct = (ev.loaded / ev.total) * 100;
      progress.value = pct;
      var mbDone = (ev.loaded / 1048576).toFixed(1);
      var mbTot = (ev.total / 1048576).toFixed(1);
      status.textContent = 'Uploading ' + pct.toFixed(1) + '% — ' + mbDone + ' / ' + mbTot + ' MB';
    }};
    xhr.onload = function () {{
      if (xhr.status >= 200 && xhr.status < 400) {{
        status.textContent = 'Upload complete. Redirecting…';
        window.location.href = xhr.responseURL || window.location.href;
      }} else {{
        submitBtn.disabled = false;
        submitBtn.textContent = 'Upload';
        status.textContent = 'Upload failed (HTTP ' + xhr.status + ').';
      }}
    }};
    xhr.onerror = function () {{
      submitBtn.disabled = false;
      submitBtn.textContent = 'Upload';
      status.textContent = 'Upload error — network interrupted?';
    }};
    xhr.send(new FormData(form));
  }});
}})();
</script>
</body>
</html>"""


class TgmFlipbookAdminController(http.Controller):

    @http.route(
        '/tgm-flipbook-admin/<int:flipbook_id>/upload-pdf',
        type='http',
        auth='user',
        methods=['GET', 'POST'],
        csrf=False,
        max_content_length=MAX_UPLOAD_BYTES,
    )
    def upload_pdf(self, flipbook_id, **kwargs):
        if not request.env.user.has_group('website.group_website_designer'):
            return request.not_found()

        flipbook = request.env['tgm.flipbook'].browse(flipbook_id).exists()
        if not flipbook:
            return request.not_found()

        if request.httprequest.method == 'GET':
            body = _render_upload_page(flipbook, error=kwargs.get('error'))
            return request.make_response(
                body,
                headers=[('Content-Type', 'text/html; charset=utf-8')],
            )

        file_storage = request.httprequest.files.get('pdf')
        if not file_storage or not file_storage.filename:
            return request.redirect(f'/tgm-flipbook-admin/{flipbook_id}/upload-pdf?error=nofile')
        if not file_storage.filename.lower().endswith('.pdf'):
            return request.redirect(f'/tgm-flipbook-admin/{flipbook_id}/upload-pdf?error=notapdf')

        filename = secure_filename(file_storage.filename) or 'catalogue.pdf'

        tmp = tempfile.NamedTemporaryFile(prefix='tgm-flipbook-upload-', suffix='.pdf', delete=False)
        tmp.close()
        with open(tmp.name, 'wb') as dst:
            file_storage.save(dst)
        size = os.path.getsize(tmp.name)

        try:
            old = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'tgm.flipbook'),
                ('res_id', '=', flipbook.id),
                ('res_field', '=', 'pdf_file'),
            ])
            old.unlink()

            with open(tmp.name, 'rb') as f:
                raw = f.read()

            request.env['ir.attachment'].sudo().create({
                'name': filename,
                'type': 'binary',
                'res_model': 'tgm.flipbook',
                'res_id': flipbook.id,
                'res_field': 'pdf_file',
                'raw': raw,
            })
            del raw

            flipbook.sudo().write({'pdf_filename': filename})
            _logger.info(
                'Flipbook %s: PDF uploaded (%s bytes, %s)',
                flipbook.slug, size, filename,
            )
        finally:
            try:
                os.unlink(tmp.name)
            except OSError:
                pass

        return request.redirect(f'/odoo/action-tgm_flipbook.action_tgm_flipbook/{flipbook.id}')
