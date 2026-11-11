"""Write a fictional, filled SIRT response for the sample gate package.

Starts from the pinned FNA template and answers every catalog row: Y, except three N answers with reasons.
The answers are invented for the demo; they describe no real system.

    python tools/make_sample_sirt.py [output.xlsx]
"""

from __future__ import annotations

import sys
from importlib import resources
from pathlib import Path

from capd.catalog import Catalog
from capd.validators import sirt, templates

NO = {"AP-2": "Planned for release 4; workers set the date by hand until then.",
      "C-1": "Claims are calculated in the separate claims system.",
      "ED-2": "Single-element updates only in this release."}


def main(out: str = "examples/sample-package/fna-uat/sirt-response.xlsx") -> None:
    with resources.as_file(templates.pinned_path("sirt")) as p:
        wb = templates.open_workbook(p)
    for r in Catalog.load().rules.values():
        if r["set"] != "sirt":
            continue
        ws = wb[r["source"]["sheet"]]
        row = r["source"]["row"]
        header = sirt._header_for(ws, row)
        answers, reason, free = sirt._columns(header)
        if free is not None:  # FNS report rows
            for c in answers:
                ws.cell(row, c + 1).value = "Monthly" if header[c] == "Frequency" else "Eligibility system"
            ws.cell(row, free + 1).value = "Produced from the eligibility system."
            continue
        if sirt._clean(ws.cell(row, answers[0] + 1).value):
            continue  # the template already answers this row (for example a heading row marked NA)
        if r["sourceId"] in NO:
            ws.cell(row, answers[0] + 1).value = "N"
            ws.cell(row, reason + 1).value = NO.pop(r["sourceId"])
        else:
            ws.cell(row, answers[0] + 1).value = "Y"
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main(*sys.argv[1:])
