from odoo import models, fields, api, exceptions
from datetime import timedelta
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
    
    @api.multi
    def copy(self, default = None):
        default = dict(default or {})
        
        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of{} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)

    _sql_constraints = [
        ('name_description_check',
        'CHECK(name != description)',
        "The title of the course should not be the description"),

        ('name_unique',
        'UNIQUE(name)',
        "The course title must be unique"),
    ]


# Sessions
class Session(models.Model):
    _name = 'odooacademy.session'
    _description = "OdooAcademy Sessions"

    name = fields.Char(required=True)
    start_date = fields.Date(default = fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string = "Number of Seats")
    active = fields.Boolean(default=True)
    color = fields.Integer()

    instructor_id = fields.Many2one('res.partner', string = "Instructor", domain = ['|',('instructor','=',True),('category_id.name','ilike',"Teacher")])
    course_id = fields.Many2one('odooacademy.course', ondelete = 'cascade', string = "Course", required = True) 
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    taken_seats = fields.Float(string = "Taken seats", compute = '_taken_seats')
    end_date = fields.Date(string = "End Date", store = True, compute = '_get_end_date', inverse='_set_end_date')
    hours = fields.Float(string = "Duration in hours", compute = '_get_hours', inverse='_set_hours')
    attendee_count = fields.Integer(string = "Attendees count", compute = '_get_attendees_count', store = True)

    @api.depends ('seats', 'attendee_ids')
    def _taken_seats(self): 
        for r in self:
            if not r.seats:  
                r.taken_seats = 0.0 
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    @api.onchange('seats','attendee_ids')
    def _verify_seats(self):
        if self.seats < 0:
            return{
                'warning':{
                    'title':"Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            },
        if self.seats < len(self.attendee_ids):
            return{
                'warning': {
                    'title':'Too many attendees',
                    'message': "Increase seats or remove excess attendees",
                },
            }
    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue
            
            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendee(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")

    @api.depends('duration')
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 24
    def _set_hours(self):
        for r in self:
            for r in self:
                r.duration = r.hours / 24
    
    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendee_count = len(r.attendee_ids)

class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean("Instructor", default=False)

    session_ids = fields.Many2many('odooacademy.session', string="Attended Sessions", readonly= True)
    