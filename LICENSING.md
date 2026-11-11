# Licensing

This project uses two licenses, chosen so that states and their vendors can use and adapt it freely, while changes to the code itself stay open.

| What | License | File |
| --- | --- | --- |
| Source code (core library, CLI, connectors, report generators) | GNU Affero General Public License v3.0 (AGPL-3.0) | [`LICENSE`](LICENSE) |
| Rules catalog data, mappings, example tests, example queries, test data, and documentation | Creative Commons CC0 1.0 Universal (public domain dedication) | [`LICENSE-DATA`](LICENSE-DATA) |

Where a file does not say otherwise, files under `docs/`, and any future `catalog/`, `examples/`, and `data/` directories, are CC0. Everything else is AGPL-3.0.

## What the AGPL means in practice

- Anyone — states, vendors, and other organizations — may use, study, change, and share the code.
- Running the tools inside your own CI/CD pipeline, or generating reports and files with them, creates **no** obligation to publish anything.
- If you **distribute** a modified version, or let others use a modified version **over a network**, you must make your modified source code available under the AGPL.
- Reports, evidence bundles, and agency files that the tools produce are your own output, not covered by the AGPL.

## Commercial license

The repository owner offers a separate commercial license for organizations that want to modify and offer the code without the AGPL's source-sharing terms. Contact the owner through a GitHub issue marked "licensing" to start that conversation.

Dual licensing is only possible because every contributor signs the [contributor license agreement](CLA.md).

## Federal funding and ownership

Federal rules give states ownership of software built with enhanced federal match, and give the federal government a royalty-free license to it (CMS Condition for Enhanced Funding CEF05 and CEF06; 42 CFR 433.112(b)(5)–(6); 7 CFR 277.18(l); FNS Handbook 901, Appendix A16).

- The core in this repository is developed independently of any state contract.
- Extensions that a state pays for under its own project belong to that state, under whatever terms its contract and the federal rules require. States are encouraged to contribute them back.

## Third-party sources

The rules catalog is derived from U.S. government publications, which are in the public domain in the United States. See [`NOTICE.md`](NOTICE.md) for sources and attributions.

*This file explains the project's intent and is not legal advice.*
