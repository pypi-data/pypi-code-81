#!/usr/bin/env python

import json
import os
import time

import click
import yaml
from junitparser import TestCase, TestSuite, JUnitXml, Error

from . import api, schema, term

pipeline_running_states = ['running', 'waiting_for_resource', 'pending']


def validate_env_vars():
    expected = ['GITLAB_ACCESS_TOKEN']
    for key in expected:
        if key not in os.environ:
            term.error('Missing ' + key)
            exit(1)


def log_validation_errors(errors, prefix=''):
    if type(errors) is dict:
        for key in errors:
            term.error('%s- %s ' % (prefix, key))
            log_validation_errors(errors[key], prefix + '  ')
    elif type(errors) is list:
        for item in errors:
            if type(item) in [dict, list]:
                log_validation_errors(item, prefix)
            elif type(item) is str:
                term.error('%s- %s' % (prefix, item))
            else:
                term.error(json.dumps(item, indent=2))
    else:
        term.error(json.dumps(errors, indent=2))


def validate_tests(tests, test_suite_name, junit):
    final_result = True
    suite = TestSuite(test_suite_name)
    for name, definition in tests:
        result, errors = schema.validate_test(definition)
        final_result = final_result * result
        if result:
            term.success('✓ %s is a valid test definition' % name)
        else:
            message = '✗ %s is not a valid test definition' % name
            term.error(message)
            log_validation_errors(errors)
            case = TestCase(name)
            case.result = Error(message)
            case.system_err = json.dumps(errors, indent=2)
            suite.add_testcase(case)
    if not final_result:
        if junit:
            junit_xml = JUnitXml()
            junit_xml.add_testsuite(suite)
            junit_xml.write('rptf-report.junit.xml')
        exit(1)


def execute_test(name, trigger, assertions):
    term.text(trigger['project_id'])


@click.command()
@click.option('--target',
              default='rptf.yml',
              help='File with test cases',
              type=click.Path(exists=True,
                              file_okay=True,
                              dir_okay=False,
                              resolve_path=True, ), )
@click.option('--junit/--no-junit',
              default=True,
              help='Generate JUnit test report', )
def main(target, junit):
    term.empty_line()
    term.header('Remote Pipeline Test Framework')
    validate_env_vars()
    term.empty_line()
    term.text('      Target: %s' % target)
    term.text('JUnit Report: %s' % junit)
    with open(target) as content:
        content = yaml.load(content, Loader=yaml.FullLoader)
        tests = content.items()
        term.empty_line()
        term.header('Validating %s test definitions' % len(tests))

        # validate
        validate_tests(tests, target, junit)

        # trigger
        term.empty_line()
        term.header('Triggering pipelines')
        triggered_pipelines = {}
        assertions = {}
        for name, definition in tests:
            trigger = definition['trigger']
            assertions[name] = definition['assertions']
            project_id = trigger['project_id']
            ref = trigger.get('ref', None)
            if not ref:
                ref = trigger.get('branch', 'master')
            variables = trigger.get('variables', {})
            pipeline_id, url = api.trigger_pipeline(project_id=project_id,
                                                    ref=ref,
                                                    variables=variables)
            triggered_pipelines[name] = {'project_id':      project_id,
                                         'pipeline_id':     pipeline_id,
                                         'pipeline_status': 'running'}
            term.success('✓ %s' % (name))
            term.text('   %s' % (url))

        # watch
        term.empty_line()
        term.header('Waiting')
        first_pass = True
        still_running = True
        while first_pass or still_running:
            first_pass = False
            time.sleep(10)
            for name in triggered_pipelines:
                project_id = triggered_pipelines[name]['project_id']
                pipeline_id = triggered_pipelines[name]['pipeline_id']
                if triggered_pipelines[name]['pipeline_status'] in pipeline_running_states:
                    pipeline = api.get_pipeline(project_id=project_id, pipeline_id=pipeline_id)
                    triggered_pipelines[name]['pipeline_status'] = pipeline['status']
                    term.text('  %s: %s' % (name, pipeline['status']))
            still_running = False
            for name in triggered_pipelines:
                status = triggered_pipelines[name]['pipeline_status']
                if status in pipeline_running_states:
                    still_running = True
        term.text('  ✓ All pipelines finished running')

        # assertions
        assertion_failures = []
        suite = TestSuite(target)

        # assert pipeline status
        term.empty_line()
        term.header('Pipeline status')
        for name in assertions:
            actual = triggered_pipelines[name]['pipeline_status']
            expected = assertions[name]['pipeline_status']
            if actual == expected:
                term.success('✓ %s' % name)
            else:
                message = '✗ %s pipeline status assertion failed \n' \
                          'Expected: %s \n' \
                          '  Actual: %s' % (name, expected, actual)
                term.error(message)
                case = TestCase(name)
                case.result = Error(message)
                case.system_err = message
                suite.add_testcase(case)
                assertion_failures.append('Test case "%s" failed. Expected "%s", actual "%s".' % (name, expected, actual))

        # assert job count
        term.empty_line()
        term.header('Job count')
        jobs = {}
        for name in assertions:
            if 'job_count' in assertions[name]:
                expected = assertions[name]['job_count']
                project_id = triggered_pipelines[name]['project_id']
                pipeline_id = triggered_pipelines[name]['pipeline_id']
                jobs[name] = api.get_jobs(project_id=project_id, pipeline_id=pipeline_id)
                actual = len(jobs[name])
                if actual == expected:
                    term.success('✓ %s' % name)
                else:
                    message = '✗ %s job count assertion failed \n' \
                              'Expected: %s \n' \
                              '  Actual: %s' % (name, expected, actual)
                    term.error(message)
                    case = TestCase(name)
                    case.result = Error(message)
                    case.system_err = message
                    suite.add_testcase(case)
                    assertion_failures.append('Test case "%s" failed. Expected "%s", actual "%s".' % (name, expected, actual))

        # assert job status
        term.empty_line()
        term.header('Job status')
        for name in assertions:
            if 'job_status' in assertions[name]:
                expected_job_status = assertions[name]['job_status']
                if name not in jobs:
                    project_id = triggered_pipelines[name]['project_id']
                    pipeline_id = triggered_pipelines[name]['pipeline_id']
                    jobs[name] = api.get_jobs(project_id=project_id, pipeline_id=pipeline_id)
                actual_job_status = {}
                for job in jobs[name]:
                    actual_job_status[job['name']] = job['status']
                for job_name in expected_job_status:
                    expected = expected_job_status[job_name]
                    if job_name not in actual_job_status:
                        message = '✗ %s.%s job status assertion failed \n' \
                                  'Expected: %s \n' \
                                  '  Actual: %s' % (name, job_name, expected, 'Not found')
                        term.error(message)
                        case = TestCase(name)
                        case.result = Error(message)
                        case.system_err = message
                        suite.add_testcase(case)
                        assertion_failures.append('Test case "%s" failed. Expected "%s", actual "%s".' % (name, expected, 'Not found'))
                    else:
                        actual = actual_job_status[job_name]
                        if expected == actual:
                            term.success('✓ %s    %s' % (name, job_name))
                        else:
                            message = '✗ %s.%s job status assertion failed \n' \
                                      'Expected: %s \n' \
                                      '  Actual: %s' % (name, job_name, expected, actual)
                            term.error(message)
                            case = TestCase(name)
                            case.result = Error(message)
                            case.system_err = message
                            suite.add_testcase(case)
                            assertion_failures.append('Test case "%s" failed. Expected "%s", actual "%s".' % (name, expected, 'Not found'))

        # Result
        term.empty_line()
        term.header('Result')
        assertion_failures_count = len(assertion_failures)
        if assertion_failures_count > 0:
            term.error('✗ %s assertion failure%s' % (assertion_failures_count, 's' if assertion_failures_count > 1 else ''))
            if junit:
                junit_xml = JUnitXml()
                junit_xml.add_testsuite(suite)
                junit_xml.write('rptf-report.junit.xml')
            exit(1)
        else:
            term.success('✓ Success')


if __name__ == '__main__':
    main()
