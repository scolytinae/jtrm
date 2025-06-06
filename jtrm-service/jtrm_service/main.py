import typing as t
import logging
import settings
from jinja2 import Environment
from dependencies import TemplatesLoaderFactory, JinjaTemplateReportMachine

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Json

class GenerateReportModel(BaseModel):
    template: str
    data: t.Dict[t.AnyStr, t.Any]


app = FastAPI()
logger = logging.getLogger('jtrm.error')


@app.post("/immediate_report/")
def generate_report(item: GenerateReportModel, response_class=FileResponse):
    logger.debug("Immediate report called")
    factory = TemplatesLoaderFactory()
    loader = factory.get_loader(settings.TEMPLATE_LOADER_CONNECTION)
    env = Environment(loader=loader)
    template = env.get_template(item.template)

    jtrm = JinjaTemplateReportMachine()
    r = jtrm.render(item.data, template)

    # jtrm = LocalReportGenerator(
    #     template_file=f"./templates/{item.template}",
    #     data_file=args.data,
    #     dest_file=args.output,
    #     dest_format=args.output_format,
    # )
    # report_file_name = reporter.make_report()
    return r

if __name__ == '__main__':
    uvicorn.run(app, log_level="trace") 