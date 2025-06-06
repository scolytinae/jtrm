#!/usr/bin/env python

import argparse
import json
import os
import sys
import uuid
import codecs
import pypandoc
from jinja2 import Environment, FileSystemLoader, Template

TEMP_REPORT_DIR = os.environ.get("JTRM_TEMP_DIR", "/tmp")

HELP_DESCRIPTION = """
Creates a report with required format from jinja template

Uses pandoc installed in system. Without it will not work.
"""


class JinjaTemplateReportMachine:

    def render(self, data: dict, template: Template):
        return template.render(data)

    def convert(self, source, source_format, dest_format):
        return pypandoc.convert_text(
            source=source, to=dest_format, format=source_format
        )

    def convert_file(self, source, source_format, dest, dest_format):
        return pypandoc.convert_file(
            source_file=source, to=dest_format, format=source_format, outputfile=dest
        )


class LocalReportGenerator(JinjaTemplateReportMachine):
    def __init__(
        self,
        template_file,
        data_file,
        dest_file=None,
        dest_format=None,
        template_format=None,
    ):
        self._template_file = template_file
        self._data_file = data_file
        self._dest_file = dest_file
        self._dest_format = (
            self._get_format(dest_file) if dest_format is None else dest_format
        )
        self._template_format = (
            self._get_template_format(template_file)
            if template_format is None
            else template_format
        )

    def _read_template(self):
        env = Environment(loader=FileSystemLoader("./"))
        return env.get_template(self._template_file)

    def _read_data(self):
        if not os.path.exists(self._data_file):
            return {}

        with codecs.open(self._data_file, "r+", encoding="utf-8") as f:
            return json.load(f)

    def _write_file(self, data, file_name):
        with codecs.open(file_name, "w", encoding="utf-8") as f:
            f.write(data)

    def _write_report(self, report):
        out = (
            sys.stdout
            if self._dest_file is None
            else codecs.open(self._dest_file, "w", encoding="utf-8")
        )
        try:
            out.write(report)
        finally:
            if self._dest_file is not None:
                out.close()

    def _get_format(self, file_name):
        return os.path.splitext(file_name)[1][1:]

    def _get_template_format(self, file_name):
        fmt = self._get_format(file_name)
        if fmt == "j2":
            fmt2 = self._get_format(file_name[: -len(fmt) - 1])
            return fmt2 if fmt2 else fmt

        return fmt

    def make_report(self):
        template = self._read_template()
        data = self._read_data()
        rendered = self.render(data, template)
        if self._template_format == self._dest_format:
            self._write_report(rendered)
        else:
            fname = os.path.join(
                TEMP_REPORT_DIR, f"{str(uuid.uuid4())}.{self._template_format}"
            )
            self._write_file(rendered, fname)
            try:
                self.convert_file(
                    fname, self._template_format, self._dest_file, self._dest_format
                )
            finally:
                os.remove(fname)


def parse_arguments():

    parser = argparse.ArgumentParser(
        prog="jtpm",
        description=HELP_DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
    )

    main_group = parser.add_argument_group("Main arguments")
    main_group.add_argument(
        "-t", "--template", required=True, type=str, help="Template file name"
    )
    main_group.add_argument("-o", "--output", type=str, help="Output report file name")
    main_group.add_argument(
        "-d", "--data", type=str, default="", help="File with data in JSON format"
    )

    optional_group = parser.add_argument_group("Optional arguments")
    optional_group.add_argument(
        "--template-format", type=str, default="", help="Template file format"
    )
    optional_group.add_argument(
        "--output-format", type=str, help="Output report format"
    )
    optional_group.add_argument(
        "-h", "--help", action="help", help="show this help message and exit"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    reporter = LocalReportGenerator(
        template_file=args.template,
        data_file=args.data,
        dest_file=args.output,
        dest_format=args.output_format,
    )
    reporter.make_report()
