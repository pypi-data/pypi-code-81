"""Utilities for Kindle Model.

- Author: Jongkuk Lim
- Contact: lim.jeikei@gmail.com
"""
from __future__ import annotations

import os
import time
from typing import (TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple,
                    Union)

import numpy as np
import torch
import torch.nn as nn
from tqdm import tqdm

if TYPE_CHECKING:
    from kindle.generator.base_generator import GeneratorAbstract


def split_str_line(msg: str, line_limit: int = 30) -> List[str]:
    """Split string with a maximum length of the line.

    Ex) split_str_line("hello world", line_limit=5)
        will return ["hello", " worl", "d"]

    Args:
        msg: message to split.
        line_limit: limit length of the line.

    Returns:
        list of the split message.
    """
    msg_list = []
    for j in range(0, len(msg), line_limit):
        end_idx = j + line_limit
        msg_list.append(msg[j:end_idx])

    return msg_list


class ModelProfiler:
    """Model time consumption profiler."""

    def __init__(
        self,
        model: nn.Module,
        n_run: int = 100,
        input_size: Tuple[int, int] = (128, 128),
        batch_size: int = 1,
    ) -> None:
        """Initialize model profiler.

        Args:
            model: kindle.Model instance for profiling.
            n_run: number of inference to run.
            input_size: input size to test.
                    If model config contains "input_size", this will be ignored.
            batch_size: batch size to test.
        """
        self.model = model
        self.n_run = n_run
        self.input_size: Tuple[int, ...] = (
            batch_size,
            self.model.model_parser.cfg["input_channel"],  # type: ignore
        )

        if "input_size" in self.model.model_parser.cfg:  # type: ignore
            self.input_size += tuple(self.model.model_parser.cfg["input_size"])  # type: ignore
        else:
            self.input_size += input_size

        self.profile_result = [
            {"name": module.name, "time": np.zeros(self.n_run)}
            for module in self.model.model  # type: ignore
        ]
        self.n_running = 0

    @property
    def result_array(self) -> np.ndarray:
        """Profiling time result array."""
        return np.array([r["time"] for r in self.profile_result])

    @property
    def mean_run_time(self) -> float:
        """Mean time of the inference."""
        return float(self.result_array.sum(axis=0).mean())

    @property
    def std_run_time(self) -> float:
        """Standard deviation time of the inference."""
        return float(self.result_array.sum(axis=0).std())

    @property
    def total_run_time(self) -> float:
        """Total running time."""
        return float(self.result_array.sum())

    @property
    def sorted_index(self) -> np.ndarray:
        """Sorted indices by time consumption of the modules.

        Ex) First index element is the slowest module index.
        """
        return np.argsort(self.result_array.sum(axis=1))[::-1]

    @property
    def running_ratio(self) -> np.ndarray:
        """Running time consumption ratio of the modules."""
        result_array = self.result_array
        result = result_array.sum(axis=1) / result_array.sum()

        if isinstance(result, np.ndarray):
            result_out = result
        else:
            result_out = np.array(result)

        return result_out

    @torch.no_grad()
    def run(self, verbose: bool = True) -> None:
        """Run profiling.

        Args:
            verbose: print profiling result at the end.
        """
        self.profile_result = [
            {"name": module.name, "time": np.zeros(self.n_run)}
            for module in self.model.model  # type: ignore
        ]

        model_input = torch.zeros(self.input_size).to(
            list(self.model.parameters())[0].device
        )

        for run_idx in tqdm(range(self.n_run), desc="Profiling ..."):
            self.n_running = run_idx
            self.model.forward_once(model_input, profile_func=self._profile_func)  # type: ignore

        if verbose:
            self.print_result()

    def print_result(  # pylint: disable=too-many-locals
        self, sort_by_rank: bool = False
    ) -> None:
        """Print profiling result.

        Args:
            sort_by_rank: print sorted by time consumption rank.
        """

        print(f"Profiling result by {self.n_run:,} times running.", end="")
        if sort_by_rank:
            print(" Sorted by time consumption.")
        else:
            print(" Sorted by running order.")

        msg_title = (
            f"{'idx':>4} | {'Name':>20} | {'Time(Mean)':>10} | "
            f"{'Time(Std)':>10} | {'Time(Total)':>10} | "
            f"{'Rank'} | {'Ratio':>7} | {'Params':>13} |"
        )

        print("-" * len(msg_title))
        print(msg_title)
        print("-" * len(msg_title))

        slow_index = {idx: i for i, idx in enumerate(self.sorted_index)}
        running_ratio = self.running_ratio

        log_msgs = []

        for i, result in enumerate(self.profile_result):
            name = result["name"]
            time_mean = result["time"].mean()
            time_std = result["time"].std()
            time_sum = result["time"].sum()

            time_mean, t_unit = self._time_convert(time_mean)
            time_std, t_unit_std = self._time_convert(time_std)
            time_sum, t_unit_sum = self._time_convert(time_sum)
            log_msg = (
                f"{i:4d} | {name:>20} | {time_mean:7.2f} {t_unit:<2} | "  # type: ignore
                f"{time_std:7.2f} {t_unit_std:<2} | "
                f"{time_sum:8.2f} {t_unit_sum:<2} | "
                f"{slow_index[i]+1:4d} | {running_ratio[i]*100:6.2f}% | "
                f"{self.model.model[i].n_params:13,d} |"
            )
            log_msgs.append(log_msg)

        if sort_by_rank:
            loop: Union[np.ndarray, range] = self.sorted_index
        else:
            loop = range(len(log_msgs))

        for i in loop:
            print(log_msgs[i])

        total_time_mean, t_unit_mean = self._time_convert(self.mean_run_time)
        total_time_std, t_unit_std = self._time_convert(self.std_run_time)
        total_time_sum, t_unit_sum = self._time_convert(self.total_run_time)
        print("-" * len(msg_title))
        print(
            f"Running time\n"
            f" - Total : {total_time_sum:8.2f} {t_unit_sum:<2}\n"
            f" - {'Mean':>5} : {total_time_mean:8.2f} {t_unit_mean:<2}\n"
            f" - {'STD':>5} : {total_time_std:8.2f} {t_unit_std:<2}\n"
        )

    @classmethod
    def _time_convert(cls, x: float) -> Tuple[float, str]:
        """Convert time units.

        Args:
            x: time to be converted (seconds).

        Returns:
            converted time value and its unit
            (seconds, milliseconds, microseconds, nanoseconds, picoseconds, femtoseconds)
        """
        time_units = ["s", "ms", "μs", "ns", "ps", "fs"]
        i = 0
        for i in range(len(time_units)):
            if x > 1.0:
                break
            x *= 1000

        return x, time_units[i]

    def _profile_func(self, module: Callable, x: torch.Tensor, i: int) -> torch.Tensor:
        """Profile callback function for kindle.Model.forward."""
        start_time = time.monotonic()
        y = module(x)
        time_took = time.monotonic() - start_time
        self.profile_result[i]["time"][self.n_running] = time_took

        return y


class ModelInfoLogger:
    """Kindle model information logger.

    This class is used once only on parsing the model.
    """

    def __init__(self, log_shapes: bool = False) -> None:
        """Initialize ModelInfoLogger instance."""
        self.log_shapes = log_shapes
        self.model_log_msg: List[str] = []

    @property
    def head(self) -> str:
        """Head message that contains column names."""
        log = (
            f"{'idx':>3} | {'from':>10} | {'n':>3} | {'params':>8} |"
            f" {'module':>15} | {'arguments':>35} |"
            f" {'in_channel':>10} | {'out_channel':>11} |"
        )
        if self.log_shapes:
            log += f" {'in shape':>15} | {'out shape':>15} |"
        log += f"\n{len(log) * '-'}"

        return log

    @property
    def info(self) -> str:
        """Model information containing head and messages."""
        return self.head + "\n" + "\n".join(self.model_log_msg)

    def add(
        self,
        info: Tuple[int, int, int],
        module: nn.Module,
        module_generator: "GeneratorAbstract",
        args: List[Any],
        kwargs: Optional[Dict[str, Any]] = None,
        in_size: Optional[Union[np.ndarray, List]] = None,
        out_size: Optional[List[int]] = None,
    ) -> None:
        """Add module logging information.

        Args:
            info: (i, idx, repeat) Current parsing information.
            module: Parsed module.
            module_generator: Module generator used to generate module.
            args: Arguments of the module.
            kwargs: Keyword arguments of the module.
            in_size: Input size of the module.
                    Only required when {self.input_size} is not None.
            out_size: Output size of the module
                    Only required when {self.input_size} is not None.
        """
        i, idx, repeat = info

        args = args.copy()
        if module.name == "YamlModule":
            args[0] = args[0].split(os.sep)[-1].split(".")[0]

        args_str = str(args)
        if kwargs is not None:
            args_str += ", "
            for key, val in kwargs.items():
                args_str += f"{key}: {val}, "

            args_str = args_str[:-2]

        args_str_list = split_str_line(args_str, line_limit=35)

        log = [
            f"{i:3d} | {str(idx):>10} | {repeat:3d} |"
            f" {module.n_params:8,d} | {module.name:>15} | {args_str_list[0]:>35} |"
            f" {module_generator.in_channel:>10} | {module_generator.out_channel:>11} |"
        ]
        for j in range(1, len(args_str_list)):
            log.append(
                f"{'':>3} | {'':>10} | {'':>3} |"
                f" {'':>8} | {'':>15} | {args_str_list[j]:>35} |"
                f" {'':>10} | {'':>11} |"
            )

        if self.log_shapes and in_size is not None and out_size is not None:
            in_size_str = str(in_size).replace("\n", ",")
            in_size_str_list = split_str_line(in_size_str, line_limit=15)

            log[0] += f" {in_size_str_list[0]:>15} | {str(out_size):>15} |"

            for j in range(1, len(in_size_str_list)):
                append_msg = f" {in_size_str_list[j]:>15} | {'':>15} |"
                if j < len(log):
                    log[j] += append_msg
                else:
                    append_msg = (
                        f"{'':>3} | {'':>10} | {'':>3} |"
                        f" {'':>8} | {'':>15} | {'':>35} |"
                        f" {'':>10} | {'':>11} |"
                    ) + append_msg

                    log.append(append_msg)

        self.model_log_msg.append("\n".join(log))
