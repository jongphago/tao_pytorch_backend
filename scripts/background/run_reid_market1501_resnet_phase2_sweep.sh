#!/usr/bin/env bash
set -euo pipefail

cd /home/jongphago/projects/tao_pytorch_backend

# 선택: 기능 정의만 필요하지만, 사용 중인 환경을 맞추기 위해 활성화 시도
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate || true
fi

# tao_pt 함수 로드
source scripts/envsetup.sh

# .env의 환경 변수를 내보내기(export)하여 하위 프로세스에서도 사용 가능하게 함
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

# Phase 2 Sweep (전략 A: 보수적 접근)
# Phase 1 최적값 기반: batch_size=32, feat_dim=512, gamma=0.3 고정
# 새 매개변수 탐색: warmup_method, num_instances, prob, re_prob, center_loss, flip_feature
# 예상: 60개 실험, mAP 0.70+ 목표

# nohup/비TTY 환경에서 동작하도록 --no-tty 사용

tao_pt \
	--no-tty \
  --mounts_file /home/jongphago/projects/tao_pytorch_backend/docker/tlt_mounts.json \
  --env WANDB_API_KEY="$WANDB_API_KEY" \
  -- python /tao-pt/nvidia_tao_pytorch/cv/re_identification/entrypoint/re_identification.py sweep \
    -e /specs/experiment_market1501_resnet.yaml \
    --sweep-config /sweeps/reid_market1501_resnet_phase2_sweep.yaml

