#!/usr/bin/env python

import argparse
import json
import os
import sys
import codecs
from jinja2 import Environment, FileSystemLoader, Template


class JinjaTemplateReportMachine:

    def render(self, data: dict, template: Template):
        return template.render(data)


class LocalReportGenerator:
    def __init__(self, template_file, data_file):
        self._jtrm = JinjaTemplateReportMachine()
        self._template_file = template_file
        self._data_file = data_file

    def _read_data(self):
        if not os.path.exists(self._data_file):
            return {}

        with codecs.open(self._data_file, "r+", encoding="utf-8") as f:
            return json.load(f)

    def _read_template(self):
        env = Environment(loader=FileSystemLoader("./"))
        return env.get_template(self._template_file)

    def render(self):
        template = self._read_template()
        data = self._read_data()

        return self._jtrm.render(data, template)


def parse_arguments():
    parser = argparse.ArgumentParser(prog="jtpm")
    parser.add_argument("-t", "--template", required=True, type=str)
    parser.add_argument("-d", "--data", type=str, default="")
    parser.add_argument("-o", "--output", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    reporter = LocalReportGenerator(template_file=args.template, data_file=args.data)

    report = reporter.render()
    if args.output is None:
        out = sys.stdout
    else:
        out = codecs.open(args.output, "w", encoding="utf-8")

    try:
        out.write(report)
    finally:
        if args.output is not None:
            out.close()
