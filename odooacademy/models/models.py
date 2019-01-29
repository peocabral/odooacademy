from odoo import models, fields, api

class odooacademy(models.Model):
    _name = 'openacademy.openacademy'

    name = fields.Char()

class Course(models.Model):
    _name = 'odooacademy.course'
    _description = "OdooAcademy Courses"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()