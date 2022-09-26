import base64
import zlib
from io import BytesIO

from services.report.parser.version_one import (
    ParsedUploadedReportFile,
    VersionOneReportParser,
)

input_data = b"""{
    "path_fixes": {"format": "legacy", "value": ""},
    "network_files": [
        "path/to/file1.c",
        "path/from/another.cpp",
        "path/from/aaaaaa.cpp"
    ],
    "coverage_files": [
        {
            "filename": "coverage.xml",
            "format": "base64+compressed",
            "data": "eJwlzMEJAzEMRNH7VjEFhFSSJhRLLAOW7bWk/mPI+fP+Z25zcEU5dPa5EUyIW76uNkdYS8vaEOViNI4b1nlimB4AY4VPRZqvgzkalVojr0p0+Z49LP9rg8s9BNL5lLx/AW8tRQ==",
            "labels": null
        },
        {
            "filename": "another.coverage.json",
            "format": "base64+compressed",
            "data": "eJztV11P2zAUfedXGEsTIC1xPigtKC0PDE17mDYJNImnyk3c1lvsRLGD6L/nOl9NoWkjlr3tJW1ufM859/ravg5uX0SMnlmmeCKn2LUdjG5nJ8Hplx93j08/71GYwEe6YicIPTw9PN5/R2drrdMbQsJkwTKdZ9RWSZ6FbJlkK2ZLpglAktrPcnw70tEZYNYmtMioDNdWRjWbYsd2xu6lj1HMJWtso5FzhZHmgilNRQrKrkaT8bXnTq7xVq5vj20Xz0AbQsUjOLUs9JVJZnAitNg0+u10c4Mq5ZJFC6rDNYsjltlhIkBtxBrJyLJKyCCl4R8wqPK1beqIAbDSmL1wvQHj3pAkFfCGt4gFahhTpdo8u1/6sS15zEp4JlK9OUBffCcqC/EsIAXDUMxlKRygXiYm6cR44PekBbFgep1EeyS9GVEhnlOZyI1IcjV3LzBCa64V1Av8U3wlKVSoGXTxC6NuxALVaFaz4gfJXEB1T3EuI7YEQ9QGJpC1cnC3RFJq7AiRHIwxOAZeSCzlTHCj1cGkn0+xymsv97hXWQNTrLOcmbmXEdew/qx6wQD1J3TuEA/S3yRJcKW4XFmlMwOjqZctrzcE78gQu8eI/Va4/hC0rmN4vV3emuHyOEM9dFS7g8CewXrk8qJj4VQMjeuBCtod2KogpDcpUP3ORYpRe34PBdWB5g6K5nWhmcn4AJ7/cTzYM3vkuNwj+pbC1f9S2J/E4VI94Db2uXls1/14oA1tz5Yy6YLuPIe6j3XTIT2ENKboXb+zM+5Dx39xrPduexqu4yc+dIGaCSb1sUpuBqKyFak1lRRTvDB9KvsmNcuS9C4RwkyhEVwkvJ6gJY0VOHH5nIS0mqJcahMtnP0Nx19qqYm9t0v+Pa/7L3j9HgH3JW4N6upqupuegZtQaPtgjg/UoWn3ofrJfM4l1/N5RxtcGXf6f1JdAKobAtleEYLmAjE7eQU4GYHA",
            "labels": ["simple", "a.py::fileclass::test_simple"]
        }
    ],
    "metadata": {   
    }
}"""


def test_version_one_parser():
    subject = VersionOneReportParser()
    res = subject.parse_raw_report_from_bytes(input_data)
    assert res.env is None
    assert res.path_fixes == ""
    assert res.toc == [
        "path/to/file1.c",
        "path/from/another.cpp",
        "path/from/aaaaaa.cpp",
    ]
    assert len(res.uploaded_files) == 2
    first_file, second_file = res.uploaded_files
    assert isinstance(first_file, ParsedUploadedReportFile)
    assert first_file.filename == "coverage.xml"
    assert (
        first_file.contents
        == b"Lorem ipsum dolor sit amet,\nconsectetur adipiscing elit,\nsed do eiusmod tempor incididunt\nut labore et dolore magna aliqua."
    )
    assert first_file.size == 123
    assert first_file.labels is None
    assert second_file.filename == "another.coverage.json"
    assert (
        second_file.contents
        == b'<?xml version="1.0" ?>\n<!DOCTYPE coverage\n  SYSTEM \'http://cobertura.sourceforge.net/xml/coverage-03.dtd\'>\n<coverage branch-rate="0.07143" line-rate="0.5506" timestamp="1658792189" version="3.7.1">\n    \n    <!-- Generated by coverage.py: http://nedbatchelder.com/code/coverage -->\n    <packages>\n        <package branch-rate="0.07143" complexity="0" line-rate="0.5506" name="">\n            <classes>\n                <class branch-rate="0.07143" complexity="0" filename="empty" line-rate="0.5506" name="empty/src"></class>\n                <class branch-rate="0.07143" complexity="0" filename="source" line-rate="0.5506" name="folder/file">\n                    <methods>\n                        <method name="(anonymous_1)"  hits="1"  signature="()V" >\n                            <lines><line number="undefined"  hits="1" /></lines>\n                        </method>\n                    </methods>\n                    <lines>\n                        <line hits="8" number="0"/>\n                        <line hits="1.0" number="1"/>\n                        <line branch="true" condition-coverage="0% (0/2)" hits="1" missing-branches="exit" number="2"/>\n                        <line branch="true" condition-coverage="50% (1/2)" hits="1" missing-branches="30" number="3"/>\n                        <line branch="true" condition-coverage="100% (2/2)" hits="1" number="4"/>\n                        <line number="5" hits="0" branch="true" condition-coverage="50% (2/4)">\n                          <conditions>\n                            <condition number="0" type="jump" coverage="0%"/>\n                            <condition number="1" type="jump" coverage="0%"/>\n                            <condition number="2" type="jump" coverage="100%"/>\n                            <condition number="3" type="jump" coverage="100%"/>\n                          </conditions>\n                        </line>\n                        <line number="6" hits="0" branch="true" condition-coverage="50% (2/4)">\n                          <conditions>\n                            <condition number="0" type="jump" coverage="0%"/>\n                            <condition number="1" type="jump" coverage="0%"/>\n                          </conditions>\n                        </line>\n                        <line branch="true" condition-coverage="0% (0/2)" hits="1" missing-branches="exit,exit,exit" number="7"/>\n                        <line branch="true" condition-coverage="50%" hits="1" number="8"/>\n                    </lines>\n                </class>\n                <!-- Scala coverage -->\n                <class branch-rate="0.07143" complexity="0" filename="file" line-rate="0.5506" name="">\n                    <methods>\n                        <statements>\n                            <statement source="file" method="beforeInteropCommit" line="1" branch="false" invocation-count="0"></statement>\n                            <statement source="file" method="" line="2" branch="true" invocation-count="1"></statement>\n                            <statement source="file" method="" line="3" branch="false" invocation-count="1"></statement>\n                        </statements>\n                    </methods>\n                </class>\n                <class branch-rate="0.07143" complexity="0" filename="ignore" line-rate="0.5506" name="codecov/__init__"></class>\n            </classes>\n        </package>\n    </packages>\n</coverage>\n'
    )
    assert second_file.size == 3415
    assert second_file.labels == ["simple", "a.py::fileclass::test_simple"]


def test_version_one_parser_parse_coverage_file_contents_bad_format():
    subject = VersionOneReportParser()
    coverage_file = {"format": "unknown", "data": b"simple", "filename": "filename.py"}
    assert subject._parse_coverage_file_contents(coverage_file) == b"simple"


def test_version_one_parser_parse_coverage_file_contents_base64_zip_format():
    original_input = b"some_cool_string right \n here"
    formatted_input = base64.b64encode(zlib.compress(original_input))
    # An assert for the sake of showing the result
    assert formatted_input == b"eJwrzs9NjU/Oz8+JLy4pysxLVyjKTM8oUeBSyEgtSgUArOcK4w=="
    subject = VersionOneReportParser()
    coverage_file = {
        "format": "base64+compressed",
        "data": formatted_input,
        "filename": "filename.py",
    }
    res = subject._parse_coverage_file_contents(coverage_file)
    assert isinstance(res, BytesIO)
    assert res.getvalue() == b"some_cool_string right \n here"
