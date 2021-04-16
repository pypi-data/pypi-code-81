from cbcdb.main import DBManager

# SSH to Bastion AWS Server
SSH_HOST = '3.22.231.37'
SSH_PORT = 22
SSH_USER = 'ec2-user'
SSHKEYPATH='~/.ssh/cbc-optio-us-east-2-bastion.pem'
REMOTE_BIND_ADDRESS = '3.22.231.37'
REMOTE_BIND_PORT = 5439
LOCAL_BIND_HOST = '127.0.0.1'
LOCAL_BIND_PORT = 5400

# Database
DB_NAME = 'optiorx'
DB_SCHEMA = 'bi'
DB_HOST = 'optiorx.ctzlr9hlwwd7.us-east-2.redshift.amazonaws.com'
DB_USER = 'pipeline'
DB_PASSWORD = 'p*k,E4RH6N7qZ(VQVf'
ENCRYPT = 'yes'

db = DBManager(
    debug_output_mode=True,
    use_ssh=True,
    ssh_key_path=SSHKEYPATH,
    ssh_host=SSH_HOST,
    ssh_port=SSH_PORT,
    ssh_user=SSH_USER,
    ssh_remote_bind_address=REMOTE_BIND_ADDRESS,

    ssh_local_bind_address=LOCAL_BIND_HOST,
    ssh_local_bind_port=LOCAL_BIND_PORT,
    ssh_remote_bind_port=REMOTE_BIND_PORT,
    db_name=DB_NAME,
    db_user=DB_USER,
    db_password=DB_PASSWORD,
    db_schema=DB_SCHEMA,
    db_host=DB_HOST)

res = db.get_sql_list_dicts('select * from bi.transactions limit 5')

a = 0
