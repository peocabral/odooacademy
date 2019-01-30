from odoo import http

class Openacademy(http.Controller):
    @http.route('/odooacademy/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/odooacademy/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('odooacademy.listing', {
            'root': '/odooacademy',
            'objects': http.request.env['odooacademy.course'].search([]),
        })

    @http.route('/odooacademy/objects/<model("odooacademy.course"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('odooacademy.object', {
            'object': obj
        })
