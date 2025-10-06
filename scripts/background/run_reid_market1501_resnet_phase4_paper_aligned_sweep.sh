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

# Phase 4 Sweep - 논문 설정으로 회귀
# 논문: lr=0.00035, batch=64, num_inst=4, gamma=0.1
# 현재 Phase 3: lr=0.002 (6배 높음!), batch=32, num_inst=2, gamma=0.5
# 목표: 논문 성능 mAP 85.9% 도달
# 예상: 40개 실험, mAP 80-85%

# nohup/비TTY 환경에서 동작하도록 --no-tty 사용

tao_pt \
	--no-tty \
  --mounts_file /home/jongphago/projects/tao_pytorch_backend/docker/tlt_mounts.json \
  --env WANDB_API_KEY="$WANDB_API_KEY" \
  -- python /tao-pt/nvidia_tao_pytorch/cv/re_identification/entrypoint/re_identification.py sweep \
    -e /specs/experiment_market1501_resnet.yaml \
    --sweep-config /sweeps/reid_market1501_resnet_phase4_paper_aligned_sweep.yaml

