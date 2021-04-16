TERM_ID = 'aboveGroundCropResidueRemoved'


def should_run(cycle: dict, primary_product: dict = None):
    return primary_product is not None


def run(cycle: dict, primary_product: dict, total_value: float, practice_value: float, *args):
    return total_value * practice_value
