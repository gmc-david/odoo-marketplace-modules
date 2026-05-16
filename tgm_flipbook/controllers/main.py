import base64

from odoo import http
from odoo.http import request

PDF_CACHE_SECONDS = 60 * 60 * 24 * 30  # 30 days — the PDF is immutable per upload


class TgmFlipbookController(http.Controller):

    @http.route('/flipbook/<string:slug>', type='http', auth='public', website=True, sitemap=True)
    def flipbook_viewer(self, slug, **kwargs):
        flipbook = self._get_published_flipbook(slug)
        if not flipbook:
            return request.not_found()
        return request.render('tgm_flipbook.flipbook_viewer_page', {
            'flipbook': flipbook,
        })

    @http.route('/flipbook/<string:slug>/file.pdf', type='http', auth='public', website=True)
    def flipbook_pdf(self, slug, **kwargs):
        """Stream the raw PDF to the browser for PDF.js to consume.

        Reads the attachment's filestore file in chunks rather than decoding
        the whole base64 blob into memory. Odoo's werkzeug response will
        stream the generator to the client.
        """
        flipbook = self._get_published_flipbook(slug)
        if not flipbook or not flipbook.pdf_file:
            return request.not_found()

        att = request.env['ir.attachment'].sudo().search([
            ('res_model', '=', 'tgm.flipbook'),
            ('res_id', '=', flipbook.id),
            ('res_field', '=', 'pdf_file'),
        ], limit=1)
        if not att:
            return request.not_found()

        headers = [
            ('Content-Type', 'application/pdf'),
            ('Cache-Control', f'public, max-age={PDF_CACHE_SECONDS}, immutable'),
        ]

        if att.store_fname:
            src_path = att._full_path(att.store_fname)

            def stream():
                with open(src_path, 'rb') as f:
                    while True:
                        chunk = f.read(1024 * 1024)
                        if not chunk:
                            break
                        yield chunk

            try:
                import os
                headers.append(('Content-Length', str(os.path.getsize(src_path))))
            except OSError:
                pass
            return request.make_response(stream(), headers=headers)

        # DB-stored attachment fallback.
        data = base64.b64decode(att.db_datas) if att.db_datas else b''
        headers.append(('Content-Length', str(len(data))))
        return request.make_response(data, headers=headers)

    def _get_published_flipbook(self, slug):
        return request.env['tgm.flipbook'].sudo().search(
            [('slug', '=', slug), ('is_published', '=', True)],
            limit=1,
        )
