from wizzi_utils.misc_tools import *  # misc tools
from wizzi_utils import torch_tools as tt  # torch tools
from wizzi_utils import pyplot_tools as pyplt  # pyplot tools
from wizzi_utils import algorithms as algs  # known algorithms
from wizzi_utils import open_cv_tools as cvt  # cv2 tools
from wizzi_utils import coreset_tools as cot  # coreset tools
from wizzi_utils import json_tools as jt  # coreset tools
from wizzi_utils import socket_tools as st  # coreset tools


def main():
    print(to_str(var=3, title='3'))
    tt.main()
    pyplt.main()
    algs.main()
    cvt.main()
    cot.main()
    jt.main()
    st.main()
    return


if __name__ == '__main__':
    main_wrapper(
        main_function=main,
        cuda_off=True,
        torch_v=True,
        tf_v=False,
        cv2_v=True,
        with_profiler=False
    )
