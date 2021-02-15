from flectra import models, fields, api, _
from flectra.exceptions import UserError

class recruit(models.Model):
    _inherit = 'hr.applicant'

    marital_status  = fields.Selection([('married', 'Married'),('not_married', 'Not Married'),],string= 'Marital Status')
    gender =  fields.Selection([('male', 'Male'),('female', 'Female'),],string= 'Gender')
    title = fields.Many2one('res.partner.title', string='title')
    emp_type = fields.Selection([('executive', 'Executive'),('nonexec', 'Non Executive'),],string= 'Employee Type')
    stage_check = fields.Boolean('check stage', compute='check_stage_new')

    @api.multi
    def check_stage_new(self):
        for rec in self:
            if rec.stage_id.name == 'Selected':
                rec.stage_check = True
            else:
                rec.stage_check = False


    @api.multi
    def create_employee_from_applicant(self):
        """ Create an hr.employee from the hr.applicants """
        x = self.env['hr.recruitment.stage'].search([('name', '=','Selected')])
        self.stage_id = x
        employee = False
        for applicant in self:
            contact_name = False
            if applicant.partner_id:
                address_id = applicant.partner_id.address_get(['contact'])['contact']
                contact_name = applicant.partner_id.name_get()[0][1]
            else :
                new_partner_id = self.env['res.partner'].create({
                    'is_company': False,
                    'name': applicant.partner_name,
                    'email': applicant.email_from,
                    'phone': applicant.partner_phone,
                    'mobile': applicant.partner_mobile
                })
                address_id = new_partner_id.address_get(['contact'])['contact']
            if applicant.job_id and (applicant.partner_name or contact_name):
                applicant.job_id.write({'no_of_hired_employee': applicant.job_id.no_of_hired_employee + 1})
                employee = self.env['hr.employee'].create({
                    'name': applicant.partner_name or contact_name,
                    'job_id': applicant.job_id.id,
                    'address_home_id': address_id,
                    'department_id': applicant.department_id.id or False,
                    'address_id': applicant.company_id and applicant.company_id.partner_id
                            and applicant.company_id.partner_id.id or False,
                    'work_email': applicant.department_id and applicant.department_id.company_id
                            and applicant.department_id.company_id.email or False,
                    'work_phone': applicant.department_id and applicant.department_id.company_id
                            and applicant.department_id.company_id.phone or False})
                applicant.write({'emp_id': employee.id})
                applicant.job_id.message_post(
                    body=_('New Employee %s Hired') % applicant.partner_name if applicant.partner_name else applicant.name,
                    subtype="hr_recruitment.mt_job_applicant_hired")
                employee._broadcast_welcome()
            else:
                raise UserError(_('You must define an Applied Job and a Contact Name for this applicant.'))

        employee_action = self.env.ref('hr.open_view_employee_list')
        dict_act_window = employee_action.read([])[0]
        if employee:
            dict_act_window['res_id'] = employee.id
        dict_act_window['view_mode'] = 'form,tree'
        return dict_act_window