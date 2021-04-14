{
    "name": "MuK Backend Theme", 
    "summary": "Odoo Community Backend Theme",
    "version": "14.0.1.0.2", 
    "category": "Themes/Backend", 
    "license": "LGPL-3", 
    "author": "MuK IT",
    "website": "http://www.mukit.at",
    'live_test_url': 'https://mukit.at/r/SgN',
    "contributors": [
        "Mathias Markl <mathias.markl@mukit.at>",
    ],
    "depends": [
        "web_editor",
    ],
    "excludes": [
        "web_enterprise",
    ],
    "data": [
        "template/assets.xml",
        "template/web.xml",
        "views/res_users.xml",
        "views/res_config_settings_view.xml",
        "data/res_company.xml",
    ],
    "qweb": [
        "static/src/components/control_panel.xml",
        "static/src/xml/*.xml",
    ],
    "images": [
        'static/description/banner.png',
        'static/description/theme_screenshot.png'
    ],
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "application": False,
    "installable": True,
    "auto_install": False,
    "uninstall_hook": "_uninstall_reset_changes",
}
