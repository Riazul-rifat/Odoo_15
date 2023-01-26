from odoo import api, fields, models
from datetime import datetime


class ResumeWorkOrder(models.TransientModel):
    _name = 'resume.work.order.wizard'
    resume = fields.Boolean(string='Do you want to set resume time?', required = True, default=False)
    resume_after = fields.Datetime(string='Resume time',)

    def send_email(self):

        data = {
            "resume": self.resume,
            "resume_date": self.resume_after
        }

        if data["resume"]:

            mail_template = self.env.ref('bfil_mrp.resume_email_template')
            workorder_active_id = self.env.context.get("active_id")
            record = self.env['mrp.workorder'].browse(workorder_active_id)
            record.write(
                {
                    'resume_time':data['resume_date']
                }
            )
            mail_template.with_context(data).send_mail(workorder_active_id, force_send=True)

        else:

            mail_template = self.env.ref('bfil_mrp.without_resume_email_template')
            workorder_active_id = self.env.context.get("active_id")
            mail_template.with_context(data).send_mail(workorder_active_id, force_send=True)
            record = self.env['mrp.workorder'].browse(workorder_active_id)
            record.write(
                {
                    'resume_time': None
                }
            )
        work_order = self.env['mrp.workorder'].browse(workorder_active_id)
        if work_order:
            work_order.button_pending()
            work_order.state = 'pause'
