import os
import time
import json
import traceback
import subprocess
import threading
import logging, logging.config
import importlib.resources
import io
import math
import shutil
from pathlib import Path
from argparse import ArgumentParser

import boto3
from botocore.exceptions import ClientError


# initialize loggers
_logger = logging.getLogger("pgvessel")
logging.getLogger("pgvessel_subprocess")


def get_logging_config_file():
    """Checks if $PG_VESSEL_LOG_CONF points to file for logging config. Returns config meant for logging.config.fileConfig

    :return: Returns config file for logging config.
    :rtype: StringIO, str
    """

    env_key = "PG_VESSEL_LOG_CONF"

    if env_key in os.environ:
        path = Path(os.environ[env_key])

        if path.is_file():
            return str(path)
        else:
            print(f"Warning: $PG_VESSEL_LOG_CONF ('{path}') is not a file. Going to use default log config.")

    # fallback default config
    config_text = importlib.resources.read_text('pgvessel._static_files_', 'logging.conf', 'utf-8')

    return io.StringIO(config_text)

def parse_args():
    """Setup ArgumentParser

    :return: result parser.parse_args()
    """

    parser = \
        ArgumentParser(
            description="Backup tool for postgres. Uses pg_receivewal and pg_basebackup. Uploads files to S3 bucket.",
            epilog="That's all folks!",
        )

    subparser = parser.add_subparsers(dest='command')

    subparser.add_parser(
        'wal-receive',
        help='Start pg_receivewal and upload WAL files to S3 bucket as the files saved to disk. Files are deleted after upload.',
    )

    base_backup_parser = subparser.add_parser(
        'base-backup',
        help='Do a pg_basebackup and upload backup files to S3 bucket. Files are deleted after upload.',
    )

    return parser.parse_args()


def get_conf():
    """Reads environment variables and returns conf-dict.

    :return: Dict with config options.
    :rtype: dict
    """

    env2conf_map = {
        "PG_VESSEL_BUCKET_NAME": 'bucketname',
        "PG_VESSEL_ENDPOINT_URL": 'endpoint_url',
        "PG_VESSEL_HOST": 'host',
        "PG_VESSEL_PORT": 'port',
        "PG_VESSEL_USER": 'user',
        "PG_VESSEL_SLOT": 'slotname',
        "PG_VESSEL_DIR": 'workdir',
    }

    required_conf = [ 'bucketname', 'host', 'user', 'workdir']

    conf = {
        'endpoint_url': None,
        'port': 5432,
        'wait': 1,
        'slotname': 'pgvessel_slot',
        **{ k: None for k in required_conf}
    }

    _logger.info("Detecting env variables...")

    # try to map env variables into conf object
    for ke,kc in env2conf_map.items():

        # if env variable exists, store its value in conf
        if ke in os.environ:
            _logger.debug(f"* Detected ${ke}='{os.environ[ke]}' (setting conf[{kc}])")
            conf[kc] = os.environ[ke]

        # else if the conf does not have a default
        elif kc in required_conf:
            _logger.critical(f"Config parameter '{kc}' is required and not set.")
            exit(2)

    _logger.info(f"-\nCONFIG: {json.dumps(conf, indent=2)}")
    return conf

def get_bucket(conf):
    """Fetches and or creates s3 boto3 bucket resource using conf options.

    :param conf: Config for pgvessel. Can fetch from pgvessel.get_conf()
    :type conf: dict

    :return: S3 bucket
    :rtype: boto3 S3.Bucket
    """

    _logger.debug('Connecting to S3 ..')

    # get bucketname
    bucketname = conf['bucketname']

    # get certain keys from conf
    keys = ['endpoint_url']
    kwargs = { k: conf[k] for k in keys if conf[k] is not None }

    # use kwargs to get s3 resource
    s3 = boto3.resource('s3', **kwargs)

    # get bucket from s3 resource
    bucket = s3.Bucket(bucketname)
    bucket.create()

    return bucket


def get_paths(conf):
    """Creates sub directories in the work directory. Returns a dict of paths.

    :param conf: Config for pgvessel. Can fetch from pgvessel.get_conf()
    :type conf: dict

    :return: dict of paths
    :rtype: dict
    """
    workdir = Path(conf['workdir'])

    if not workdir.is_dir():
        raise Exception(f"'{workdir}' is not a directory.")

    # create wals_dir if not exsists
    wals_dir = workdir/"wals"
    if not wals_dir.is_dir():
        os.mkdir(wals_dir)

    # create base_dir if not exsists
    base_dir = workdir/"base"
    if not base_dir.is_dir():
        os.mkdir(base_dir)

    paths = {
        'workdir': workdir,
        'wals_dir': wals_dir,
        'base_dir': base_dir,
    }

    return paths

def delete_objects(bucket, keys):
    """Deletes objects from S3 bucket provided a list of object keys.

    :param bucket: S3 bucket
    :type bucket: boto3 S3.Bucket

    :param keys: list of string object keys.
    :type bucket: list of strings

    :return: boto3 S3.Bucket.delete_objects return value
    :rtype: dict
    """

    return bucket.delete_objects(
        Delete={
            'Objects': [{'Key': k for k in keys}],
        }
    )

def upload_file(bucket, file_path, object_key):
    """Uploads a file to S3 bucket.

    :param bucket: S3 bucket
    :type bucket: boto3 S3.Bucket

    :param file_path: path to file to upload
    :type file_path: pathlib.Path

    :param object_key: key for the uploaded S3 object
    :type object_key: str

    :raises PermissionError: raised if s3 operation returns a permission denied status.

    :return: True of False for success or fail.
    :rtype: bool
    """

    # try to upload file
    try:
        with open(file_path, "rb") as f:
            ret = bucket.upload_fileobj(f, object_key)
        # return success
        return True

    # handle Client error, if error 403 raise PermissionError
    except ClientError as e:
        # log errors
        _logger.error(e)
        _logger.error("-\n"+json.dumps(e.response, indent=2))

        # access denied, program should stop
        if e.response['ResponseMetadata']['HTTPStatusCode'] == 403:
            raise PermissionError("403 is a critical error code.. exiting ..")

        # return fail
        return False

def upload_dir(bucket, dir_path, key_prefix):
    """Traverses a directory and uploads all files to bucket with key_prefix.
    Uses pgvessel.upload_file().
    Returns an iterable that yields status for each file uploaded.

    :param bucket: S3 bucket
    :type bucket: boto3 S3.Bucket

    :param dir_path: path to dir to upload
    :type dir_path: pathlib.Path

    :param key_prefix: prefix for all the objects that are uploaded
    :type key_prefix: str

    :return: Iterable that yields a tuple with (upload success boolean, uploaded file pathlib.Path object, str object_key)
    :rtype: Iterable[bool, pathlib.Path, str]
    """

    # walk through all files in directory
    for r, d, ff in os.walk(dir_path):
        root = Path(r)

        # loop through files in current dir
        for f in ff:
            # create file Path object
            file = root / f

            # create object_key for S3 bucket
            object_key = key_prefix + str(file.relative_to(dir_path))

            # upload file
            success = upload_file(bucket, file, object_key)

            # yield success, file, object_key
            yield success, file, object_key


def get_wal_files(dir_path):
    """Checks a dir if it has any files that does not end in '.partial'

    :param dir_path: path to dir to upload
    :type dir_path: pathlib.Path

    :return: list of file paths that point all wal files ready for sending.
    :rtype: List[pathlib.Path]
    """

    if not dir_path.is_dir():
        raise TypeError(f"Path '{dir_path}' is not a directory.")

    # list elements that are not directories in dir_path
    files = [ e for e in dir_path.iterdir() if not e.is_dir()]

    # list all files that dont end on '.partial'
    files = [ f for f in files if f.suffix != '.partial' ]

    return files

def watch_upload_wals(bucket, conf, dir_path):
    """Watches the WALs directory, uploads done WAL files to S3, deletes them, then yields results.
    If no files are found: Waits ``conf['wait']`` seconds and yields None.

    :param bucket: S3 bucket
    :type bucket: boto3 S3.Bucket

    :param conf: Config for pgvessel. Can fetch from pgvessel.get_conf()
    :type conf: dict

    :param dir_path: path to WALS directory
    :type dir_path: pathlib.Path

    :return: Iterable that yields a tuple with (upload success boolean, uploaded file pathlib.Path object, str object_key)
    :rtype: Iterable[(bool, pathlib.Path, str) or None]
    """

    _logger.info(f"Start WAL directory watch")
    _logger.info(f"WAL directory: {dir_path}")

    while True:
        _logger.debug("Checking for WAL files")

        wals = get_wal_files(dir_path)

        if len(wals) == 0:
            _logger.debug(f"* Found {len(wals)} files (waiting {conf['wait']} seconds)")
            time.sleep(conf['wait'])
            yield None

        # if results were found
        else:
            _logger.info(f"* Found {len(wals)} files")

            for f in wals:
                _logger.info(f"Uploading '{f}'")

                object_key = "wals/"+f.name

                success = upload_file(bucket, f, object_key)

                if success:
                    _logger.debug("* success")
                    _logger.debug("* deleting file")
                    os.remove(f)
                else:
                    _logger.error("* failed")

                yield success, f, object_key

def subprocess_start(args):
    """Starts a subprocess using subprocess.Popen.
    Also spawns two daemon threads for capturing stdout+stderr and logging them.

    :param args: args to be passed to subprocess.Popen
    :type args: List[str]

    :return: started subprocess.Popen object
    :rtype: subprocess.Popen
    """

    # get subprocess logger
    proc_logger = logging.getLogger("pgvessel_subprocess")

    _logger.info(f"Running subprocess: {args}")

    # start process in the background
    proc = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # define method for thead logging
    def _proxy_lines(pipe, logger, logger_level):
        with pipe:
            for line in pipe:
                logger.log(logger_level, line.decode('utf-8').strip())

    # start threads for reading stdout and stderr
    threading.Thread(target=_proxy_lines, args=[proc.stdout, proc_logger, logging.INFO], daemon=True).start()
    threading.Thread(target=_proxy_lines, args=[proc.stderr, proc_logger, logging.ERROR], daemon=True).start()

    # returns subproces.Popen
    return proc


def subprocess_iter(proc):
    """Iterates in an infinite loop and checks if subprocess has exited. If process has exited Exception is raised.

    :param proc: subprocess object
    :type proc: subprocess.Popen

    :raises Exception: if the process exits.

    :return: iterable with the Popen object from the proc parameter
    :rtype: Iterable[subprocess.Popen]
    """

    while True:

        if proc.poll() is not None:
            raise Exception(f"{proc.args} terminated with returncode: {proc.returncode}")

        yield proc

def wal_receive(bucket, paths, conf):

    # get directory path for saving wal files
    wals_dir = paths['wals_dir']
    _logger.info("wals_dir: {wals_dir}")

    # define pg_receivewal command
    cmd = [
        "pg_receivewal",
        "--directory="+str(wals_dir),
        "--slot="+conf['slotname'],
        "--verbose",
        "--no-loop",
        "--compress=9",
        "--host="+conf['host'],
        "--port="+str(conf['port']),
        "--username="+conf['user'],
    ]

    # create slot
    slot_proc = subprocess_start(
        cmd + [ "--create-slot", "--if-not-exists" ], # pg_receivewal with create-slot params
    )
    slot_proc.wait()
    _logger.info(f"Slot creation exited with returncode: {slot_proc.returncode}")

    # setup iterators for program loop
    process_iter  = subprocess_iter(subprocess_start(cmd))
    wals_uploader = watch_upload_wals(bucket, conf, wals_dir)

    # start program loop
    _logger.info("Start program loop ..")
    for _ in zip(process_iter, wals_uploader):
        pass

    _logger.critical("Program loop stopped!")

    # return exit code for the program
    return 1

def base_backup(bucket, paths, conf):

    # get directory path for saving base backups
    base_dir = paths['base_dir']
    _logger.info("base_dir: {base_dir}")

    # create label for backup
    label = str(math.floor(time.time()))

    # create backup dir with label in name to save backup files to
    backup_dir = base_dir / label

    # define pg_basebackup command
    cmd = [
        "pg_basebackup",
        "--pgdata="+str(backup_dir),
        "--format=tar",
        "--compress=9",
        "--label="+label,
        "--progress",
        "--verbose",
        "--host="+conf['host'],
        "--port="+str(conf['port']),
        "--username="+conf['user'],
    ]

    # start base backup process, wait and check return code
    proc = subprocess_start( cmd )
    proc.wait()
    if proc.returncode != 0:
        raise Exception(f"Backup process exited with returncode: {proc.returncode}")

    # state variables before loop
    success = True
    uploaded_keys = []

    _logger.info(f"Uploading {backup_dir} to S3..")

    # try to upload basebackup directory
    try:

        # iterate through upload_dir
        for status, file, key in \
                upload_dir(bucket, backup_dir, "base/"+label+"/"):

            # log result
            _status = "SUCCESS" if status else "FAILED"
            _logger.debug(f"[{_status}] {file} -> {key}")

            # check if file is uploaded
            if status:
                uploaded_keys.append(key)
            else:
                # if file upload failed raise Exception and terminate process
                _logger.info("Stopping directory upload because of failed file upload..")
                raise Exception(f"Upload of {file} failed!")

    # Catch any exception that happens
    except Exception as e:

        # log error and traceback
        _logger.debug(traceback.format_exc())
        _logger.error(f"Caught error: {e}")

        # mark operation has failed
        success = False

        # try to delete uploaded objects from bucket
        _logger.info(f"Deleting {uploaded_keys} from bucket ..")
        try:
            delete_objects(bucket, uploaded_keys)
        except:
            _logger.critical(f"Could not delete {uploaded_keys} from bucket")

    # delete base backup files regardless if operation was sucessful or not
    finally:
        _logger.info(f"Deleting backup dir ({backup_dir})")
        shutil.rmtree(backup_dir)

    # if everything was good, return returncode 0 ..  else return 1
    if success:
        return 0
    else:
        return 1

# main funtion for module
def main(args, conf):

    # get bucket
    bucket = get_bucket(conf)

    # get/create subdirectories in workdir
    paths = get_paths(conf)

    _logger.info(f"Command: {args.command}")


    # hook command to correct method

    # -> 'wal-receive':
    if args.command == 'wal-receive':
        return wal_receive(bucket, paths, conf)

    # -> 'base-backup':
    elif args.command == 'base-backup':
        return base_backup(bucket, paths, conf)

    # code can never reach this point
    return 0

# entrypoint that works like CLI program
def entrypoint():

    # configure logging
    logging.config.fileConfig(get_logging_config_file())

    # parse command line args
    args = parse_args()

    # get conf
    conf = get_conf()

    returncode = 0

    # try main function, catch errors and log them
    try:
        # run main method and send in (args, conf)
        returncode = main(args, conf)
    except Exception as e:
        # log erros and set return code
        _logger.debug(traceback.format_exc())
        _logger.critical(e)
        returncode = 1

    # return returncode
    return returncode

if __name__ == '__main__':
    exit(entrypoint())


