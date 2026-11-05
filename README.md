# Eval Forge

A JSONL evaluation runner with strict output checks, per-case diagnostics, and regression gates.

[![tests](https://github.com/izzyfrm/eval-forge/actions/workflows/tests.yml/badge.svg)](https://github.com/izzyfrm/eval-forge/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Built as a focused AI engineering lab: inspectable algorithms, deterministic examples, and explicit failure behavior. Runs offline with the Python standard library. No API keys, model downloads, or paid services.

## Run it

```bash
git clone https://github.com/izzyfrm/eval-forge.git
cd eval-forge
python -m eval_forge examples/cases.jsonl --minimum 1 --report report.json
```

Requires Python 3.11 or newer. Commands run from the repository root and work in PowerShell, bash, and zsh. An editable install with `python -m pip install -e .` also exposes the `eval-forge` command; direct module execution needs no installation.

## How it works

Recorded model outputs → deterministic assertions → per-case checks → aggregate pass rate → process exit code. Exit code 1 means the configured minimum was missed. Exact matches trim surrounding whitespace; substring checks ignore case; regex checks match the whole response. JSON checks validate named top level fields and distinguish booleans from numbers.

## Where it fits

Export responses from your local inference pipeline as JSONL. Keep model and prompt revisions in the dataset filename, compare the same cases between revisions, and use the exit status as a release gate.

## Example output

See [the checked demo output](examples/output.json). It comes from the quickstart command and is a small fixture demonstration, not a performance benchmark.

## Verify

```bash
python -m unittest discover -s tests -v
```

Tests cover core behavior and edge cases. GitHub Actions runs the suite on Python 3.11, 3.12, and 3.13. Local verification is recorded in [VALIDATION.md](VALIDATION.md).

## Limitations and tradeoffs

This evaluates recorded outputs and does not call a model. These are contract checks, not a semantic quality score or a complete JSON Schema implementation. Regex patterns and datasets must be trusted; adversarial regexes can be slow.

## Project layout

| Path | Purpose |
| --- | --- |
| `eval_forge.py` | Importable implementation and CLI |
| `tests/` | Behavioral and failure case tests |
| `examples/` | Reproducible demonstration artifacts |
| `pyproject.toml` | Package metadata and console entry point |

## Related labs

[Evidence Search](https://github.com/izzyfrm/evidence-search) · [Eval Forge](https://github.com/izzyfrm/eval-forge) · [Prompt Vault](https://github.com/izzyfrm/prompt-vault) · [Drift Radar](https://github.com/izzyfrm/drift-radar) · [Route Lab](https://github.com/izzyfrm/route-lab)

## License

MIT. See [LICENSE](LICENSE).
