# models/kt_thue_gtgt.py
from odoo import models, fields, api
from datetime import datetime


class KtThueGtgt(models.Model):
    _name = 'kt.khau.tru.thue.gtgt'
    _description = 'Khai báo thuế GTGT'
    _order = 'ngay_ht desc, so_ct desc'

    def _get_default_so_ct(self):
        return 'New'

    so_ct = fields.Char(
        string='Số chứng từ',
        required=True,
        readonly=True,
        copy=False,
        default=_get_default_so_ct,
        tracking=True
    )

    ky = fields.Selection([
        ('1', 'Tháng 1'),
        ('2', 'Tháng 2'),
        ('3', 'Tháng 3'),
        ('4', 'Tháng 4'),
        ('5', 'Tháng 5'),
        ('6', 'Tháng 6'),
        ('7', 'Tháng 7'),
        ('8', 'Tháng 8'),
        ('9', 'Tháng 9'),
        ('10', 'Tháng 10'),
        ('11', 'Tháng 11'),
        ('12', 'Tháng 12'),
        ('q1', 'Quý I'),
        ('q2', 'Quý II'),
        ('q3', 'Quý III'),
        ('q4', 'Quý IV')
    ], string='Kỳ', required=True, tracking=True)

    nam = fields.Selection(
        selection='_get_nam_selection',
        string='Năm',
        required=True,
        tracking=True
    )

    @api.model
    def _get_nam_selection(self):
        current_year = datetime.now().year
        years = []
        for year in range(current_year - 10, current_year + 10):
            years.append((str(year), str(year)))
        return years

    dien_giai = fields.Text('Diễn giải', tracking=True)
    ngay_ht = fields.Date('Ngày hạch toán', default=fields.Date.context_today, tracking=True)
    ngay_ct = fields.Date('Ngày chứng từ', default=fields.Date.context_today, tracking=True)

    thue_gtgt_duoc_khau_tru = fields.Float('Thuế GTGT được khấu trừ', digits=(16, 2), tracking=True)
    thue_gtgt_dau_ra = fields.Float('Thuế GTGT đầu ra', digits=(16, 2), tracking=True)

    company_id = fields.Many2one(
        'res.company',
        string='Đại học/Trường',
        required=True,
        default=lambda self: self.env.company,
        tracking=True
    )

    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('xac_nhan', 'Đã xác nhận'),
        ('huy', 'Huỷ')
    ], string='Trạng thái', default='nhap', tracking=True)

    tt_ids = fields.One2many('kt.khau.tru.thue.gtgt.ht', 'kt_id', string='Hạch toán')
    move_id = fields.Many2one('account.move', string='Bút toán khấu trừ')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('so_ct', 'New') == 'New':
                # Format: KTGT0001
                sequence = self.env['ir.sequence'].next_by_code('kt.khau.tru.thue.sequence')
                vals['so_ct'] = sequence
        return super().create(vals_list)

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.so_ct} - {dict(record._fields['ky'].selection).get(record.ky)}/{record.nam}"
            result.append((record.id, name))
        return result

    def action_confirm(self):
        for record in self:
            record.trang_thai = 'xac_nhan'

    def action_draft(self):
        for record in self:
            record.trang_thai = 'nhap'

    def action_cancel(self):
        for record in self:
            record.trang_thai = 'huy'
