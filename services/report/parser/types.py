from io import BytesIO
from typing import BinaryIO, List, Optional

from services.path_fixer.fixpaths import clean_toc


class ParsedUploadedReportFile(object):
    def __init__(
        self,
        filename: Optional[str],
        file_contents: BinaryIO,
        labels: Optional[List[str]] = None,
    ):
        self.filename = filename
        self.contents = file_contents.getvalue()
        self.size = len(self.contents)
        self.labels = labels

    @property
    def file_contents(self):
        return BytesIO(self.contents)

    def get_first_line(self):
        return self.file_contents.readline()


class ParsedRawReport(object):
    def __init__(
        self,
        toc: Optional[BinaryIO],
        env: Optional[BinaryIO],
        uploaded_files: List[ParsedUploadedReportFile],
        path_fixes: Optional[BinaryIO],
    ):
        self.toc = toc
        self.env = env
        self.uploaded_files = uploaded_files
        self.path_fixes = path_fixes

    def has_toc(self) -> bool:
        return self.toc is not None

    def has_env(self) -> bool:
        return self.env is not None

    def has_path_fixes(self) -> bool:
        return self.path_fixes is not None

    @property
    def size(self):
        return sum(f.size for f in self.uploaded_files)


class VersionOneRawReport(ParsedRawReport):
    def get_toc(self) -> List[str]:
        return self.toc

    def get_env(self):
        return self.env

    def get_uploaded_files(self):
        return self.uploaded_files

    def get_path_fixes(self):
        return self.path_fixes


class LegacyParcedRawReport(ParsedRawReport):
    def get_toc(self) -> List[str]:
        toc = self.toc.read().decode(errors="replace").strip()
        toc = clean_toc(toc)
        return toc

    def get_env(self):
        return self.env.read().decode(errors="replace")

    def get_uploaded_files(self):
        return self.uploaded_files

    def get_path_fixes(self):
        return self.path_fixes.read().decode(errors="replace")
