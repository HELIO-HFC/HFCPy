#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Python module template."""

# ________________ IMPORT _________________________
# (Include here the modules to import, e.g. import sys)

# ________________ HEADER _________________________

# Mandatory
__version__ = ""
__author__ = ""
__date__ = ""

# Optional
__license__ = ""
__credit__ = [""]
__maintainer__ = ""
__email__ = ""
__project__ = ""
__institute__ = ""
__changes__ = ""


# ________________ Global Variables _____________
# (define here the global variables)

# ________________ Class Definition __________
# (If required, define here classes)

# ________________ Global Functions __________
# (If required, define here global functions)
def main():
    """Main program."""


def setup_logging(filename=None, error_filename=None,
                  quiet=False, verbose=False, debug=False):
    """Method to setup a logging instance."""
    import logging

    if debug:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)-8s: %(message)s')
    elif verbose:
        logging.basicConfig(level=logging.INFO,
                            format='%(levelname)-8s: %(message)s')
    else:
        logging.basicConfig(level=logging.CRITICAL,
                            format='%(levelname)-8s: %(message)s')

    if quiet:
        logging.root.handlers[0].setLevel(logging.CRITICAL + 10)
    elif verbose:
        logging.root.handlers[0].setLevel(logging.INFO)
    else:
        logging.root.handlers[0].setLevel(logging.CRITICAL)

    if filename:
        import logging.handlers
        fhandler = logging.FileHandler(filename, delay=True)
        fhandler.setFormatter(logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(funcName)-12s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'))
        if debug:
            fhandler.setLevel(logging.DEBUG)
        else:
            fhandler.setLevel(logging.INFO)

        logging.root.addHandler(fhandler)

    if error_filename:
        import logging.handlers
        efhandler = logging.FileHandler(error_filename, delay=True)
        efhandler.setFormatter(logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(funcName)-12s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'))

        efhandler.setLevel(logging.ERROR)
        logging.root.addHandler(efhandler)

    # _________________ Main ____________________________


if __name__ == "__main__":
    # print ""
    main()
