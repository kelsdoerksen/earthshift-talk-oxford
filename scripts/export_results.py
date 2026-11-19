#!/usr/bin/env python3
"""Turn EarthShift per-task results into data/model_summary.csv for the talk charts.

Input: one or more CSVs with one row per (task, model, protocol), e.g. exported
from the aggregation workbook. Column names are configurable; defaults match the
standard aggregation columns (Task, Model, Avg Test ID, Avg Test OOD) plus a
protocol column (FULL / HEAD). If your file has no protocol column, append
:FULL or :HEAD to the file name.

Task -> shift mapping comes from data/task_to_shift.csv (edit it to match your
task names exactly).

Effective robustness follows the paper (Eq. 1, Taori et al.): within each shift
and protocol, fit OOD = m*ID + b over all model-task points, then
rho = OOD - (m*ID + b). With --center (default, as in Fig 3) rho is centred
within each task so 0 is the average model. Scores are averaged over tasks in a
shift, and the "Overall" row averages the five shifts with equal weight.

Usage:
  python3 scripts/export_results.py results_full.csv:FULL results_head.csv:HEAD
Stdlib only (Python 3.10+).
"""
import argparse
import csv
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FAMILY = {
    # GFMs
    "clay": "GFM", "croma": "GFM", "dofa": "GFM", "prithvi": "GFM",
    "terrafm": "GFM", "terramind": "GFM", "dinov3_large_sat": "GFM",
    # generic pretrained
    "clip": "VFM", "resnet50_imgnet": "VFM", "vit_imgnet": "VFM",
    # random init
    "resnet_random": "Random", "vit_random": "Random",
}
EXCLUDE = {"galileo", "olmoearth", "olmo-earth"}  # not in the paper


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("inputs", nargs="+", help="CSV files as PATH or PATH:PROTOCOL (e.g. full.csv:FULL)")
    p.add_argument("--task-col", default="Task")
    p.add_argument("--model-col", default="Model")
    p.add_argument("--protocol-col", default="Protocol")
    p.add_argument("--id-col", default="Avg Test ID")
    p.add_argument("--ood-col", default="Avg Test OOD")
    p.add_argument("--map", default=str(ROOT / "data" / "task_to_shift.csv"))
    p.add_argument("--out", default=str(ROOT / "data" / "model_summary.csv"))
    p.add_argument("--points", action="store_true", help="multiply scores by 100 (paper's Fig 3 uses points)")
    p.add_argument("--no-center", action="store_true", help="do not centre ER within each task")
    return p


def main():
    args = parse_args().parse_args()
    files, protos = [], []
    for spec in args.inputs:
        path, _, proto = spec.partition(":")
        files.append(path)
        protos.append(proto or None)

    shift_of = {}
    with open(args.map, newline="") as f:
        for r in csv.DictReader(f):
            shift_of[r["task"].strip()] = r["shift"].strip()

    rows = []  # (shift, task, model, protocol, id, ood)
    missing = set()
    for path, proto in zip(files, protos):
        # utf-8-sig drops a BOM; errors="replace" tolerates stray non-UTF-8 bytes in spreadsheet exports
        with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
            for r in csv.DictReader(f):
                model = r[args.model_col].strip()
                if model.lower() in EXCLUDE:
                    continue
                task = r[args.task_col].strip()
                if task not in shift_of:
                    missing.add(task)
                    continue
                prot = proto or r.get(args.protocol_col, "").strip()
                if not prot:
                    sys.exit(f"No protocol for {path}; pass it as {path}:FULL or {path}:HEAD")
                try:
                    idv, oodv = float(r[args.id_col]), float(r[args.ood_col])
                except (ValueError, KeyError):
                    continue
                k = 100.0 if args.points else 1.0
                rows.append((shift_of[task], task, model, prot.upper(), idv * k, oodv * k))
    if missing:
        print("WARNING: tasks missing from task_to_shift.csv (skipped):", ", ".join(sorted(missing)), file=sys.stderr)
    if not rows:
        sys.exit("No rows read — check column names (--id-col, --ood-col, ...)")

    # per (shift, protocol) linear fit across all model-task points
    groups = defaultdict(list)
    for s, t, m, pr, i_, o_ in rows:
        groups[(s, pr)].append((i_, o_))
    fit = {g: st.linear_regression([x for x, _ in pts], [y for _, y in pts]) for g, pts in groups.items()}

    er = {}
    for s, t, m, pr, i_, o_ in rows:
        sl, ic = fit[(s, pr)]
        er[(s, t, m, pr)] = o_ - (sl * i_ + ic)
    if not args.no_center:
        by_task = defaultdict(list)
        for (s, t, m, pr), v in er.items():
            by_task[(s, t, pr)].append(v)
        means = {k: st.fmean(v) for k, v in by_task.items()}
        er = {(s, t, m, pr): v - means[(s, t, pr)] for (s, t, m, pr), v in er.items()}

    agg = defaultdict(lambda: {"id": [], "ood": [], "er": []})
    for s, t, m, pr, i_, o_ in rows:
        a = agg[(m, pr, s)]
        a["id"].append(i_); a["ood"].append(o_); a["er"].append(er[(s, t, m, pr)])

    out = []
    per_model = defaultdict(lambda: defaultdict(list))
    for (m, pr, s), a in sorted(agg.items()):
        rec = {k: st.fmean(v) for k, v in a.items()}
        out.append((m, pr, s, rec))
        for k, v in rec.items():
            per_model[(m, pr)][k].append(v)
    for (m, pr), d in sorted(per_model.items()):
        n_shifts = len(d["id"])
        if n_shifts < 5:
            print(f"NOTE: {m} {pr} has only {n_shifts}/5 shifts; Overall row averages what exists", file=sys.stderr)
        out.append((m, pr, "Overall", {k: st.fmean(v) for k, v in d.items()}))

    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "family", "protocol", "shift", "id", "ood", "er"])
        for m, pr, s, rec in out:
            w.writerow([m, FAMILY.get(m.lower(), "Other"), pr, s,
                        f"{rec['id']:.4f}", f"{rec['ood']:.4f}", f"{rec['er']:.4f}"])
    print(f"Wrote {len(out)} rows to {args.out}")
    for (s, pr), (sl, ic) in sorted(fit.items()):
        print(f"  fit {pr:4s} {s:10s} OOD = {sl:.3f}*ID {ic:+.3f}")


if __name__ == "__main__":
    main()
