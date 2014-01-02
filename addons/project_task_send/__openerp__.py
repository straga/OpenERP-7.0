# -*- coding: utf-8 -*-

{
    'name' : 'Project task send',
    'version' : '7.0.0.2',
    'author' : 'Viktor Vorobjov',
    'category': 'Project Management',
    'description' : """

        Send task over email. When create task.
        Create email_template
        Send to assignment (get email from user)
        Subject: Customer : Task name
        Body:
            Task Description
            Context.

    """,
    'website' : 'http://www.prolv.net',
    'depends' : ['project'],
    'data': [
        'task_send_template.xml',

    ],
    'installable': True,
}

