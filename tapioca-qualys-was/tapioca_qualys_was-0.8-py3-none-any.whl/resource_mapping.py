# coding: utf-8

RESOURCE_MAPPING = {
    'count_web_applications': {
        'resource': '/qps/rest/3.0/count/was/webapp',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET', 'POST']
    },
    'search_web_applications': {
        'resource': '/qps/rest/3.0/search/was/webapp',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET', 'POST']
    },
    'get_web_application_details': {
        'resource': '/qps/rest/3.0/get/was/webapp/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET']
    },
    'create_web_application': {
        'resource': '/qps/rest/3.0/create/was/webapp',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'update_web_application': {
        'resource': '/qps/rest/3.0/update/was/webapp/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'delete_web_application': {
        'resource': '/qps/rest/3.0/delete/was/webapp/{id_or_filter}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'purge_web_application': {
        'resource': '/qps/rest/3.0/purge/was/webapp/{id_or_filter}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'download-selenium-script': {
        'resource': '/qps/rest/3.0/downloadSeleniumScript/was/webapp',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'authentication_count': {
        'resource': '/qps/rest/3.0/count/was/webappauthrecord',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET', 'POST']
    },
    'search_authentication_record': {
        'resource': '/qps/rest/3.0/search/was/webappauthrecord',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'get_authentication_record_details': {
        'resource': '/qps/rest/3.0/get/was/webappauthrecord/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET']
    },
    'create_authentication_record': {
        'resource': '/qps/rest/3.0/create/was/webappauthrecord',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'update_authentication_record': {
        'resource': '/qps/rest/3.0/update/was/webappauthrecord/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'delete_authentication_record': {
        'resource': '/qps/rest/3.0/delete/was/webappauthrecord/{id_or_filters}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'scan_count': {
        'resource': '/qps/rest/3.0/count/was/wasscan',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET', 'POST']
    },
    'search_scans': {
        'resource': '/qps/rest/3.0/search/was/wasscan',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'get_scan_details': {
        'resource': '/qps/rest/3.0/get/was/wasscan/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'launch_scans': {
        'resource': '/qps/rest/3.0/launch/was/wasscan/',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'retrieve_scan_status': {
        'resource': '/qps/rest/3.0/status/was/wasscan/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET']
    },
    'retrieve_scan_results': {
        'resource': '/qps/rest/3.0/download/was/wasscan/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET']
    },
    'cancel_scan': {
        'resource': '/qps/rest/3.0/cancel/was/wasscan/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET']
    },
    'delete_scan': {
        'resource': '/qps/rest/3.0/delete/was/wasscan/{id_or_filters}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'schedule_count': {
        'resource': '/qps/rest/3.0/count/was/wasscanschedule',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET', 'POST']
    },
    'search_schedule': {
        'resource': '/qps/rest/3.0/search/was/wasscanschedule',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'get_schedule_details': {
        'resource': '/qps/rest/3.0/get/was/wasscanschedule/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET']
    },
    'create_a_schedule': {
        'resource': '/qps/rest/3.0/create/was/wasscanschedule',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'update_schedule': {
        'resource': '/qps/rest/3.0/update/was/wasscanschedule/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'activate_an_existing_schedule': {
        'resource': '/qps/rest/3.0/activate/was/wasscanschedule/{id_or_filters}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'deactivate_schedule': {
        'resource': '/qps/rest/3.0/deactivate/was/wasscanschedule/{id_or_filters}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'delete_schedule': {
        'resource': '/qps/rest/3.0/delete/was/wasscanschedule/{id_or_filters}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'download_schedule': {
        'resource': '/qps/rest/3.0/download/was/wasscanschedule/{id_or_filters}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'report_count': {
        'resource': '/qps/rest/3.0/count/was/report',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET', 'POST']
    },
    'search_report': {
        'resource': '/qps/rest/3.0/search/was/report',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'get_report_details': {
        'resource': '/qps/rest/3.0/get/was/report/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET']
    },
    'get_report_status': {
        'resource': '/qps/rest/3.0/status/was/report/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET']
    },
    'download_report': {
        'resource': '/qps/rest/3.0/download/was/report/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET']
    },
    'send_encrypted_pdf_report': {
        'resource': '/qps/rest/3.0/send/was/report/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'update_report': {
        'resource': '/qps/rest/3.0/update/was/report/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'delete_report': {
        'resource': '/qps/rest/3.0/delete/was/report/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'delete_reports': {
        'resource': '/qps/rest/3.0/delete/was/report',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'create_report': {
        'resource': '/qps/rest/3.0/create/was/report',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'scan_report': {
        'resource': '/qps/rest/3.0/create/was/report',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'scorecard_report': {
        'resource': '/qps/rest/3.0/create/was/report',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'catalog_report': {
        'resource': '/qps/rest/3.0/create/was/report',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'report_template_count': {
        'resource': '/qps/rest/3.0/count/was/reporttemplate',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'search_report_template': {
        'resource': '/qps/rest/3.0/search/was/reporttemplate',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'get_details_of_report_template': {
        'resource': '/qps/rest/3.0/get/was/reporttemplate/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET']
    },
    'option_profile_count': {
        'resource': '/qps/rest/3.0/count/was/optionprofile',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET', 'POST']
    },
    'search_option_profiles': {
        'resource': '/qps/rest/3.0/search/was/optionprofile',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'get_option_profile_details': {
        'resource': '/qps/rest/3.0/get/was/optionprofile/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['GET']
    },
    'create_a_new_option_profile': {
        'resource': '/qps/rest/3.0/create/was/optionprofile',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'update_an_option_profile': {
        'resource': '/qps/rest/3.0/update/was/optionprofile/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'delete_an_option_profile': {
        'resource': '/qps/rest/3.0/delete/was/optionprofile/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'finding_count': {
        'resource': '/qps/rest/3.0/count/was/finding',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'search_findings': {
        'resource': '/qps/rest/3.0/search/was/finding',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'get_finding_details': {
        'resource': '/qps/rest/3.0/get/was/finding/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['Get']
    },
    'ignore_findings': {
        'resource': '/qps/rest/3.0/ignore/was/finding/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'activate_findings': {
        'resource': '/qps/rest/3.0/activate/was/finding',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'edit_finding_severity': {
        'resource': '/qps/rest/3.0/editSeverity/was/finding/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'restore_findings_severity': {
        'resource': '/qps/rest/3.0/restoreSeverity/was/finding/{id}',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'retest_findings': {
        'resource': '/qps/rest/3.0/retest/was/finding/<id>',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    },
    'import_burp_issues': {
        'resource': '/qps/rest/3.0/import/was/burp',
        'docs': 'https://www.qualys.com/docs/qualys-was-api-user-guide.pdf',
        'method': ['POST']
    }
}
