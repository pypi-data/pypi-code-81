from django.core.management import call_command


def update_test_with_key(project_name, host, user, git_user_password, key_file):
    call_command('update_project', project_name, host, user, git_user_password, key_file)


def update_test_with_password(project_name, host, user, git_user_password, server_password):
    call_command('update_project', project_name, host, user, git_user_password, f'--password {server_password}')


def build_test(project_name, project_port, host, user, server_password, git_user_password):
    call_command('build_project', project_name, project_port, host, user, server_password, git_user_password)
