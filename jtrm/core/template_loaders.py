import os
from urllib import parse
import typing as t
from jinja2 import FunctionLoader, FileSystemLoader, BaseLoader


class FileSystemTemlatesLoader(FileSystemLoader):

    def __init__(self, bucket: str) -> None:        
        self._searchpath = os.environ.get("JTRM_TEMPLATES_DIR", "./templates")
        self._loader = FileSystemLoader(searchpath=os.path.join(self._searchpath, bucket))
        super().__init__(searchpath=self._searchpath)


class TemplatesLoaderFactory:
    
    def get_loader(self, uri: str) -> BaseLoader:
        settings = parse(uri)
        if settings.scheme == "file":
            return FileSystemTemlatesLoader(bucket=settings.netloc)

        raise RuntimeError(f"No template loader for settings {uri}")
        
