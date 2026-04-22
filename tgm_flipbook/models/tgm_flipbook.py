import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TgmFlipbook(models.Model):
    _name = 'tgm.flipbook'
    _description = 'Flipbook (Live PDF render)'
    _order = 'sequence, id'

    name = fields.Char(string='Title', required=True)
    slug = fields.Char(
        string='URL Slug',
        required=True,
        help='URL path segment, e.g. "spring-2026" exposes the book at /flipbook/spring-2026',
    )
    sequence = fields.Integer(default=10)
    description = fields.Html(string='Description', sanitize=True)

    # Uploaded via /tgm-flipbook-admin/<id>/upload-pdf, never via the form —
    # base64 round-trips OOM the worker for large PDFs.
    pdf_file = fields.Binary(string='PDF File', attachment=True)
    pdf_filename = fields.Char(string='PDF Filename')

    has_pdf = fields.Boolean(compute='_compute_pdf_meta')
    pdf_size_str = fields.Char(string='PDF Size', compute='_compute_pdf_meta')

    show_cover = fields.Boolean(
        string='Single Cover Page',
        default=True,
        help='Render the first page on its own, then spread the rest in pairs.',
    )

    is_published = fields.Boolean(string='Published on Website', default=False)
    public_url = fields.Char(string='Public URL', compute='_compute_public_url')

    _sql_constraints = [
        ('slug_unique', 'unique(slug)', 'Another flipbook is already using this URL slug.'),
    ]

    @api.depends('slug')
    def _compute_public_url(self):
        for rec in self:
            rec.public_url = f'/flipbook/{rec.slug}' if rec.slug else False

    def _compute_pdf_meta(self):
        rows = self.env['ir.attachment'].sudo().search_read(
            [('res_model', '=', self._name),
             ('res_id', 'in', self.ids),
             ('res_field', '=', 'pdf_file')],
            ['res_id', 'file_size'],
        )
        size_by_id = {r['res_id']: r['file_size'] for r in rows}
        for rec in self:
            size = size_by_id.get(rec.id, 0)
            rec.has_pdf = bool(size)
            if size >= 1024 * 1024:
                rec.pdf_size_str = f'{size / (1024 * 1024):.1f} MB'
            elif size > 0:
                rec.pdf_size_str = f'{size / 1024:.1f} KB'
            else:
                rec.pdf_size_str = '—'

    def action_open_upload(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/tgm-flipbook-admin/{self.id}/upload-pdf',
            'target': 'self',
        }

    @api.constrains('slug')
    def _check_slug_format(self):
        pattern = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
        for rec in self:
            if not pattern.match(rec.slug or ''):
                raise ValidationError(
                    'Slug must be lowercase letters, digits, and single hyphens only '
                    '(e.g. "spring-2026").'
                )
