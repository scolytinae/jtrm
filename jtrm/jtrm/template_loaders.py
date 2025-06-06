import os
from urllib.parse import urlparse
import typing as t
from jinja2 import FunctionLoader, FileSystemLoader, BaseLoader
import settings


class FileSystemTemlatesLoader(FileSystemLoader):

    def __init__(self, bucket: str) -> None:        
        self._searchpath = os.path.join(settings.JTRM_TEMPLATES_DIR, bucket)        
        super().__init__(searchpath=self._searchpath)


class S3TemplatesLoader(BaseLoader):

    def __init__(self, bucket: str) -> None:
        self._bucket = bucket
        super().__init__()

    def get_source(
        self, environment: "Environment", template: str
    ) -> t.Tuple[str, t.Optional[str], t.Optional[t.Callable[[], bool]]]:
        pass

    def list_templates(self) -> t.List[str]:
        found = set()
        return sorted(found)


class TemplatesLoaderFactory:
    
    def get_loader(self, uri: str) -> BaseLoader:
        settings = urlparse(uri)
        if settings.scheme == "file":
            return FileSystemTemlatesLoader(bucket=settings.netloc)

        if settings.scheme == "s3":
            return S3TemplatesLoader(bucket=settings.netloc)

        raise RuntimeError(f"No template loader for settings {uri}")
        
