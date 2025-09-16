"""W&B Sweep launcher for Re-Identification (learning rate sweep).

This script is discovered as a subtask by the common TAO entrypoint. It creates a
Weights & Biases sweep focused on tuning the base learning rate and, for each sweep
trial, launches the regular `train` subtask with an override to `train.optim.base_lr`.

Usage (inside TAO container):
  python /tao-pt/nvidia_tao_pytorch/cv/re_identification/entrypoint/re_identification.py sweep \
      -e /specs/experiment_market1501_resnet.yaml \
      results_dir=/results/market1501 \
      encryption_key=nvidia_tao

Optional flags (parsed by this script, not Hydra):
  --count  Number of sweep runs to execute (default: number of lr values)
  --method Sweep method: grid|random|bayes (default: grid)
  --lr_values Comma-separated lr values (default: 1e-4,3e-4,1e-3,3e-3,1e-2)
"""

import argparse
import os
import shlex
import subprocess
import sys
from typing import List

import wandb
import yaml


def _parse_unknown_results_dir(unknown_args: List[str], default_dir: str) -> str:
    """Extract results_dir from unknown args if present, else return default."""
    for arg in reversed(unknown_args):
        if arg.startswith("results_dir="):
            return arg.split("=", 1)[1]
    return default_dir


def _load_wandb_project_entity(spec_path: str):
    """Return (project, entity) from spec if present; else from env; else defaults."""
    project = os.getenv("WANDB_PROJECT", None)
    entity = os.getenv("WANDB_ENTITY", None)
    try:
        with open(spec_path, "r") as f:
            cfg = yaml.safe_load(f) or {}
        if isinstance(cfg, dict) and "wandb" in cfg and isinstance(cfg["wandb"], dict):
            project = cfg["wandb"].get("project", project)
            entity = cfg["wandb"].get("entity", entity)
    except Exception:
        pass
    return project or "TAO Toolkit", entity


def main():
    parser = argparse.ArgumentParser("re_identification_sweep", add_help=True)
    # These two are injected by the TAO entrypoint from -e/--experiment_spec_file
    parser.add_argument("--config-path", dest="config_path", default="", help="Hydra config path")
    parser.add_argument("--config-name", dest="config_name", required=True, help="Hydra config name (spec file)")

    parser.add_argument("--count", type=int, default=None)
    parser.add_argument("--method", type=str, choices=["grid", "random", "bayes"], default="grid")
    parser.add_argument(
        "--lr_values",
        type=str,
        default="1e-4,3e-4,1e-3,3e-3,1e-2",
        help="Comma-separated list of learning rates to try",
    )
    parser.add_argument(
        "--wd_values",
        type=str,
        default="1e-5,5e-5,1e-4,5e-4,1e-3",
        help="Comma-separated list of weight_decay values to try",
    )

    args, unknown_args = parser.parse_known_args()

    # Mitigate git ownership issues inside container when W&B tries to scan git metadata
    os.environ.setdefault("WANDB_DISABLE_GIT", "true")
    try:
        subprocess.run(["git", "config", "--global", "--add", "safe.directory", "/tao-pt"], check=False)
    except Exception:
        pass

    spec_path = os.path.join(args.config_path, args.config_name) if args.config_path else args.config_name
    if not os.path.exists(spec_path):
        print(f"ERROR: Spec not found at {spec_path}", file=sys.stderr)
        sys.exit(1)

    project, entity = _load_wandb_project_entity(spec_path)

    # Prepare sweep configuration
    lr_values = [float(v) for v in args.lr_values.split(",") if v.strip()]
    wd_values = [float(v) for v in args.wd_values.split(",") if v.strip()]
    sweep_config = {
        "name": "reid_lr_sweep",
        "method": args.method,
        "metric": {"name": "mAP", "goal": "maximize"},
        "parameters": {
            "lr": {"values": lr_values},
            "weight_decay": {"values": wd_values},
        },
    }

    sweep_id = wandb.sweep(sweep_config, project=project, entity=entity)

    # Determine base results_dir and ensure per-run isolation
    base_results_dir = _parse_unknown_results_dir(unknown_args, "/results/reid_sweep")

    def train_sweep():
        # Initialize the sweep run
        run = wandb.init(project=project, entity=entity)
        lr = wandb.config.get("lr")
        weight_decay = wandb.config.get("weight_decay")

        # Derive per-run outputs and consistent W&B run naming
        run_suffix = run.name.replace(" ", "_") if run.name else run.id
        run_results_dir = os.path.join(base_results_dir, "sweep", sweep_id, run_suffix)
        wandb_name_override = run.name if run.name else f"lr_{lr}_wd_{weight_decay}"

        # Build the child training command
        # We call the same entrypoint with subtask `train` and override base_lr + results_dir + wandb.name
        entrypoint_py = "/tao-pt/nvidia_tao_pytorch/cv/re_identification/entrypoint/re_identification.py"
        cmd_parts = [
            sys.executable,
            entrypoint_py,
            "train",
            "-e",
            spec_path,
        ]

        # Pass through any user-provided overrides first, then append our final overrides to take precedence
        cmd_parts.extend(unknown_args)
        cmd_parts.extend([
            f"results_dir={run_results_dir}",
            f"train.optim.base_lr={lr}",
            f"train.optim.weight_decay={weight_decay}",
            f"wandb.name={wandb_name_override}",
        ])

        env = os.environ.copy()
        # Ensure W&B child process attaches to this run
        if run.id:
            env["WANDB_RUN_ID"] = run.id
        if sweep_id:
            env["WANDB_SWEEP_ID"] = sweep_id
        # Allow child process to attach to the same run
        env.setdefault("WANDB_RESUME", "allow")
        # Ensure child doesn't try to scan git metadata
        env.setdefault("WANDB_DISABLE_GIT", "true")

        print("Launching:", shlex.join(cmd_parts))
        try:
            subprocess.run(cmd_parts, check=True, env=env)
        finally:
            # Close the sweep run in this process
            wandb.finish()

    # Execute the sweep trials
    count = args.count if args.count is not None else max(len(lr_values), len(wd_values))
    wandb.agent(sweep_id, function=train_sweep, count=count, project=project, entity=entity)


if __name__ == "__main__":
    main()


