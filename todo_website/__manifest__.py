{
    'name': 'Solicitud de vacaciones Website',
    'description': 'Solicitar vaciones desde el portal Web.',
    'author': 'Victor Manuel Alonso Soto',
    'depends': ['website_form','hr_holidays','hr'],
    'data': [
    	'security/ir.model.access.csv',
        'views/todo_web.xml',
        'views/view.xml',
        'data/config_data.xml',
    ],
}
