#!/usr/bin/env python
    # logger = logging.getLogger()
    # print('\033[?25h')
    # sys.exit()
    # stack = Stack(
    #     exc_type='KeyboardInterrupt',
    #     exc_value='User sent CTRL+C to kill the program.',
    #     # is_cause=True,
    # )
    # show_locals = False
    # for frame_summary, line_no in tb.walk_stack(frame):
    #     filename = os.path.abspath(frame_summary.f_code.co_filename)
    #     frame = Frame(
    #         filename=filename,
    #         lineno=line_no,
    #         name=frame_summary.f_code.co_name,
    #         locals={
    #             key: pretty.traverse(
    #                 value,
    #                 max_length=10,
    #                 max_string=88,
    #             )
    #             for key, value in frame_summary.f_locals.items()
    #         }
    #         if show_locals
    #         else None,
    #     )
    #     stack.frames.append(frame)
    # trace = Trace(stacks=[stack])
    # keytb = Traceback(trace=trace, width=100)
    # c = Console()
    # c.print(keytb)
    # raise KeyboardInterrupt('Killed in above stage. Partial files may exist! Re-run '
    #                         'from an earlier stage.')
    # except KeyboardInterrupt as e:
    #     logger.exception('User killed program with CTRL+C.')
    #     pprint(dir(e.__traceback__.tb_frame))
