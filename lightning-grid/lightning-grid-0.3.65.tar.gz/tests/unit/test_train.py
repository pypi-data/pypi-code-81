import click
import pytest

from grid.cli.grid_train import _check_is_valid_extension
from grid.cli.grid_train import _check_run_name_is_valid
from grid.cli.grid_train import _resolve_instance_type_nickname
from grid.utilities import check_description_isnt_too_long


class TestTrainCallbacks:
    """Tests callbacks in train."""
    def test_name_callback(self):
        # Run name needs to be alphanumeric
        with pytest.raises(click.ClickException):
            _check_run_name_is_valid(None, None, '$')

        # Run name can't start or end with a dash
        with pytest.raises(click.ClickException):
            _check_run_name_is_valid(None, None, '-run')

        with pytest.raises(click.ClickException):
            _check_run_name_is_valid(None, None, 'run-')

        # Run name can't contain upper case letters
        with pytest.raises(click.ClickException):
            _check_run_name_is_valid(None, None, 'Run')

        # Besides that, run name should work
        assert _check_run_name_is_valid(None, None, 'run')

    def test_nickname(self):
        aws_node_to_nicknames = {
            'p3.16xlarge': '8_v100_16gb',
            'p3dn.24xlarge': '8_v100_32gb',
            'g4dn.metal': '8_t4_16gb',
            'p2.8xlarge': '8_k80_12gb',
            'p3.8xlarge': '4_v100_16gb',
            'g4dn.12xlarge': '4_t4_16gb',
            'g3.16xlarge': '4_m60_8gb',
            'g3.8xlarge': '2_m60_8gb',
            'p3.2xlarge': '1_v100_16gb',
            'p3.2xlarge': '1_V100_16Gb',
            'g4dn.16xlarge': '1_t4_16gb',
            'p2.xlarge': '1_k80_12gb',
            'g3.4xlarge': '1_m60_8gb',
            't2.large': '2_cpu_8gb',
            't2.large': '2_CPU_8GB',
            't2.medium': '2_cpu_4gb'
        }
        for k, v in aws_node_to_nicknames.items():

            assert _resolve_instance_type_nickname(None, None, v) == k

    def test_valid_extension_callback(self):
        """
        _check_is_valid_extension() raises exception if file isn't valid extension
        """
        f = 'foo.txt'
        with pytest.raises(click.BadParameter):
            _check_is_valid_extension(None, None, f)

    def test_check_description_isnt_too_long(self):
        """
        _check_description_isnt_too_long() checks that description isn't
        too long
        """
        d = 'a' * 199
        assert d == check_description_isnt_too_long(None, None, d)

        d = 'a' * 201
        with pytest.raises(click.BadParameter):
            check_description_isnt_too_long(None, None, d)
