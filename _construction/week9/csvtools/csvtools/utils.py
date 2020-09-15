import sys 


class InputError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def report_error(error, quiet=False):
    """
    Formats the error message and prints it to stderr

    :param error: string containing error text
    :param quiet: if True, don't report errors
    """
    if not quiet:
        sys.stderr.write('ERROR: ' + error + '\n')


def report_wrong_number_of_columns(row, careful, quiet):
    """
    Reports invalid columns in a row error

    :param careful: whether to ignore this kind of error
    :param quiet: whether to print the error message to stderr
    """
    error = 'Wrong number of columns in row'
    if careful:
        raise InputError(row, error)
    report_error(error + '"' + ','.join(row) + '"', quiet)


