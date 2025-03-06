#!/usr/bin/env python

import argparse
import json
import os
import codecs
from jinja2 import Environment, FileSystemLoader, Template

DEFAULT_TEMPLATES_PATH = "./templates"

class JinjaTemplateReportMachine:
    DEFAULT_TEMPLATE = ""
    DEFAULT_DATA = ""
    DEFAULT_OUTPUT = ""

    def __init__(self, 
            template_file=DEFAULT_TEMPLATE, 
            data_file=DEFAULT_DATA, 
            output_file=DEFAULT_OUTPUT
    ):
        self.template_file = template_file
        self.data_file = data_file
        self.output_file = output_file

    def parse_arguments(self):
        parser = argparse.ArgumentParser(prog="jtpm")
        parser.add_argument("-t", "--template", required=True)
        parser.add_argument("-d", "--data", required=True)
        parser.add_argument("-o", "--output")
        return parser.parse_args()


    def render(self, data: dict, template: Template):
        return template.render(data)


class LocalReportGenerator:
    def __init__(self,
            template_file=DEFAULT_TEMPLATE, 
            data_file=DEFAULT_DATA, 
            output_file=DEFAULT_OUTPUT
    ):
        self._jtrm = JinjaTemplateReportMachine()
        self._template_file = template_file
        self._data_file = data_file
        self._output_file = output_file

    def _read_data(self):
        if not os.path.exists(self._data_file):
            return {}

        with codecs.open(self._data_file, "r+", encoding="utf-8") as f:
            return json.load(f)

    def _read_template(self):
        env = Environment(loader=FileSystemLoader("./"))
        return env.get_template(self._template_file)

    def generate_report(self):
        template = self._read_template()
        data = self._read_data()

        output = self._jtrm.render(data, template)
        with codecs.open(self._output_file, "w", encoding="utf-8") as of:
            of.writelines(output)

    def parse_arguments(self):
        parser = argparse.ArgumentParser(prog="jtpm")
        parser.add_argument("-t", "--template", required=True)
        parser.add_argument("-d", "--data", required=True)
        parser.add_argument("-o", "--output")
        return parser.parse_args()


if __name__ == "__main__":
    jtrm = JinjaTemplateReportMachine()
    # jtrm.parse_arguments()
    jtrm.render2()


