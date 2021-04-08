import in1
import os


def in1_upsample(args):
    """ Upsample your image using in1 from the command line.
    """

    # Define CLI flags to variables
    metrics = args.metrics
    quiet = args.quiet
    api_key = args.api
    source = args.source
    result_path = args.result

    # Ensure given file exists
    msg = f"Input file {source} doesn't exist"
    assert os.path.isfile(source), msg

    # Ensure in1 result has the correct file path
    msg = "{} should be a .tif/.tiff file".format(result_path)
    assert result_path[-4:] == ".tif" or result_path[-5:] == ".tiff", msg

    # Apply super resolution
    if not quiet:
        print("Super-resolving {}...".format(source))

    result, profile, metrics = in1.sisr(source, api_key=api_key, calc_metrics=metrics)

    if not quiet:
        print("Writing image to file...")

    in1.write(result, result_path, profile)

    if not quiet:
        print("Done! See {}".format(result_path))

    if metrics:
        if not quiet:
            print("Writing metrics to file ...")

        in1.write(metrics["fidelity"], "result-fidelity.tif", profile)
        in1.write(metrics["enhancement"], "result-enhancement.tif", profile)

        if not quiet:
            print("Done! See result-fidelity.tif and result-enhancement.tif ")
