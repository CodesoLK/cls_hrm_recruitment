from flectra import models, fields, api, _

class A1(models.Model):
    _inherit = 'hr.job'

class A2(models.Model):
    _inherit = 'hr.applicant'

class A3(models.Model):
    _inherit = 'hr.recruitment.stage'

class A4(models.Model):
    _inherit = 'hr.applicant.category'

class A5(models.Model):
    _inherit = 'hr.recruitment.degree'

class A6(models.Model):
    _inherit = 'hr.recruitment.source'

class A7(models.Model):
    _inherit = 'hr.department'

class A8(models.Model):
    _inherit = 'resource.resource'

class A9(models.Model):
    _inherit = 'hr.work.location'

class A10(models.Model):
    _inherit = 'hr.employee.line'

class A11(models.Model):
    _inherit = 'resource.calendar'

class A12(models.Model):
    _inherit = 'resource.calendar.attendance'

class A13(models.Model):
    _inherit = 'hr.payslip'

