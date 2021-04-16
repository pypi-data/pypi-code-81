import asyncio
import os
import random
import time
from importlib import reload

from behave import *

import refinitiv.dataplatform as rdp
from env import write_prj_config, remove_prj_config, write_user_config, remove_user_config, parse_path_value
from refinitiv.dataplatform import configure
from tools import create_obj_with_value_by_path, delete_all_custom_config_files_except_default


@given("Old config files deleted")
def step_impl(context):
    remove_prj_config()
    remove_user_config()
    delete_all_custom_config_files_except_default("rdplibconfig.default.json")


@given("Configuration reloaded")
def step_impl(context):
    reload(rdp)
    reload(configure)
    reload(os)


@given("I have been using the Library as dependency in my project")
def step_impl(context):
    reload(rdp)
    reload(configure)
    reload(os)
    assert rdp


@when("I create the '{file_name}' file in the project root directory")
@step("I create the '{file_name}' file in the project root directory")
def step_impl(context, file_name):
    filepath = os.path.join(os.getcwd(), file_name)

    saved_key = "project-config"
    config = {saved_key: "project-config-value"}
    write_prj_config(config, filepath)

    context.saved_key = saved_key
    context.filepath = filepath


@when("I set dataplatform env to '{env_value}' (using '{env_key}')")
@step("I set dataplatform env to '{env_value}' (using '{env_key}')")
def step_impl(context, env_value, env_key):
    env_value = env_value.replace("<project_root>", os.getcwd())
    os.environ[env_key] = env_value


@then("Configuration values saved at '{file_name}' are used in appropriate places of Library")
def step_impl(context, file_name):
    reload(configure)
    assert configure.config.get(context.saved_key) is not None


@when("I don't have the '{file_name}' configuration file at the project root directory")
def step_impl(context, file_name):
    filepath = os.path.join(os.getcwd(), file_name)
    remove_prj_config(filepath)


@then("Default configuration (hardcoded in the Library) is used")
def step_impl(context):
    assert len(configure._config_files_paths) == 3, configure._config_files_paths
    assert 'default' in configure._config_files_paths[2], configure._config_files_paths
    assert configure.config is not None, configure.config


@then("The individual default value is overridden. "
      "All other values come from the default config (hardcoded in the Library config file).")
def step_impl(context):
    reload(configure)
    assert configure.config.get('sessions.platform.default-session.base-url') == context.saved_value


@step("I write there only one parameter from a list of parameters")
def step_impl(context):
    filepath = context.filepath
    saved_value = "my-base-url"
    config = {
        "sessions": {
            "platform": {
                "default-session": {
                    "base-url": saved_value
                }
            }
        }
    }

    write_prj_config(config, filepath)

    context.saved_value = saved_value


@when("I create the '{file_name}' configuration file in directory within the project ('{dir_path}')")
def step_impl(context, file_name, dir_path):
    path = dir_path.replace("<project_root>", os.getcwd())
    config_path = os.path.join(path, file_name)

    os.makedirs(path, exist_ok=True)

    saved_key = "secret-config-key"
    config = {saved_key: "config-value"}
    write_prj_config(config, config_path)

    context.saved_key = saved_key


@then("Config file '{file_name}' in folder '{dir_path}' is used.")
def step_impl(context, file_name, dir_path):
    reload(configure)
    assert configure.config.get(context.saved_key) is not None


@when("I create the '{file_name}' configuration file in the User's Home directory")
def step_impl(context, file_name):
    config_path = os.path.join(os.path.expanduser('~'), file_name)
    saved_key = "user-home-config-key"
    config = {saved_key: "config-value"}
    write_user_config(config, config_path)
    context.saved_key = saved_key


@when("I enable watch mode")
def step_impl(context):
    def on_config_updated():
        pass

    reload(configure)
    configure.enable_watch()
    configure.config.on('update', on_config_updated)


@step("I change/add/remove configuration file")
def step_impl(context):
    filepath = context.filepath
    saved_key = "changed-key"
    config = {saved_key: "changed-value"}
    write_prj_config(config, filepath)
    context.saved_key = saved_key
    time.sleep(1)


@then("A new configuration is applied 'on the fly' while maintaining priority")
def step_impl(context):
    configure.unload()
    value = configure.config.get(context.saved_key)
    assert value is not None, [context.saved_key, value]


@when("I use a template string in the format '{template}'")
def step_impl(context, template):
    filepath = context.filepath
    saved_key = "template-key"
    config = {saved_key: f"{template}"}
    t = template.replace('${', '').replace('}', '')
    c = config
    for k in t.split(':'):
        v = {}
        c[k] = v
        prev = c
        c = v
    prev[k] = 'template-value'
    write_prj_config(config, filepath)
    context.saved_key = saved_key


@then("Appropriate value from the current config file '{template}' will be applied instead of template")
def step_impl(context, template):
    reload(configure)
    v = configure.config.get(template)
    assert v is not None


@when("I use a template string for not exist path in the format '{template}'")
def step_impl(context, template):
    filepath = context.filepath
    saved_key = "template-key"
    config = {saved_key: f"{template}"}
    write_prj_config(config, filepath)
    context.saved_key = saved_key


@then("Template string will not be replaced (value is a string '{template}')")
def step_impl(context, template):
    reload(configure)
    v = configure.config.get(context.saved_key)
    assert v == template


@then("Appropriate value from the environment variables '{template}' will be applied instead of template")
def step_impl(context, template):
    reload(configure)
    v = configure.config.get(context.saved_key)
    env_value = os.environ[template]
    assert v == env_value


@when("I use a template string for get from environment in the format '{template}'")
def step_impl(context, template):
    filepath = context.filepath
    saved_key = "env-template-key"
    config = {saved_key: f"{template}"}
    write_prj_config(config, filepath)
    env_key = template.replace('${', '').replace('}', '')
    os.environ[env_key] = "env-template-value"
    context.saved_key = saved_key


@then("No such env variable - looking for '{template}' field withing the config file to replace the template")
def step_impl(context, template):
    reload(configure)
    v = configure.config.get(context.saved_key)
    try:
        os.environ[template]
        assert False
    except KeyError:
        assert True
    assert v == template
    reload(configure)


@when("I use a template string for not exist environment in the format '{template}'")
def step_impl(context, template):
    filepath = context.filepath
    saved_key = "env-template-key"
    config = {saved_key: f"{template}"}
    write_prj_config(config, filepath)
    env_key = template.replace('${', '').replace('}', '')

    try:
        del os.environ[env_key]
    except KeyError:
        pass

    context.saved_key = saved_key


@given("I have a config file in my project")
def step_impl(context):
    remove_prj_config()
    remove_user_config()
    reload(rdp)
    reload(configure)
    reload(os)
    if os.environ.get('RDPLIB_ENV'):
        del os.environ['RDPLIB_ENV']
    if os.environ.get('RDPLIB_ENV_DIR'):
        del os.environ['RDPLIB_ENV_DIR']
    assert rdp


@when("I don't specify '{key}' endpoints in the configuration file")
@when("I don't specify '{key}' setting in the config file")
def step_impl(context, key):
    try:
        _, session_type, *_ = key.split('.')
        context.session_type = session_type
    except ValueError:
        pass
    context.key_value = configure.get(key)


@then("Default base url '{expected_url}' is used")
def step_impl(context, expected_url):
    session_type = context.session_type
    if session_type == 'desktop':
        session = rdp.DesktopSession("")
        url = session._get_base_url()
    elif session_type == 'platform':
        session = rdp.PlatformSession("", grant=rdp.GrantPassword(username="", password=""))
        url = session._get_rdp_url_root()
    assert expected_url == url, url


@when("I create a desktop session")
def step_impl(context):
    session = rdp.DesktopSession("")
    context.session = session
    context.session_name = session._session_name


@then("Default path for the handshake '{value}' is used")
def step_impl(context, value):
    url = context.session._get_handshake_url(1)
    assert value in url, url


@then("Default platform path for the RDP '{path}' is used")
def step_impl(context, path):
    session_name = context.session_name
    platform_paths = configure.get(configure.keys.desktop_platform_paths(session_name))
    rdp_path = platform_paths.get('rdp')
    assert rdp_path == path, rdp_path


@step("Default platform path for the UDF platform '{path}' is used")
def step_impl(context, path):
    session_name = context.session_name
    platform_paths = configure.get(configure.keys.desktop_platform_paths(session_name))
    udf_path = platform_paths.get('udf')
    assert udf_path == path, udf_path


@when("I set sessions.<name>.default-session.base-url setting to '{domain}'")
def step_impl(context, domain):
    config = {
        "sessions": {
            "platform": {
                "default-session": {
                    "base-url": f"{domain}",
                },
            },
            "desktop": {
                "default-session": {
                    "base-url": f"{domain}",
                }
            }
        }
    }
    write_prj_config(config)


@when('I set "{path}" setting to "{value}"')
@when('I set "{path}" setting in the config file to "{value}"')
def step_impl(context, path, value):
    config = create_obj_with_value_by_path(path, value)
    write_prj_config(config)
    reload(configure)


@then("All the requests, related to this session are send to the specified '{expected_domain}'")
def step_impl(context, expected_domain):
    reload(configure)
    desktop_session = rdp.DesktopSession("")
    desktop_session.set_port_number(8000)
    url = desktop_session._get_rdp_url_root()
    assert expected_domain in url, url
    url = desktop_session._get_handshake_url()
    assert expected_domain in url, url
    url = desktop_session._get_udf_url()
    assert expected_domain in url, url

    platform_session = rdp.PlatformSession("", grant=rdp.GrantPassword(username="", password=""))
    url = platform_session._get_rdp_url_root()
    assert expected_domain in url, url


@then('New host "{expected_value}" is used to retrieve data from the TREP')
def step_impl(context, expected_value):
    reload(configure)
    platform_session = rdp.PlatformSession("", grant=rdp.GrantPassword(username="", password=""))
    host = platform_session._deployed_platform_host
    # TODO: Investigate why platform_session._deployed_platform_host returns None
    assert host == expected_value, host


@then("Default '{key}' '{expected_value}' is used")
def step_impl(context, key, expected_value):
    cfg = context.key_value
    value = cfg.get(key)
    assert value == expected_value, value


@when("Override any of default platform/desktop session configuration (auth, handshake-url, platform-paths)")
def step_impl(context):
    override_value = "override/value"
    config = {
        "sessions": {
            "platform": {
                "default-session": {
                    "auth": {
                        "url": f"{override_value}/auth",
                    }
                },
            },
            "desktop": {
                "default-session": {
                    "platform-paths": {
                        "rdp": f"{override_value}/rdp",
                        "udf": f"{override_value}/udf"
                    },
                    "handshake-url": f"{override_value}/handshake"
                }
            }
        }
    }
    write_prj_config(config)
    context.override_value = override_value


@then("New (overridden) values are used for the sessions configuration")
def step_impl(context):
    reload(configure)

    override_value = context.override_value
    desktop_session = rdp.DesktopSession("")
    desktop_session.set_port_number(8000)
    url = desktop_session._get_udf_url()
    assert override_value in url, url

    url = desktop_session._get_rdp_url_root()
    assert override_value in url, url

    url = desktop_session._get_handshake_url()
    assert override_value in url, url

    platform_session = rdp.PlatformSession("", grant=rdp.GrantPassword(username="", password=""))
    url = platform_session._get_auth_token_uri()
    assert override_value in url, url


@when("Specify 'endpoints' section within 'sessions' configuration")
def step_impl(context):
    endpoint_path = "path/to/endpoint"
    endpoint_name = "search"
    config = {
        "sessions": {
            "platform": {
                "default-session": {
                    "endpoints": {
                        f"{endpoint_name}": {
                            "url": f"{endpoint_path}",
                        }
                    }
                },
            },
            "desktop": {
                "default-session": {
                    "endpoints": {
                        f"{endpoint_name}": {
                            "url": f"{endpoint_path}",
                        }
                    }
                },
            }
        }
    }
    write_prj_config(config)
    context.endpoint_name = endpoint_name
    context.endpoint_path = endpoint_path


@then("This 'sessions' endpoints override common endpoints.")
def step_impl(context):
    reload(configure)
    endpoint_name = context.endpoint_name
    expected_endpoint_path = context.endpoint_path

    platform_session = rdp.PlatformSession("", grant=rdp.GrantPassword(username="", password=""))
    config = platform_session._get_endpoint_config(endpoint_name)
    # TODO investigate  why config fails with None
    path = config.get(f'{endpoint_name}.url')
    assert expected_endpoint_path == path, f"expected={expected_endpoint_path} exist={path}, {endpoint_name}"

    desktop_session = rdp.DesktopSession("")
    config = desktop_session._get_endpoint_config(endpoint_name)
    path = config.get(f'{endpoint_name}.url')
    assert expected_endpoint_path == path, f"expected={expected_endpoint_path} exist={path}, {endpoint_name}"


@then("'{path}' base path is used for the environmental-social-governance content object creation")
def step_impl(context, path):
    session = rdp.PlatformSession("", grant=rdp.GrantPassword(username="", password=""))
    esg = rdp.ESG(session=session)
    url = esg._url
    assert path == url, url


@then("Default base path '{path}' for the environmental-social-governance content object is used")
def step_impl(context, path):
    session = rdp.PlatformSession("", grant=rdp.GrantPassword(username="", password=""))
    esg = rdp.ESG(session=session)
    url = esg._url
    assert path == url, url


@then("Default subpath '{expected_path}' for the '{data_type}' endpoint is used")
@then("'{expected_path}' subpath to receive '{data_type}' data is used")
def step_impl(context, expected_path, data_type):
    session = rdp.PlatformSession("", grant=rdp.GrantPassword(username="", password=""))
    esg = rdp.ESG(session=session)

    if data_type == 'universe':
        path = esg._url_universe
    else:
        path = esg._get_url(data_type)

    assert expected_path in path, path


@when('I set "{path}" setting to random value ({text})')
def step_impl(context, path, text):
    items = text.replace('"', '').split(', ')
    value = random.choice(items)
    context.set_notifications_value = value
    prepared_config = create_obj_with_value_by_path(path, value)
    context.prepared_config = prepared_config
    write_prj_config(prepared_config)
    reload(configure)
    context.log_level = value


@then("Appropriate level for project logger is applied.")
def step_impl(context):
    expected = context.log_level
    session = rdp.DesktopSession("")
    from refinitiv.dataplatform import log
    expected = log.convert_log_level(expected)
    log_level = session.get_log_level()
    assert expected == log_level, log_level


@then('"{expected}" is used as file-name config value.')
def step_impl(context, expected):
    log_filename_value_from_config = configure.get_str(configure.keys.log_filename)
    assert log_filename_value_from_config == expected


@given("I have a config file in my project (watch mode is enabled)")
def step_impl(context):
    config = create_obj_with_value_by_path(configure.keys.watch_enabled, True)
    write_prj_config(config)
    reload(configure)


@when('I change "logs" setting on the fly (level, filter, etc.), (see How config works for supported ways)')
def step_impl(context):
    session = rdp.DesktopSession("")
    log_level = session.get_log_level()
    context.prev_log_level = log_level
    config = create_obj_with_value_by_path(configure.keys.log_level, "warn")
    write_prj_config(config)


@then("The corresponding setting value has been changed to the passed one")
def step_impl(context):
    configure.unload()
    prev_log_level = context.prev_log_level
    session = rdp.DesktopSession("")
    log_level = session.get_log_level()
    assert log_level != prev_log_level, prev_log_level


@then("Default base path '{expected}' for the historical-pricing content object is used")
@then("'{expected}' base path is used for the historical-pricing content object creation")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    pricing = rdp.HistoricalPricing(session)
    url = pricing._endpoint.url
    assert expected == url, url


@then("Default subpath '{expected}' for the historical-pricing events endpoint is used")
@then("'{expected}' subpath to receive historical-pricing events is used")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    pricing = rdp.HistoricalPricing(session)
    try:
        res = pricing._get_events("universe", rdp.EventTypes.QUOTE)
    except rdp.EndpointError:
        pass

    url = pricing._endpoint.url
    assert expected in url, url


@then("Default subpath '{expected}' to receive an appropriate historical-pricing interday summaries is used")
@then("'{expected}' subpath to receive an appropriate historical-pricing interday summaries is used")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    pricing = rdp.HistoricalPricing(session)
    try:
        res = pricing._get_summaries("universe", interval=rdp.Intervals.YEARLY)
    except rdp.EndpointError:
        pass

    url = pricing._endpoint.url
    assert expected in url, url


@then("Default subpath '{expected}' to receive an appropriate historical-pricing intraday summaries is used")
@then("'{expected}' subpath to receive an appropriate historical-pricing intraday summaries is used")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    pricing = rdp.HistoricalPricing(session)
    try:
        pricing._get_summaries("universe", interval=rdp.Intervals.ONE_HOUR)
    except rdp.EndpointError:
        pass

    url = pricing._endpoint.url
    assert expected in url, url


@then("Default subpath '{expected}' for the quantitative-analytics-financial-contracts endpoint is used")
@then("'{expected}' subpath to receive financial-contracts data is used")
@then("Default base path '{expected}' for the quantitative-analytics-financial-contracts content object is used")
@then("'{expected}' base path is used for the quantitative-analytics-financial-contracts content object creation")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    contracts = rdp.ipa.FinancialContracts(session)
    url = contracts.url

    assert expected in url, url


@then("Default subpath '{expected}' for the surfaces endpoint is used")
@then("'{expected}' subpath to receive surfaces data is used")
@then("Default base path '{expected}' for the quantitative-analytics-curves-and-surfaces content object is used")
@then("'{expected}' base path is used for the quantitative-analytics-curves-and-surfaces content object creation")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    contracts = rdp.ipa.surface.Surfaces(session)
    url = contracts.url

    assert expected in url, url


@then("Default subpath '{expected}' for the forward-curves endpoint is used")
@then("'{expected}' subpath to receive forward-curves data is used")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    contracts = rdp.ipa.curve.Curves(session)
    url = contracts.url

    assert expected in url, [configure.config, configure._config_files_paths]


@then("Default base path '{expected}' for the news content object is used")
@then("'{expected}' base path is used for the news content object creation")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    news = rdp.news.News(session)

    url = news._headlines._endpoint_headlines.url
    assert expected in url, url

    url = news._story._endpoint_story.url
    assert expected in url, [configure.config, configure._config_files_paths]


@then("Default subpath '{expected}' for the headlines endpoint is used")
@then("'{expected}' subpath to receive headlines data is used")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    news = rdp.news.News(session)

    url = news._headlines._endpoint_headlines.url
    assert expected in url, [configure.config, configure._config_files_paths]


@then("Default subpath '{expected}' for the news stories endpoint is used")
@then("'{expected}' subpath to receive news stories data is used")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    news = rdp.news.News(session)

    url = news._story._endpoint_story.url
    assert expected in url, [configure.config, configure._config_files_paths]


@then("Default base path '{expected}' for the search content object is used")
@then("'{expected}' base path is used for the search content object creation")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    search = rdp.Search(session)

    url = search._endpoint.url
    assert expected in url, [configure.config, configure._config_files_paths]


@then("Default subpath '{expected}' for the search endpoint is used")
@then("'{expected}' subpath to receive search data is used")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    search = rdp.Search(session)

    url = search._endpoint.url
    assert expected in url, url


@then("Default subpath '{expected}' for the lookup endpoint is used")
@then("'{expected}' subpath to receive lookup data is used")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    lookup = rdp.Lookup(session)

    url = lookup._endpoint.url
    assert expected in url, url


@then("Default subpath '{expected}' for the metadata endpoint is used")
@then("'{expected}' subpath to receive metadata data is used")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    metadata = rdp.ViewMetadata(session)

    url = metadata._url
    assert expected in url, url


@then("'{expected}' base path is used for the datagrid object creation")
@then("Default datagrid base path '{expected}' is used")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    fundamental = rdp.Fundamental(session)

    url = fundamental._endpoint.url
    assert expected in url, url


@then("Default subpath '{expected}' for the datagrid endpoint is used")
@then("'{expected}' subpath to receive info about datagrid data is used")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    fundamental = rdp.Fundamental(session)

    url = fundamental._endpoint.url
    assert expected in url, url


@then("'{expected}' base path is used for the pricing object creation")
@then("Default pricing base path '{expected}' is used")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    pricing = rdp.Pricing(session)

    url = pricing._snapshot_endpoint.url
    assert expected in url, url


@then("Default subpath '{expected}' for the snapshots endpoint is used")
@then("'{expected}' subpath to receive info about snapshots data is used")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    pricing = rdp.Pricing(session)

    url = pricing._snapshot_endpoint.url
    assert expected in url, url


@then("Default subpath '{expected}' for the chains endpoint is used")
@then("'{expected}' subpath to receive info about chains data is used")
def step_impl(context, expected):
    session = rdp.DesktopSession("")
    pricing = rdp.Chain(session)

    url = pricing._endpoint.url
    assert expected in url, url


@then("I receive notifications about changes in configuration file")
def step_impl(context):
    was_update = False

    def on_config_updated():
        nonlocal was_update
        was_update = True

    configure.config.on('update', on_config_updated)
    config = {"foo": "bar"}
    write_prj_config(config)
    reload(configure)
    asyncio.get_event_loop().run_until_complete(asyncio.sleep(3))
    assert was_update is True

    configure.unload()


@then("I do not receive any notifications about changes in the configuration files")
def step_impl(context):
    was_update = False

    def on_config_updated():
        nonlocal was_update
        was_update = True

    configure.config.on('update', on_config_updated)
    config = context.prepared_config
    write_prj_config(config)

    asyncio.get_event_loop().run_until_complete(asyncio.sleep(3))
    assert was_update is False

    configure.unload()


@then("I receive single notification event about each change in the configuration file")
def step_impl(context):
    was_update = False
    num_update = 0

    def on_config_updated():
        nonlocal was_update, num_update
        num_update += 1
        was_update = True

    configure.config.on('update', on_config_updated)
    config = {"foo": "bar"}
    write_prj_config(config, is_remove=False)

    asyncio.get_event_loop().run_until_complete(asyncio.sleep(6))
    assert num_update == 1, num_update
    assert was_update is True


@step("I have the same settings list in the PWD and USER HOMEDIR config files "
      "with different values (e.g. PWD {project}, USER HOMEDIR {user} => final {final})")
def step_impl(context, project, user, final):
    config = create_obj_with_value_by_path(*parse_path_value(project))
    write_prj_config(config, is_remove=False)
    config = create_obj_with_value_by_path(*parse_path_value(user))
    write_user_config(config, is_remove=False)

    reload(configure)

    log_level = configure.get_str(configure.keys.log_level)

    _, value = parse_path_value(final)
    assert log_level == value


@when("I delete PWD config file")
def step_impl(context):
    asyncio.get_event_loop().run_until_complete(asyncio.sleep(6))

    num_update = 0

    def on_config_updated():
        nonlocal num_update
        context.was_update = True
        num_update += 1
        context.num_update = num_update

    configure.config.on('update', on_config_updated)

    remove_prj_config()
    asyncio.get_event_loop().run_until_complete(asyncio.sleep(6))


@then("I receive an event notification with the final object {final} and the source that has been physically modified (PWD).")
def step_impl(context, final):
    log_level = configure.get_str(configure.keys.log_level)
    _, value = parse_path_value(final)
    assert log_level == value, log_level
    assert context.was_update is True
    assert context.num_update == 1, context.num_update


@when("I change settings at an intermediate level that does not affect the final configuration")
def step_impl(context):
    # project's config higher priority
    expected = "debug"
    config = {"logs": {"level": expected}}
    context.expected = expected
    write_prj_config(config)

    config = {"logs": {"level": "warn"}}
    write_user_config(config)

    reload(configure)

    log_level = configure.get_str(configure.keys.log_level)
    assert log_level == expected, log_level

    context.num_update = 0
    context.was_update = False

    def on_config_updated():
        context.was_update = True
        context.num_update += 1

    configure.config.on('update', on_config_updated)

    remove_user_config()
    asyncio.get_event_loop().run_until_complete(asyncio.sleep(6))


@then("I don't receive an event notification")
def step_impl(context):
    expected = context.expected
    log_level = configure.get_str(configure.keys.log_level)
    assert log_level == expected, log_level
    assert context.was_update is False, context.was_update
    assert context.num_update == 0, context.num_update


@given("I do not have my custom configuration file in the project")
def step_impl(context):
    remove_prj_config()
    reload(configure)


@when("I create streaming connections")
def step_impl(context):
    assert rdp.OMMStreamConnection


@then("Default values listed bellow are used.")
def step_impl(context):
    pricing_url = "apis.streaming.pricing.url"
    pricing_path = "apis.streaming.pricing.endpoints.main.path"
    pricing_protocols = "apis.streaming.pricing.endpoints.main.protocols"
    pricing_locations = "apis.streaming.pricing.endpoints.main.locations"
    trading_analytics_url = "apis.streaming.trading-analytics.url"
    trading_analytics_path = "apis.streaming.trading-analytics.endpoints.redi.path"
    trading_analytics_protocols = "apis.streaming.trading-analytics.endpoints.redi.protocols"
    trading_analytics_locations = "apis.streaming.trading-analytics.endpoints.redi.locations"

    text = context.text
    import json
    data = json.loads(text)
    expected_config = configure.ext_config_mod.config_from_dict(data)

    def assert_expected_and_default_configs_equal_by_property(property):
        assert expected_config.get(property) == configure.get(property)

    assert_expected_and_default_configs_equal_by_property(pricing_url)
    assert_expected_and_default_configs_equal_by_property(pricing_path)
    assert_expected_and_default_configs_equal_by_property(pricing_protocols)
    assert_expected_and_default_configs_equal_by_property(pricing_locations)
    assert_expected_and_default_configs_equal_by_property(trading_analytics_url)
    assert_expected_and_default_configs_equal_by_property(trading_analytics_path)
    assert_expected_and_default_configs_equal_by_property(trading_analytics_protocols)
    assert_expected_and_default_configs_equal_by_property(trading_analytics_locations)


@given("I have my custom configuration file in the project")
def step_impl(context):
    config = {"my-key": "my-value"}
    write_prj_config(config)
    reload(configure)


@when("I create ItemStream/StreamingPrice connection without specify an optional parameter 'connection'")
def step_impl(context):
    session = rdp.DesktopSession("")
    stream = rdp.OMMItemStream(session, name="EUR=")
    context.stream = stream


@when("I create ItemStream/StreamingPrice connection")
def step_impl(context):
    session = rdp.DesktopSession("")
    stream = rdp.StreamingPrice(session=session, name='EUR=')
    context.stream = stream


@then("'{expected}' streaming connection is used by default.")
def step_impl(context, expected):
    assert context.stream.connection == expected
