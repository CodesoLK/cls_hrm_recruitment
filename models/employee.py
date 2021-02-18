from flectra import models, fields, api, _
from datetime import date,datetime
from dateutil.relativedelta import relativedelta

class contractInherit(models.Model):
    _inherit = 'hr.contract'

    renewed = fields.Boolean('Already renewed', default = False)

    @api.multi
    def write(self,vals):
        
        if not (self.env.user.has_group('cls_hrm_recruitment.group_director') or self.env.user.has_group('cls_hrm_recruitment.group_hrm_hod')):
            vals['state'] = self.state

        if vals['state'] == 'open':
            permanent =  self.env['hr.employee.category'].search([('name', '=', 'Permanent')],limit=1)
            emp = self.env['hr.employee'].search([('id','=', self.employee_id.id)],limit=1)
        

            emp.write({
                'category_ids': [(4,permanent.id)]
            })



        
            
        res = super(contractInherit, self).write(vals)
        return res

    
    def change_contract(self):
        self.search([

            ('trial_date_end', '<=', fields.Date.to_string(datetime.today())),
        ]).write({
            'state':'open',
            })
    
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

    def resign(self):
        self.active = False


    @api.model
    def change_age(self):

        employees = self.env['hr.employee'].search([])
        
        for rec in employees:
            if rec.birthday:
                y= relativedelta(date.today(),datetime.strptime(rec.birthday, "%Y-%m-%d").date()).years
                rec.age = y
            if y >= 55:
                contracts = self.env['hr.contract'].search([('employee_id', '=', rec.id)])
                for c in contracts:
                    if c.renewed != True:
                        c.write({
                            'state': 'pending',
                            'renewed':True,
                        })

            

    