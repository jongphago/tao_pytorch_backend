cd ~/projects/tao_pytorch_backend
cat docker/tlt_mounts.json
source scripts/envsetup.sh

# 현재 쉘 세션에 적용
set -a
source .env
set +a

# 컨테이너 진입 없이 바로 실행
tao_pt --mounts_file /home/jongphago/projects/tao_pytorch_backend/docker/tlt_mounts.json \
  --env WANDB_API_KEY=$WANDB_API_KEY \
  -- python /tao-pt/nvidia_tao_pytorch/cv/re_identification/entrypoint/re_identification.py train \
      -e /specs/experiment_market1501_resnet.yaml \
      results_dir=/results/market1501 \
      encryption_key=nvidia_tao
      

# The data is saved here
export DATA_DIR=/data
export MODEL_DIR=/model
export SPECS_DIR=/specs
export RESULTS_DIR=/results
export KEY=nvidia_tao

tao_pt -- python nvidia_tao_pytorch/cv/re_identification/entrypoint/re_identification.py train \
    -e $SPECS_DIR/experiment_market1501_resnet.yaml \
    results_dir=$RESULTS_DIR/market1501 \
    encryption_key=$KEY



# 컨테이너 진입 없이 바로 실행
tao_pt --mounts_file /home/jongphago/projects/tao_pytorch_backend/docker/tlt_mounts.json \
  --env WANDB_API_KEY=$WANDB_API_KEY \
  --env WANDB_ENTITY=jongphago \
  --env WANDB_START_METHOD=thread \
  -- python /tao-pt/nvidia_tao_pytorch/cv/re_identification/entrypoint/re_identification.py train \
      -e /specs/experiment_market1501_resnet.yaml \
      results_dir=/results/market1501 \
      encryption_key=nvidia_tao