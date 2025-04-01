from typing import Union, Object

# from core import JinjaTemplateReportMachine
from template_loaders import TemplatesLoaderFactory

from fastapi import FastAPI, FileResponse
from pydantic import BaseModel, Json

class GenerateReportModel(BaseModel):
    template: str
    data: Json[Object]

app = FastAPI()

@app.post("/immediate_report/{item}")
def generate_report(item: GenerateReportModel, response_class=FileResponse):
    loader = TemplatesLoaderFactory.get_loader("file://test_bucket")
    env = Environment(loader=loader)
    template = env.get_template(item.template)

    jtrm = JinjaTemplateReportMachine()
    r = jtrm.render({}, template)

    # jtrm = LocalReportGenerator(
    #     template_file=f"./templates/{item.template}",
    #     data_file=args.data,
    #     dest_file=args.output,
    #     dest_format=args.output_format,
    # )
    # report_file_name = reporter.make_report()
    return r
