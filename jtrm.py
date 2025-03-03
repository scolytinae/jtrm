#!/usr/bin/env python

import argparse
import json
from jinja2 import Environment, FileSystemLoader

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

    def get_data(self):
        # with open(self.data_file, "r") as f:
        #     return json.loads(f)
        return json.loads('{ "username" : "Igrtkv"} ')

    def render(self):
        env = Environment(loader=FileSystemLoader("./templates"))
        template = env.get_template("test-template.md")
        data = self.get_data()
        print(template.render(data))

if __name__ == "__main__":
    jtrm = JinjaTemplateReportMachine()
    # jtrm.parse_arguments()
    jtrm.render()


