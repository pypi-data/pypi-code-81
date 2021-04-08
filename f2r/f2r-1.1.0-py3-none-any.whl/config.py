import os
ali_prefix = os.getcwd()
work_dir = os.path.dirname(os.path.realpath(__file__))
dry_run = False
target_rpm_dir = '/tmp/o2_rpms'
skip_deps = False
force_build = False
log_level='INFO'
s3_bucket='s3://system-configuration/test/'
release_tag='dev'
architecture='slc7_x86-64'
