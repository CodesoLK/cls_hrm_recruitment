from flectra import models, fields, api, _
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
from flectra.exceptions import ValidationError

class contractInherit(models.Model):
    _inherit = 'hr.contract'

    renewed = fields.Boolean('Already renewed', default = False)

    # @api.multi
    # def write(self,vals):
        
    #     if not (self.env.user.has_group('cls_hrm_recruitment.group_director') or self.env.user.has_group('cls_hrm_recruitment.group_hrm_hod')):
    #         vals['state'] = self.state

    #     if vals.get('state'):
    #         if vals['state'] == 'open':
                
    #             permanent =  self.env['hr.employee.category'].search([('name', '=', 'Permanent')],limit=1)
    #             emp = self.env['hr.employee'].search([('id','=', self.employee_id.id)],limit=1)
        

    #             emp.write({
    #                 'category_ids': [(4,permanent.id)]
    #             })



        
            
    #     res = super(contractInherit, self).write(vals)
    #     return res

    
    def change_contract(self):
        
        contracts = self.env['hr.contract'].search([])
        for rec in contracts:    
            rec.search([('trial_date_end', '<=', fields.Date.to_string(datetime.today())),]).write({'state':'open',})
            
    # @api.onchange('state')
    # def change_emp_tag_by_contract(self):

     
    #     permanent =  self.env['hr.employee.category'].search([('name', '=', 'Permanent')],limit=1)
    #     emp = self.env['hr.employee'].search([('id','=', self.employee_id.id)],limit=1)
        

    #     emp.write({
    #         'category_ids': [(4,permanent.id)]
    #     })
    
            
            


class employeeInherit(models.Model):
    _inherit = 'hr.employee'

    agenew = fields.Char('TestAge')
    # changing the user group access for fields 
    # address_home_id = fields.Many2one(
    #     'res.partner', 'Private Address', help='Enter here the private address of the employee, not the one linked to your company.',
    #     groups="hr.group_hr_user,cls_hrm_recruitment.group_director")
    # country_id = fields.Many2one(
    #     'res.country', 'Nationality (Country)', groups="hr.group_hr_user")
    # gender = fields.Selection([
    #     ('male', 'Male'),
    #     ('female', 'Female'),
    #     ('other', 'Other')
    # ], groups="hr.group_hr_user,cls_hrm_recruitment.group_director", default="male")
    # marital = fields.Selection([
    #     ('single', 'Single'),
    #     ('married', 'Married'),
    #     ('cohabitant', 'Legal Cohabitant'),
    #     ('widower', 'Widower'),
    #     ('divorced', 'Divorced')
    # ], string='Marital Status', groups="hr.group_hr_user,cls_hrm_recruitment.group_director", default='single')
    # birthday = fields.Date('Date of Birth', groups="hr.group_hr_user,cls_hrm_recruitment.group_director")
    # ssnid = fields.Char('SSN No', help='Social Security Number', groups="hr.group_hr_user,cls_hrm_recruitment.group_director")
    # sinid = fields.Char('SIN No', help='Social Insurance Number', groups="hr.group_hr_user,cls_hrm_recruitment.group_director")
    # identification_id = fields.Char(string='Identification No', groups="hr.group_hr_user,cls_hrm_recruitment.group_director")
    # passport_id = fields.Char('Passport No', groups="hr.group_hr_user,cls_hrm_recruitment.group_director")
    # bank_account_id = fields.Many2one(
    #     'res.partner.bank', 'Bank Account Number',
    #     domain="[('partner_id', '=', address_home_id)]",
    #     groups="hr.group_hr_user,cls_hrm_recruitment.group_director",
    #     help='Employee bank salary account')
    # permit_no = fields.Char('Work Permit No', groups="hr.group_hr_user,cls_hrm_recruitment.group_director")
    # visa_no = fields.Char('Visa No', groups="hr.group_hr_user,cls_hrm_recruitment.group_director")
    # visa_expire = fields.Date('Visa Expire Date', groups="hr.group_hr_user,cls_hrm_recruitment.group_director")
    # payslip_count = fields.Integer(compute='_compute_payslip_count', string='Payslips', groups="hr_payroll.group_hr_payroll_user,cls_hrm_recruitment.group_director")
    epf_no = fields.Char(string='EPF Number')

    def resign(self):
        self.active = False


    @api.model
    def change_age(self):

        employees = self.env['hr.employee'].search([])
        
        for rec in employees:
            if rec.birthday:
                y= relativedelta(date.today(),datetime.strptime(rec.birthday, "%Y-%m-%d").date()).years
                rec.age = y
            if rec.age >= 55:
                contracts = self.env['hr.contract'].search([('employee_id', '=', rec.id)])
                for c in contracts:
                    if c.renewed != True:
                        c.write({
                            'state': 'pending',
                            'renewed':True,
                        })
    
    # @api.multi
    # def _compute_show_leaves(self):
    #     show_leaves = self.env['res.users'].has_group('hr_holidays.group_hr_holidays_user') or self.env['res.users'].has_group('cls_hrm_recruitment.group_director')
    #     for employee in self:
    #         if show_leaves or employee.user_id == self.env.user:
    #             employee.show_leaves = True
    #         else:
    #             employee.show_leaves = False

            

    