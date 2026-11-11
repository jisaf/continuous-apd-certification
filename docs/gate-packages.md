# Gate packages

Before each review, the state sends CMS or FNA a package of files: letters, plans, the agency workbooks.
`capd package` checks that folder and writes a **submission record**: what the package held, with a SHA-256
hash for each file, so anyone can later prove which files went to the agency.

It tracks files only. It does not judge a letter or a plan, and it does not replace the agency's own
checklist. Tests and metrics stay with the pipeline and the [report layer](report-layer.md).

## Try it

```sh
capd package check FNA-UAT examples/sample-package/fna-uat -o out/package
capd package verify out/package/submission-record.json examples/sample-package/fna-uat
```

The sample is fictional and reports "Not complete" on purpose. Open `out/package/checklist.md`.

## What it checks

| Check | Where the list comes from |
| --- | --- |
| Every applicable rule for the gate that rests on a file (a document, attestation, demonstration record, or report) has a file | The catalog: rules whose evidence kinds for the gate include a file kind. For the FNA gates these are the Go Live criteria; for the ORR and CR, the CEFs and outcomes that need documents. SIRT rows are answered in the SIRT workbook instead. |
| The agency workbooks the gate needs are present and pass their checks | Defaults: ORR needs the SMC Intake Form; CR needs the Intake Form and the ORW; FNA UAT needs the SIRT response. Change them with `workbooks:` in `package.yaml`. |
| Every file's SHA-256, and a hash over the whole record | `submission-record.json` ([schema](../src/capd/data/schemas/submission-record.schema.json)) |

Rules the state marked N/A in `capd.yaml` show as N/A. `capd package check` exits with 1 until the package
is complete, so a pipeline or a person can use it as a gate.

## The package index

Put a `package.yaml` in the folder. It says which file answers which rule:

```yaml
gate: FNA-UAT
items:
  fna:golive:GL01: [letters/transmittal-letter.pdf]
  fna:golive:GL08: [sirt-response.xlsx]
workbooks: [sirt]          # optional; overrides the gate's default workbooks
```

Workbooks are found by their template, not their name: any `.xlsx` file that matches a pinned CMS or FNA
template is checked.

## The SIRT response check

`capd validate sirt FILE` checks a state's answers in FNA's SIRT workbook (the Excel version pinned in this
package):

- the workbook is the known template version, and no rows were added, removed, or moved;
- every row has an answer (Y, N, or NA; FNS report rows need a frequency, data source, or comment);
- every N answer has a reason;
- with `--bundle out/bundle.json`, a Y answer on a rule whose tagged tests fail is a warning. This catches a
  SIRT that says "yes" while the pipeline says the feature is broken.

## Proving what was sent

Keep `submission-record.json` with the package. Later, `capd package verify RECORD FOLDER` re-hashes the
files and reports any file that changed or is missing, and any change to the record itself.
