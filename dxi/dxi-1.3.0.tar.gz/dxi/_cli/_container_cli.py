#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

import click
from dxi._lib.util import boolean_based_system_exit
from dxi.container.dxi_container import DXIContainer
from dxi.container.dxi_container import DXIContainerConstants


@click.group(
    short_help="\b\nPerform Delphix Self-Service Container Operations.\n"
               "[create | refresh | reset | restore | delete | "
               "add-owner \nremove-owner | connection-info | enable | list]"
)
def container():
    """
    Self-Service Container operations
    """
    pass


# List Command
@click.option(
    "--engine",
    default=DXIContainerConstants.ENGINE_ID,
    help="\b\nName of Delphix Engine in the config file.\n"
    "[Default: default]",
)
@click.option(
    "--single-thread",
    help="\b\nRun as a single thread\n"
    "[Default: {}]".format(DXIContainerConstants.SINGLE_THREAD),
    default=DXIContainerConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--config",
    help="Full path to the dxtools.conf file with filename.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log-file-path",
    help="Full path to the logs folder.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=DXIContainerConstants.POLL,
)
@container.command()
def list(engine, single_thread, config, log_file_path, poll):
    """
    List all self-service containers on a given engine
    """
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(ss_container.list())


# Create Container Command
@container.command()
@click.option(
    "--container-name",
    required=True,
    help="Name of the self-service container.",
)
@click.option(
    "--db-name",
    required=True,
    help="\b\nName of the datasets to create the self-service container.\n"
    "If the container should contain multiple datasets,\n"
    "separate the names with colon (:).\n"
    "Sample: db1:db2:db3",
)
@click.option(
    "--template-name",
    required=True,
    help="Name of the parent self-service template for the container.",
)
@click.option(
    "--engine",
    default=DXIContainerConstants.ENGINE_ID,
    help="\b\nName of Delphix Engine in the config file.\n"
    "[Default: default]",
)
@click.option(
    "--config",
    help="Full path to the dxtools.conf file with filename.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log-file-path",
    help="Full path to the logs folder.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--single-thread",
    help="\b\nRun as a single thread\n"
    "[Default: {}]".format(DXIContainerConstants.SINGLE_THREAD),
    default=DXIContainerConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    help="\b\nThe number of seconds to wait between job polls.\n"
    "[Default: {}s]".format(DXIContainerConstants.POLL),
    default=DXIContainerConstants.POLL,
)
def create(
    container_name,
    template_name,
    db_name,
    engine,
    single_thread,
    config,
    log_file_path,
    poll,
):
    """
    Create a self-service container.
    """
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(
        ss_container.create(container_name, template_name, db_name=db_name)
    )


# Delete Container Command
@click.option(
    "--container-name",
    required=True,
    help="Name of the self-service container.",
)
@click.option(
    "--keep-vdbs",
    help="\b\nIf set, deleting the container will not remove \n"
    "the underlying virtual dataset(s)\n"
    "[Default: False]",
    default=False,
    is_flag=True,
)
@click.option(
    "--engine",
    default=DXIContainerConstants.ENGINE_ID,
    help="\b\nName of Delphix Engine in the config file.\n"
    "[Default: default]",
)
@click.option(
    "--config",
    help="Full path to the dxtools.conf file with filename.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log-file-path",
    help="Full path to the logs folder.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--single-thread",
    help="\b\nRun as a single thread\n"
    "[Default: {}]".format(DXIContainerConstants.SINGLE_THREAD),
    default=DXIContainerConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    help="\b\nThe number of seconds to wait between job polls.\n"
    "[Default: {}s]".format(DXIContainerConstants.POLL),
    default=DXIContainerConstants.POLL,
)
@container.command()
def delete(
    container_name,
    keep_vdbs,
    engine,
    single_thread,
    config,
    log_file_path,
    poll,
):
    """
    Delete a self-service container
    """
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(
        ss_container.delete(container_name, keep_vdbs=keep_vdbs)
    )


# Reset Container Command
@container.command()
@click.option(
    "--container-name",
    required=True,
    help="Name of the self-service container.",
)
@click.option(
    "--engine",
    default=DXIContainerConstants.ENGINE_ID,
    help="\b\nName of Delphix Engine in the config file.\n"
    "[Default: default]",
)
@click.option(
    "--config",
    help="Full path to the dxtools.conf file with filename.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log-file-path",
    help="Full path to the logs folder.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--single-thread",
    help="\b\nRun as a single thread\n"
    "[Default: {}]".format(DXIContainerConstants.SINGLE_THREAD),
    default=DXIContainerConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    help="\b\nThe number of seconds to wait between job polls.\n"
    "[Default: {}s]".format(DXIContainerConstants.POLL),
    default=DXIContainerConstants.POLL,
)
def reset(container_name, engine, single_thread, config, log_file_path, poll):
    """
    Undo the last refresh or restore operation on a self-service container.
    """
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(ss_container.reset(container_name))


# Refresh Container Command
@container.command()
@click.option(
    "--container_name",
    required=True,
    help="Name of the self-service container.",
)
@click.option(
    "--engine",
    default=DXIContainerConstants.ENGINE_ID,
    help="\b\nName of Delphix Engine in the config file.\n"
    "[Default: default]",
)
@click.option(
    "--config",
    help="Full path to the dxtools.conf file with filename.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log-file-path",
    help="Full path to the logs folder.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--single-thread",
    help="\b\nRun as a single thread\n"
    "[Default: {}]".format(DXIContainerConstants.SINGLE_THREAD),
    default=DXIContainerConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    help="\b\nThe number of seconds to wait between job polls.\n"
    "[Default: {}s]".format(DXIContainerConstants.POLL),
    default=DXIContainerConstants.POLL,
)
def refresh(
    container_name, engine, single_thread, config, log_file_path, poll
):
    """
    Refresh a self-service container.
    """
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(ss_container.refresh(container_name))


# Restore Container Command
@container.command()
@click.option(
    "--bookmark-name",
    required=True,
    help="Name of the self-service bookmark to restore the container",
)
@click.option(
    "--container-name",
    required=True,
    help="Name of the self-service container.",
)
@click.option(
    "--engine",
    default=DXIContainerConstants.ENGINE_ID,
    help="\b\nName of Delphix Engine in the config file.\n"
    "[Default: default]",
)
@click.option(
    "--config",
    help="Full path to the dxtools.conf file with filename.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log-file-path",
    help="Full path to the logs folder.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--single-thread",
    help="\b\nRun as a single thread\n"
    "[Default: {}]".format(DXIContainerConstants.SINGLE_THREAD),
    default=DXIContainerConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    help="\b\nThe number of seconds to wait between job polls.\n"
    "[Default: {}s]".format(DXIContainerConstants.POLL),
    default=DXIContainerConstants.POLL,
)
def restore(
    container_name,
    bookmark_name,
    engine,
    single_thread,
    config,
    log_file_path,
    poll,
):
    """
    Restore a self-service container to a specific self-service bookmark.
    """
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(
        ss_container.restore(container_name, bookmark_name)
    )


# Lists hierarchy Command
@click.option(
    "--container-name",
    required=True,
    help="Name of the self-service container.",
)
@click.option(
    "--engine",
    default=DXIContainerConstants.ENGINE_ID,
    help="\b\nName of Delphix Engine in the config file.\n"
    "[Default: default]",
)
@click.option(
    "--config",
    help="Full path to the dxtools.conf file with filename.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log-file-path",
    help="Full path to the logs folder.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--single-thread",
    help="\b\nRun as a single thread\n"
    "[Default: {}]".format(DXIContainerConstants.SINGLE_THREAD),
    default=DXIContainerConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    help="\b\nThe number of seconds to wait between job polls.\n"
    "[Default: {}s]".format(DXIContainerConstants.POLL),
    default=DXIContainerConstants.POLL,
)
@container.command()
def connection_info(
    container_name, engine, single_thread, config, log_file_path, poll
):
    """
    List connection information for a self-service container.
    """
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(ss_container.connection_info(container_name))


# Add owner Command
@container.command()
@click.option(
    "--container-name",
    required=True,
    help="Name of the self-service container.",
)
@click.option(
    "--owner-name",
    required=True,
    help="Name of the owner user for the container",
)
@click.option(
    "--engine",
    default=DXIContainerConstants.ENGINE_ID,
    help="\b\nName of Delphix Engine in the config file.\n"
    "[Default: default]",
)
@click.option(
    "--config",
    help="Full path to the dxtools.conf file with filename.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log-file-path",
    help="Full path to the logs folder.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--single-thread",
    help="\b\nRun as a single thread\n"
    "[Default: {}]".format(DXIContainerConstants.SINGLE_THREAD),
    default=DXIContainerConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    help="\b\nThe number of seconds to wait between job polls.\n"
    "[Default: {}s]".format(DXIContainerConstants.POLL),
    default=DXIContainerConstants.POLL,
)
def add_owner(
    owner_name,
    container_name,
    engine,
    single_thread,
    config,
    log_file_path,
    poll,
):
    """
    Add an owner to a self-service container.
    """
    # print(owner_name, container_name)
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(
        ss_container.add_owner(container_name, owner_name)
    )


# Delete owner Command
@container.command()
@click.option(
    "--container-name",
    required=True,
    help="Name of the self-service container.",
)
@click.option(
    "--owner-name",
    required=True,
    help="Name of the owner user for the container",
)
@click.option(
    "--engine",
    default=DXIContainerConstants.ENGINE_ID,
    help="\b\nName of Delphix Engine in the config file.\n"
    "[Default: default]",
)
@click.option(
    "--config",
    help="Full path to the dxtools.conf file with filename.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log-file-path",
    help="Full path to the logs folder.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--single-thread",
    help="\b\nRun as a single thread\n"
    "[Default: {}]".format(DXIContainerConstants.SINGLE_THREAD),
    default=DXIContainerConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    help="\b\nThe number of seconds to wait between job polls.\n"
    "[Default: {}s]".format(DXIContainerConstants.POLL),
    default=DXIContainerConstants.POLL,
)
def remove_owner(
    container_name,
    owner_name,
    engine,
    single_thread,
    config,
    log_file_path,
    poll,
):
    """
    Remove an owner from a self-service container.
    """
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(
        ss_container.remove_owner(container_name, owner_name)
    )
