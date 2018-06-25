import sys
import unittest

import test_headers
from .test_headers import TestHeaders
import test_args
from .test_args import TestArgs
import test_form
from .test_form import TestForm
import test_json
from .test_json import TestJson
import test_handle_errors
from .test_handle_errors import TestHandleErrors


def main():
    try:
        module_name = sys.argv[1]
        unittest.main(globals()[module_name], argv=[])
    except IndexError:
        unittest.main()


if __name__ == '__main__':
    main()