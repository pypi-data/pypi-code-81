from rocketchat_API.rocketchat import RocketChat


def add_rocketchat_options(parser):
    group = parser.getgroup("rocketchat")
    group.addoption(
        "--ssl_verify",
        action="store",
        dest="ssl_verify",
        default=True,
        help="Set the TLS certificate verification",
    )
    group.addoption(
        "--rocketchat_server_url",
        action="store",
        dest="rocket_url",
        default=None,
        help="Set rocketchat server url",
    )
    group.addoption(
        "--rocketchat_channel",
        action="store",
        dest="rocket_channel",
        default=None,
        help="Set the channel name to report",
    )
    group.addoption(
        "--rocketchat_username",
        action="store",
        dest="rocket_username",
        default=None,
        help="Set the reporter name",
    )
    group.addoption(
        "--rocketchat_password",
        action="store",
        dest="rocket_password",
        default=None,
        help="Used for authentication to rocketchat by rocket_username",
    )

    group.addoption(
        "--rocketchat_report_link",
        action="store",
        dest="rocket_report_link",
        default=None,
        help="Set the report link",
    )

    group.addoption(
        "--rocketchat_message_prefix",
        action="store",
        dest="rocket_message_prefix",
        default=None,
        help="Set a prefix to come before the test result counts.",
    )

    group.addoption(
        "--rocketchat_timeout",
        action="store",
        dest="rocket_timeout",
        default=10,
        help="Set the report send timeout",
    )

    group.addoption(
        "--rocketchat_success_emoji",
        action="store",
        dest="rocket_success_emoji",
        default=":thumbsup:",
        help="Set emoji for a successful run",
    )

    group.addoption(
        "--rocketchat_failed_emoji",
        action="store",
        dest="rocket_failed_emoji",
        default=":thumbsdown:",
        help="Set emoji for a failed run",
    )


def rocketchat_send_message(test_result, config, exitstatus):
    timeout = config.option.rocket_timeout
    report_link = config.option.rocket_report_link
    server_url = config.option.rocket_url
    channel = config.option.rocket_channel
    ssl_verify = config.option.ssl_verify
    message_prefix = config.option.rocket_message_prefix
    rocket_username = (
        config.option.rocket_username
        if config.option.rocket_username
        else "Regression testing results"
    )
    rocket_pass = config.option.rocket_password
    if int(exitstatus) == 0:
        color = "#56a64f"
        emoji = config.option.rocket_success_emoji
    else:
        color = "#ff0000"
        emoji = config.option.rocket_failed_emoji
    final_results = "Passed=%s Failed=%s Skipped=%s Error=%s XFailed=%s XPassed=%s" % (
        test_result.passed,
        test_result.failed,
        test_result.skipped,
        test_result.error,
        test_result.xfailed,
        test_result.xpassed,
    )
    if report_link:
        final_results = "<%s|%s>" % (report_link, final_results)
    if message_prefix:
        final_results = "%s: %s" % (message_prefix, final_results)

    # # uncomment after fix 3.11.1 rocket issue
    # # https://github.com/RocketChat/Rocket.Chat/issues/20556
    #
    # results_pattern = {
    #     "color": color,
    #     "text": final_results,
    #     "mrkdwn_in": [
    #         "text",
    #         "pretext",
    #     ]
    # }

    rocket_client = RocketChat(
        user=rocket_username,
        password=rocket_pass,
        server_url=server_url,
        timeout=timeout,
        ssl_verify=ssl_verify,
    )

    rocket_client.chat_post_message(
        # attachments=[results_pattern],  # uncomment after fix3.11.1 rocket
        channel=channel,
        alias=rocket_username,
        emoji=emoji,
        text=final_results,
    )
