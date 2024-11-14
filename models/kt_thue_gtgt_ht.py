from odoo import models, fields, api


class KtThueGtgtHt(models.Model):
    _name = 'kt.khau.tru.thue.gtgt.ht'
    _description = 'Hạch toán khấu trừ thuế GTGT'

    kt_id = fields.Many2one('kt.khau.tru.thue.gtgt', string='Hạch toán', required=True)
    dien_giai = fields.Text('Diễn giải')

    # Tài khoản nợ
    tk_no_id = fields.Many2one('account.account',
                               string='Tài khoản nợ',
                               required=True,
                               domain=[('deprecated', '=', False)],  # Chỉ hiển thị các TK còn active
                               )
    ma_tk_no = fields.Char(
        'Mã tài khoản nợ',
        related='tk_no_id.code',  # Lấy mã TK từ trường code của account.account
        readonly=True,
        store=True,
    )
    ten_tk_no = fields.Char(
        'Tên tài khoản nợ',
        related='tk_no_id.name',  # Lấy tên TK từ trường name của account.account
        readonly=True,
        store=True,
    )

    # Tài khoản có
    tk_co_id = fields.Many2one('account.account',
                               string='Tài khoản có',
                               required=True,
                               domain=[('deprecated', '=', False)],  # Chỉ hiển thị các TK còn active
                               )
    ma_tk_co = fields.Char(
        'Mã tài khoản có',
        related='tk_co_id.code',  # Lấy mã TK từ trường code của account.account
        readonly=True,
        store=True,
    )
    ten_tk_co = fields.Char(
        'Tên tài khoản có',
        related='tk_co_id.name',  # Lấy tên TK từ trường name của account.account
        readonly=True,
        store=True,
    )

    so_tien = fields.Float('Số tiền', digits=(16, 2), required=True)

    @api.onchange('tk_no_id')
    def _onchange_tk_no(self):
        """Tự động cập nhật mã và tên TK nợ khi thay đổi tk_no_id"""
        if self.tk_no_id:
            self.ma_tk_no = self.tk_no_id.code
            self.ten_tk_no = self.tk_no_id.name
        else:
            self.ma_tk_no = False
            self.ten_tk_no = False

    @api.onchange('tk_co_id')
    def _onchange_tk_co(self):
        """Tự động cập nhật mã và tên TK có khi thay đổi tk_co_id"""
        if self.tk_co_id:
            self.ma_tk_co = self.tk_co_id.code
            self.ten_tk_co = self.tk_co_id.name
        else:
            self.ma_tk_co = False
            self.ten_tk_co = False