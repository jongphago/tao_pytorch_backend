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
    parser.add_argument("--method", type=str, choices=["grid", "random", "bayes"], default=None)
    parser.add_argument(
        "--sweep_id",
        type=str,
        default=None,
        help="Existing W&B sweep ID to resume. If set, no new sweep is created.",
    )
    parser.add_argument(
        "--sweep-config",
        type=str,
        default=None,
        help="Path to a YAML file containing sweep settings (name, method, parameters, count, results_dir_base).",
    )
    parser.add_argument(
        "--lr_values",
        type=str,
        default=None,
        help="Comma-separated list of learning rates to try",
    )
    parser.add_argument(
        "--wd_values",
        type=str,
        default=None,
        help="Comma-separated list of weight_decay values to try",
    )
    parser.add_argument(
        "--warmup_factor_values",
        type=str,
        default=None,
        help="Comma-separated list of warmup_factor values to try",
    )
    parser.add_argument(
        "--warmup_iters_values",
        type=str,
        default=None,
        help="Comma-separated list of warmup_iters values to try",
    )
    parser.add_argument(
        "--triplet_margin_values",
        type=str,
        default=None,
        help="Comma-separated list of triplet_loss_margin values to try",
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

    # Prepare sweep configuration (from optional YAML file, then CLI overrides, then defaults)
    def _as_list(v):
        if v is None:
            return None
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            return [s for s in v.split(",") if s.strip()]
        return [v]

    sweep_cfg = {}
    if args.sweep_config:
        try:
            with open(args.sweep_config, "r") as f:
                sweep_cfg = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"WARNING: Failed to load sweep config '{args.sweep_config}': {e}")
            sweep_cfg = {}

    cfg_params = sweep_cfg.get("parameters", {}) if isinstance(sweep_cfg, dict) else {}

    method = args.method or sweep_cfg.get("method") or "grid"
    name = sweep_cfg.get("name", "reid_resnet_perf_sweep")
    metric = sweep_cfg.get("metric", {"name": "mAP", "goal": "maximize"})

    lr_values_raw = _as_list(args.lr_values) or cfg_params.get("lr") or ["1e-4", "3e-4", "1e-3", "3e-3", "1e-2"]
    wd_values_raw = _as_list(args.wd_values) or cfg_params.get("weight_decay") or ["1e-5", "5e-5", "1e-4", "5e-4", "1e-3"]
    wf_values_raw = _as_list(args.warmup_factor_values) or cfg_params.get("warmup_factor") or ["0.01", "0.05", "0.1"]
    wi_values_raw = _as_list(args.warmup_iters_values) or cfg_params.get("warmup_iters") or [0, 10, 20]
    margin_values_raw = _as_list(args.triplet_margin_values) or cfg_params.get("triplet_loss_margin") or [0.2, 0.3, 0.4]

    lr_values = [float(v) for v in lr_values_raw]
    wd_values = [float(v) for v in wd_values_raw]
    wf_values = [float(v) for v in wf_values_raw]
    wi_values = [int(float(v)) for v in wi_values_raw]
    margin_values = [float(v) for v in margin_values_raw]

    sweep_config = {
        "name": name,
        "method": method,
        "metric": metric,
        "parameters": {
            "lr": {"values": lr_values},
            "weight_decay": {"values": wd_values},
            "warmup_factor": {"values": wf_values},
            "warmup_iters": {"values": wi_values},
            "triplet_loss_margin": {"values": margin_values},
        },
    }
    # early_terminate 설정이 있으면 추가
    if sweep_cfg.get("early_terminate", None):
        sweep_config["early_terminate"] = sweep_cfg.get("early_terminate")

    sweep_id = args.sweep_id if args.sweep_id else wandb.sweep(sweep_config, project=project, entity=entity)

    # Determine base results_dir and ensure per-run isolation
    cfg_base_dir = sweep_cfg.get("results_dir_base", "/results/reid_sweep") if isinstance(sweep_cfg, dict) else "/results/reid_sweep"
    base_results_dir = _parse_unknown_results_dir(unknown_args, cfg_base_dir)

    def train_sweep():
        # Initialize the sweep run
        run = wandb.init(project=project, entity=entity)
        lr = wandb.config.get("lr")
        weight_decay = wandb.config.get("weight_decay")
        warmup_factor = wandb.config.get("warmup_factor")
        warmup_iters = wandb.config.get("warmup_iters")
        triplet_loss_margin = wandb.config.get("triplet_loss_margin")

        # Derive per-run outputs and consistent W&B run naming
        run_suffix = run.name.replace(" ", "_") if run.name else run.id
        run_results_dir = os.path.join(base_results_dir, "sweep", sweep_id, run_suffix)
        # Compose name without None values
        if run.name:
            wandb_name_override = run.name
        else:
            name_parts = []
            if lr is not None:
                name_parts.append(f"lr_{lr}")
            if weight_decay is not None:
                name_parts.append(f"wd_{weight_decay}")
            if warmup_factor is not None:
                name_parts.append(f"wf_{warmup_factor}")
            if warmup_iters is not None:
                name_parts.append(f"wi_{warmup_iters}")
            if triplet_loss_margin is not None:
                name_parts.append(f"m_{triplet_loss_margin}")
            wandb_name_override = "_".join(name_parts) if name_parts else run_suffix

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
        cmd_parts.extend([f"results_dir={run_results_dir}"])
        if lr is not None:
            cmd_parts.append(f"train.optim.base_lr={lr}")
        if weight_decay is not None:
            cmd_parts.append(f"train.optim.weight_decay={weight_decay}")
        if warmup_factor is not None:
            cmd_parts.append(f"train.optim.warmup_factor={warmup_factor}")
        if warmup_iters is not None:
            cmd_parts.append(f"train.optim.warmup_iters={warmup_iters}")
        if triplet_loss_margin is not None:
            cmd_parts.append(f"train.optim.triplet_loss_margin={triplet_loss_margin}")
        cmd_parts.append(f"wandb.name={wandb_name_override}")

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
    if args.sweep_id:
        # When attaching to an existing sweep, default to agent-managed count unless user overrides
        count = args.count
    else:
        total_grid = (
            len(lr_values)
            * len(wd_values)
            * len(wf_values)
            * len(wi_values)
            * len(margin_values)
        )
        cfg_count = None
        if isinstance(sweep_cfg, dict):
            cfg_count = sweep_cfg.get("count", None)
        if args.count is not None:
            count = args.count
        elif cfg_count not in (None, 0):
            try:
                count = int(cfg_count)
            except Exception:
                count = total_grid
        else:
            count = total_grid
    wandb.agent(sweep_id, function=train_sweep, count=count, project=project, entity=entity)


if __name__ == "__main__":
    main()


