import re

from base_linter import BaseLinter, INPUT_METHOD_TEMP_FILE

CONFIG = {
    'language': 'Puppet_duallint',
    'executable': 'puppet-duallinter.sh',
    'lint_args': ['{filename}'],
    'test_existence_args': '-v',
    'input_method': INPUT_METHOD_TEMP_FILE
}


class Linter(BaseLinter):
    def parse_errors(self, view, errors, lines, errorUnderlines, violationUnderlines, warningUnderlines, errorMessages, violationMessages, warningMessages):
        for line in errors.splitlines():
            #match puppet-lint output
            match = re.match(r'(ERROR|WARNING): (?P<error>.+?) on line (?P<line>\d+)?', line)
            if match:
                error, line = match.group('error'), match.group('line')
                lineno = int(line)
                self.add_message(lineno, lines, error, errorMessages)

            #match puppet output
            match = re.match(r'[Ee]rr(or)?: (?P<error>.+?(Syntax error at \'(?P<near>.+?)\'; expected \'.+\')) at /.+?:(?P<line>\d+)?', line)
            if not match:
                match = re.match(r'[Ee]rr(or)?: (?P<error>.+?(Could not match (?P<near>.+?))?) at /.+?:(?P<line>\d+)?', line)

            if match:
                error, line = match.group('error'), match.group('line')
                lineno = int(line)
                near = match.group('near')

                if near:
                    error = '{0}, near "{1}"'.format(error, near)
                    self.underline_regex(view, lineno, '(?P<underline>{0})'.format(re.escape(near)), lines, errorUnderlines)

                self.add_message(lineno, lines, error, errorMessages)
