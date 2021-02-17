from flectra import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta

class contractInherit(models.Model):
    _inherit = 'hr.contract'

    @api.multi
    def write(self,vals):
        
        if not (self.env.user.has_group('cls_hrm_recruitment.group_director') or self.env.user.has_group('cls_hrm_recruitment.group_hrm_hod')):
            vals['state'] = self.state


        
            
        res = super(contractInherit, self).write(vals)
        return res

    
    def change_contract(self):
        self.search([

            ('trial_date_end', '<=', fields.Date.to_string(datetime.today())),
        ]).write({
            'state':'open',
            })
        
            
            


class employeeInherit(models.Model):
    _inherit = 'hr.employee'

    def resign(self):
        self.active = False

    def change_age(self):

        for record in self:
            age = 0
            if record.birthday:
                age = relativedelta(
                    fields.Date.from_string(fields.Date.today()),
                    fields.Date.from_string(record.birthday)).years
            record.age = age
            

    