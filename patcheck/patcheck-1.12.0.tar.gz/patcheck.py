import argparse
import csv
import datetime
import json
import os
import re
import subprocess
import time

FILE_RESULT_HEADERS = ['row_no', 'dataset_name', 'is_user_applied', 'raw_response']

DESCRIPTION = "PAT Check - Validate user permissions on a given GCP datasets"
EPILOG = "This is one of DBD Toolset"

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

DATASET_ID = 'datasetId'
DATASET_REFERENCE = 'datasetReference'


class BqService:
    REGX_ALL_DATASET_NAME = '^[A-Z]{3}_.*$'
    REGX_NORMAL_DATASET_NAME = '^[A-Z]{3}_.+[^5Y]$'
    REGX_5Y_DATASET_NAME = '^[A-Z]{3}_\w+_5Y$'

    def __init__(self, gcp_project_id: str, dataset_mode: str, user_email: str, user_role: str):
        """

        :type user_role: str
        :type user_email: str
        :type dataset_mode: str
        :type gcp_project_id: str
        """
        self.gcp_project_id = gcp_project_id
        self.dataset_mode = dataset_mode
        self.user_email = user_email
        self.user_role = user_role

    @staticmethod
    def _predicate_valid_dbd_dataset(dataset: object, pattern: str) -> bool:
        dataset_id = dataset[DATASET_REFERENCE][DATASET_ID]
        is_match = bool(re.match(pattern, dataset_id))
        return is_match

    @staticmethod
    def predicate_all_dataset(dataset):
        return BqService._predicate_valid_dbd_dataset(dataset, BqService.REGX_ALL_DATASET_NAME)

    @staticmethod
    def predicate_5y_dataset(dataset):
        return BqService._predicate_valid_dbd_dataset(dataset, BqService.REGX_5Y_DATASET_NAME)

    @staticmethod
    def predicate_normal_dataset(dataset):
        return BqService._predicate_valid_dbd_dataset(dataset, BqService.REGX_NORMAL_DATASET_NAME)

    @staticmethod
    def bq_list_all_datasets(gcp_project_id):
        return subprocess.Popen(['bq', 'ls',
                                 '--format', 'json',
                                 '--max_results', '9999999',
                                 '--project_id', gcp_project_id],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

    @staticmethod
    def predicate_bq_data_viewer_role(user_role):
        return lambda access: access['role'] == user_role

    @staticmethod
    def _is_valid_user(user):
        if not user:
            return False
        else:
            return True

    def read_dataset_from_bq(self):
        stdout, stderr = self.bq_list_all_datasets(self.gcp_project_id).communicate()
        all_datasets = json.loads(stdout)
        if self.dataset_mode == '5Y':
            lines = [line[DATASET_REFERENCE][DATASET_ID] for line in
                     list(filter(self.predicate_5y_dataset, all_datasets))]
        elif self.dataset_mode == 'NORMAL':
            lines = [line[DATASET_REFERENCE][DATASET_ID] for line in
                     list(filter(self.predicate_normal_dataset, all_datasets))]
        else:
            lines = [line[DATASET_REFERENCE][DATASET_ID] for line in
                     list(filter(self.predicate_all_dataset, all_datasets))]
        return lines

    def bq_show(self, dataset_id):
        return subprocess.Popen(['bq', 'show',
                                 '--format', 'json',
                                 '--project_id', self.gcp_project_id, dataset_id],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

    def validate_user_permission(self, bq_response) -> (bool, str, object):
        dataset_id = bq_response[DATASET_REFERENCE][DATASET_ID]
        access_users = bq_response['access']
        bq_viewer_users = filter(self.predicate_bq_data_viewer_role(self.user_role),
                                 access_users)
        validated_user = [user for user in bq_viewer_users if
                          ('userByEmail' in user) and (user['userByEmail'] == self.user_email)]
        return self._is_valid_user(validated_user), dataset_id, bq_response


class ProcessOrchestrator:

    def __init__(self, delay, counter):
        self.delay = delay
        self.counter = counter

    def wait_all_until_done(self, initial_action, main_action, iterable):
        processes = []
        for index, item in enumerate(iterable):
            print(item)
            processes.append(initial_action(item))
        while processes:
            for p in processes:
                if p.poll() is not None:
                    if p.stdout is not None:
                        main_action(p, self.counter)
                        self.counter = self.counter + 1
                    processes.remove(p)
                else:
                    print('Processing...')
                    time.sleep(self.delay)


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def load_datasets(dataset_file: str, bq_client: BqService):
    if dataset_file is not None:
        f = open(dataset_file)
        return list(map(lambda line: line.strip(), f.readlines()))
    else:
        return bq_client.read_dataset_from_bq()


def check_permission(bq_service, csv_writer, process, row_no):
    stdout, stderr = process.communicate()
    bq_response = json.loads(stdout)
    is_user_applied, dataset_id, bq_response = bq_service.validate_user_permission(bq_response)
    row = [str(row_no), dataset_id, is_user_applied, json.dumps(bq_response)]
    csv_writer.writerow(row)
    print(row)


def execute(dataset_file, user_email, user_role, batch_size, mode, gcp_project_id):
    bq_service = BqService(gcp_project_id, mode, user_email, user_role)
    process_orchestrator = ProcessOrchestrator(delay=0.5, counter=1)

    print('\n ====================== Loading Datasets ======================')
    dataset_load_start_time = time.time()
    datasets = load_datasets(dataset_file, bq_service)
    total_dataset_load_time = time.time() - dataset_load_start_time
    print('Total Dataset Loading Time(sec): {:.2f}'.format(total_dataset_load_time))

    dataset_chunks = list(chunks(datasets, batch_size))

    start_datetime = datetime.datetime.now()
    total_start_time = time.time()

    print('\n ====================== Start checking permission ======================')
    print('GCP project:', gcp_project_id)
    print('User email:', user_email)
    print('User Role:', user_role)
    if dataset_file is None:
        print('Mode:', mode)
    else:
        print('Dataset file:', dataset_file)
    print('Batch size:', batch_size)
    print('Total dataset:', len(datasets))
    print('Total batch:', str(round(len(datasets) / batch_size)))
    print('Start time:', start_datetime)

    with open('check_result.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(FILE_RESULT_HEADERS)

        for batch_no, dataset_chunk in enumerate(dataset_chunks):
            batch_start_time = time.time()
            print('\n------------- Batch', str(batch_no + 1), ' Size:', len(dataset_chunk), '---------------')

            process_orchestrator.wait_all_until_done(
                initial_action=lambda dataset_id: bq_service.bq_show(dataset_id),
                main_action=lambda process, counter: check_permission(bq_service, csv_writer, process, counter),
                iterable=dataset_chunk
            )

            batch_end_time = time.time() - batch_start_time
            print('\nTotal Batch Processing Time(sec): {:.2f}'.format(batch_end_time))

    end_date_time = datetime.datetime.now()
    total_end_time = time.time() - total_start_time
    print('\n---------------- Completed checking permission ------------------')
    print('Total processing time(sec): {:.2f}'.format(total_end_time))
    print('End time(s):', end_date_time)


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG)

    parser.add_argument(
        '--dataset_file', required=False, type=str, help=(
            "Full path to a dataset file which contains collection of dataset names separated by line. ex: all_datasets_no_5y.csv"
        )
    )

    parser.add_argument(
        '--mode', required=False, default='ALL', type=str, help=(
            "Validate user permission on specific set of datasets \n"
            "\nex. ALL, NORMAL, and 5Y"
        )
    )

    parser.add_argument(
        '--user_email', required=True, type=str, help=(
            "A primary user email to check for the existing permission on given datasets.  "
            "\nex: xxx@yyyy.gserviceaccount.com"
        )
    )

    parser.add_argument(
        '--user_role', default='projects/dbd-sdlc-prod/roles/BigDataViewer', type=str, help=(
            "A dataset user role permission to search for "
            "\ndefault is projects/dbd-sdlc-prod/roles/BigDataViewer"
        )
    )

    parser.add_argument(
        '--gcp_project_id', default='dbd-sdlc-prod', type=str, help=(
            "A GCP project ID name which contains datasets"
            "\ndefault is dbd-sdlc-prod"
        )
    )

    parser.add_argument(
        '--batch_size', default=10, type=int, help=(
            "Number of maxminum requests send to BigQuery.  Default is 10"
        )
    )

    try:
        args = parser.parse_args()
        execute(args.dataset_file, args.user_email, args.user_role, args.batch_size, args.mode, args.gcp_project_id)
        parser.exit(0)
    except Exception as e:
        parser.error(str(e))


main()
