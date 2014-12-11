import logging
import sys
from . import auto

if __name__ == '__main__':
    # Default logging levels. These can be overridden when the config file is loaded.
    logging.getLogger().setLevel(logging.WARNING)
    logging.getLogger('neocommon').setLevel(logging.INFO)
    logging.getLogger('fetch').setLevel(logging.INFO)

    if len(sys.argv) != 2:
        sys.stderr.writelines([
            'Usage: fetch-service <config.yaml>\n'
        ])
        sys.exit(1)

    run_config = auto.init_run_config(sys.argv[1])
    auto.run_loop(run_config)
