import typing as t
from . import settings
from jtrm_core.template_loaders import TemplatesLoaderFactory

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Json

class GenerateReportModel(BaseModel):
    template: str
    data: Json[t.List]


app = FastAPI()


@app.post("/immediate_report/")
def generate_report(item: GenerateReportModel, response_class=FileResponse):
    loader = TemplatesLoaderFactory.get_loader(settings.TEMPLATE_LOADER_CONNECTION)
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
