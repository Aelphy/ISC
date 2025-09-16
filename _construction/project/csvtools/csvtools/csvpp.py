from argparse import ArgumentParser
import sys

from . utils import report_error, report_wrong_number_of_columns, InputError

DESCRIPTION = 'csvpp - prints cvs file in human-readable format'
EXAMPLES = 'example: cat file.txt | csvpp -f | less -SR'


def print_row(row, column_widths, output_stream, careful, quiet):
    """
    Prints a row in human-readable format taking column widths into account

    :param row: row represented as a list of columns
    :param column_widths: a list of column list widths to be used for pretty printing
    :param output_stream: a stream to pretty print the row
    :param careful: raise an exception on incorrect rows
    :param quiet: don't report non-critical errors
    """
    if len(column_widths) != len(row):
        report_wrong_number_of_columns(row, careful, quiet)

    output_line = '|'
    for i, column in enumerate(row):
        width = column_widths[i] if i < len(column_widths) else 0
        output_line += ' ' + column + ' ' * (width - len(column)) + ' |'
    output_line += '\n'
    output_stream.write(output_line)


def pretty_print(args):
    input_stream = sys.stdin
    output_stream = sys.stdout
    try:
        if args.file:
            input_stream = open(args.file, 'r')
        if args.output_file:
            output_stream = open(args.output_file, 'w')

        columns = input_stream.readline().strip().split(args.separator)
        first_rows = [columns]
        for line in input_stream:
            row = line.strip().split(args.separator)
            first_rows.append(row)
            # Read no more than lines_number first lines
            if len(first_rows) > args.lines_number:
                break

        column_widths = [max([len(column) for column in [row[i] if i < len(row) else '' for row in first_rows]])
                         for i in range(len(columns))]

        for row in first_rows:
            print_row(row, column_widths, output_stream, args.careful, args.quiet)
        for row in input_stream:
            print_row(row.strip().split(args.separator), column_widths, output_stream,
                      args.careful, args.quiet)

    except FileNotFoundError:
        report_error("File {} doesn't exist".format(args.file))
    except InputError as e:
        report_error(e.message + '. Row: ' + str(e.expression))
    except KeyboardInterrupt:
        pass
    except BrokenPipeError:
        # The following line prevents python to inform you about the broken pipe
        sys.stderr.close()
    except Exception as e:
        report_error('Caught unknown exception. Please report to developers: {}'.format(e))
    finally:
        if input_stream and input_stream != sys.stdin:
            input_stream.close()
        if output_stream:
            output_stream.close()


def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-s', '--separator', type=str, help='Separator to be used', default=',')
    parser.add_argument('-n', '--lines_number', type=int, help='Number of lines used to set column width',
                        default=100)
    parser.add_argument('-f', '--format_floats', help='Format floating-point numbers nicely', action='store_true')
    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')
    parser.add_argument('-q', '--quiet', help="Don't print information regarding errors", action='store_true')
    parser.add_argument('--careful', help='Stop if input contains an incorrect row', action='store_true')

    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    pretty_print(parse_args())
