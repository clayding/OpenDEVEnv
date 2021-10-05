#!/usr/bin/env python3

import options
import base

if __name__ == "__main__":
    try:
        config = base.BaseConfig()
        ret = config.setup()
    except Exception as esc:
        ret = 1
        import traceback
        traceback.print_exc()
