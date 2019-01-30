from odoo import models, fields, api

class odooacademy(models.Model):
    _name = 'odooacademy'

    name = fields.Char()

class Course(models.Model):
    _name = 'odooacademy.course'
    _description = "OdooAcademy Courses"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()

    responsible_id = fields.Many2one('res.users', ondelete = 'set null', string = "Responsible", index = True)
    session_ids = fields.One2many('odooacademy.session', 'course_id', string="Sessions")
    


# Sessions
class Session(models.Model):
    _name = 'odooacademy.session'
    _description = "OdooAcademy Sessions"

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string = "Number of Seats")

    instructor_id = fields.Many2one('res.partner', string = "Instructor")
    course_id = fields.Many2one('odooacademy.course', ondelete = 'cascade', string = "Course", required = True) 
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean("Instructor", default=False)

    session_ids = fields.Many2many('odooacademy.session', string="Attended Sessions", readonly= True)
    