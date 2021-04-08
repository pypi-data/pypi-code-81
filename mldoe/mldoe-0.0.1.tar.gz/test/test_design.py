import mldoe


def test_design_init():
    assert(mldoe.design(16).n_runs == 16)
