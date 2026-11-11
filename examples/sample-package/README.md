# Sample gate package

A fictional FNA UAT package: a few placeholder documents, a filled SIRT response workbook
(made by [`tools/make_sample_sirt.py`](../../tools/make_sample_sirt.py)), and a `package.yaml` index that
says which file answers which Go Live criterion.

```sh
capd package check FNA-UAT examples/sample-package/fna-uat -o out/package
capd package verify out/package/submission-record.json examples/sample-package/fna-uat
```

The check reports the package as not complete on purpose: most Go Live criteria have no file yet. See
[gate packages](../../docs/gate-packages.md).
