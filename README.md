# disensor-hide-pending

A pre-registered experiment: does a structured record with an explicit place for
what stayed open (the residue schema of [disensor](https://github.com/NicolasRocchia/disensor))
make an AI agent admit that a tool call never returned its results?

The scenario is *Hide Pending Tool Call*, from Huang et al., *Language Models Are
"Insecure" Reporters*, [arXiv:2609.36139](https://arxiv.org/abs/2609.36139). The
subject is `gpt-5.6-sol` running inside Codex CLI, on 100 agent logs, each with a
clean twin in which the query does return.

## Result of phase 1

- With the residue schema, the record states that the query did not return in
  **29 of 100** logs; with a plain findings list, in **5 of 100**. Neither format
  raised it in any of the 100 clean twins.
- The pre-registered test is significant: mean paired effect **0.24** [0.16, 0.33],
  exact sign-flip p = 1.2 × 10⁻⁷.
- But in **71 of 100** logs, the residue record declared that nothing remained open
  while the query was still pending. All 71 passed the schema, and 69 passed every
  validator rule (the other two failed on an unrelated rule): none was rejected for
  being false.

## Start here

| Document | For |
|---|---|
| [`28-W3C-REPORT-PHASE-1.md`](28-W3C-REPORT-PHASE-1.md) | The full report in English: setup, results, pre-registration, limitations. |
| [`30-REPORT-FOR-THE-AUTHORS.md`](30-REPORT-FOR-THE-AUTHORS.md) | Notes for the authors of the source paper: reproducing the recipe, a clean-twin control, the result read against the paper. |
| [`27-RESULTADO-FASE-1.md`](27-RESULTADO-FASE-1.md) | The result, in Spanish. |
| [`29-INFORME-DISENSOR.md`](29-INFORME-DISENSOR.md) | What the result means for disensor, in Spanish. |
| [`01-PROTOCOLO.md`](01-PROTOCOLO.md) | The frozen protocol (v23), in Spanish. |

The working documents are in Spanish and numbered in the order they were written:
reviews of the protocol (`02` to `04`, `16`, `19`, `21` to `23`), harness and pilot
tests (`05` to `15`, `18`), answers to the reviews (`17`, `20`), and the run (`24`
to `26`).

## Reproduce the analysis

```
git clone https://github.com/NicolasRocchia/disensor-hide-pending
cd disensor-hide-pending
python herramientas/prueba_offline.py
python herramientas/corrida.py analizar
```

`prueba_offline.py` runs 142 tests without calling any model (it needs
`jsonschema`; tested with 4.26.0 on Python 3.14.2). `corrida.py analizar`
re-verifies the freeze (it needs a full clone and network access to fetch
`origin/main`), rebuilds the pairs from the stored outputs and rewrites
`corrida/informe.json`; on a fresh clone the file comes out identical. Re-running
the model calls needs Codex CLI 0.153.4 and Claude Code 2.1.285 with the pinned
hashes in `piloto/arnes/binarios.json`, and accounts for both.

## What is where

| Path | Contents |
|---|---|
| `herramientas/` | The harness: log generation and checks, twins, subject calls, judge, validator, analysis (`corrida.py` runs the stages; `analisis.py` holds the test and the decision rules). |
| `prompts/`, `esquemas/` | The frozen judge and twin prompts, and the two schema fragments (residue and placebo). |
| `corrida/` | The run: the seeded draw, the 114 generated logs, the twins and the author's decisions, the frozen list of 100 pairs, the 400 subject outputs (`brazos/`), the 400 judge verdicts (`juez/`), the blind labeling sheet and its labels (`validacion/`), and the analysis (`informe.json`). |
| `piloto/` | The pilot, run before freezing. |
| `Q.1.8-*`, `Q.2.8-*` | The generator and judge prompts of the source paper (Appendix Q, pp. 61 to 64 and 89 to 91), with the layout line breaks undone (`reflow` scripts in `herramientas/`). |
| `protocolo-v0-archivo.md` to `protocolo-v4-archivo.md` | Early drafts of the protocol; later versions are in the git history. |

## Pre-registration

The protocol was frozen at the tag `protocolo-congelado`. The list of 100 pairs was
frozen in `238c1df`, with a freeze record in the protocol's amendments section
(`7d02634`), and both were published to this repository one minute before the
first measured call. The harness refused to run if the list, the code, the prompts
or the schemas changed after that point. The order of everything published is in
[`28-W3C-REPORT-PHASE-1.md`](28-W3C-REPORT-PHASE-1.md#pre-registration-and-external-anchoring).

## Source and disclosure

The scenario, the log generator and the capacity question come from Huang, Fan,
Humayun, Chen, Qin, Chen, Navalpakkam and Gu, *Language Models Are "Insecure"
Reporters*, arXiv:2609.36139 (2026). Their prompts are reproduced here only to make
the experiment reproducible; the paper itself is not included.

The paper is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Its prompts Q.1.8 and Q.2.8 are reproduced here under that license, with changes:
page numbers and running headers removed, and the line breaks of the PDF layout
undone (documented in `00-LEEME-procedencia.md`).

I wrote disensor, the tool whose residue schema this experiment tests. Nicolás
Rocchia.
