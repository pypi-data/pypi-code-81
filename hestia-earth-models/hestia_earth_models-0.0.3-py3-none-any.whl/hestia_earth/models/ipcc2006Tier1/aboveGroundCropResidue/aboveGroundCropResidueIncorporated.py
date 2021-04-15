TERM_ID = 'aboveGroundCropResidueIncorporated'


def should_run(*args): return True


def run(cycle: dict, primary_product: dict, total_value: float, practice_value: float, *args):
    return total_value * practice_value
