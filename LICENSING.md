# Licensing

This project is fully open source. There is no commercial license and no contributor license agreement. The goal is that any state, vendor, or other organization can use, change, and build on every part of it, including connectors, without asking anyone.

| What | License | File |
| --- | --- | --- |
| Source code (core library, CLI, connectors, report generators, templates that are code) | Apache License 2.0 | [`LICENSE`](LICENSE) |
| Rules catalog data, mappings, example tests, example queries, test data, and documentation | Creative Commons CC0 1.0 Universal (public domain dedication) | [`LICENSE-DATA`](LICENSE-DATA) |

Where a file does not say otherwise, files under `docs/`, and any future `catalog/`, `examples/`, and `data/` directories, are CC0. Everything else is Apache-2.0.

## What this means in practice

- Anyone may use, change, and share the code, including in paid work and inside state contracts.
- Vendors may write and deliver connectors under any terms their contract requires.
- Apache-2.0 includes an express patent license from contributors.
- Reports, evidence bundles, and agency files the tools produce belong to whoever produces them.

## Contributions

Contributions are accepted under the same licenses: code under Apache-2.0 and data or documentation under CC0. Each commit must carry a [Developer Certificate of Origin](https://developercertificate.org/) sign-off (`git commit -s`), which certifies that the contributor has the right to submit it. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Third-party material

We respect the licenses of everything we build on:

- **U.S. government works** (CMS and FNA/FNS guidance, the SNAP SIRT, 18F prototypes) are public domain in the United States and may be included in the CC0 data. The 18F prototypes also carry a CC0 waiver.
- **Permissive licenses (MIT, BSD)** — for example the MES Certification Navigator (MIT) and MAGI in the Cloud (BSD-3) — may be included only with their original notices kept, in a clearly marked third-party folder. Such material is not relabeled CC0.
- **Copyleft licenses (AGPL, MPL)** — for example PolicyEngine US (AGPL-3.0) — are never copied into this project. They may be run as separate tools, for example as an independent engine that cross-checks test cases.
- **Noncommercial licenses** (for example PolyForm Noncommercial) are not used.

## Federal funding and ownership

Federal rules give states ownership of software built with enhanced federal match, and give the federal government a royalty-free license to it (CMS Conditions for Enhanced Funding CEF05 and CEF06; 42 CFR 433.112(b)(5)–(6); 7 CFR 277.18(l); FNS Handbook 901, Appendix A16). A permissive license is compatible with this: extensions a state pays for belong to that state, and states are encouraged to contribute them back.

*This file explains the project's intent and is not legal advice.*
