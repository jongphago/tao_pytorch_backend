# TAO Pytorch Backend W&B 구현 분석 보고서

## 목차

1. [서론](#서론)
2. [본론](#본론)
   - 2.1 [W&B 구현 아키텍처](#21-wb-구현-아키텍처)
   - 2.2 [핵심 컴포넌트](#22-핵심-컴포넌트)
   - 2.3 [설정 구조](#23-설정-구조)
   - 2.4 [초기화 및 실행 흐름](#24-초기화-및-실행-흐름)
   - 2.5 [메트릭 로깅](#25-메트릭-로깅)
   - 2.6 [Sweep 기능](#26-sweep-기능)
   - 2.7 [환경 설정](#27-환경-설정)
3. [결론](#결론)
4. [참조 목록](#참조-목록)

---

## 서론

본 보고서는 NVIDIA TAO Pytorch Backend 프로젝트의 Re-Identification 모델에서 구현된 Weights & Biases(W&B) 연동을 분석한 문서입니다. 분석 목적은 동일한 W&B 설정을 다른 프로젝트(`~/projects/reid-strong-baseline`)에 적용하기 위한 참고 자료로 활용하는 것입니다.

분석 대상은 다음과 같습니다:
- Re-Identification 모델의 W&B 통합 구조
- 설정 파일 구성 방식
- PyTorch Lightning과의 연동
- Hyperparameter Sweep 구현
- 환경 변수 및 인증 처리

---

## 본론

### 2.1 W&B 구현 아키텍처

TAO Pytorch Backend는 계층적 구조로 W&B를 구현하고 있습니다:

```
nvidia_tao_pytorch/
├── core/
│   ├── common_config.py           # WandBConfig 정의
│   ├── initialize_experiments.py  # W&B 로거 초기화
│   └── mlops/
│       └── wandb.py               # W&B 유틸리티 함수
└── cv/
    └── re_identification/
        ├── config/
        │   └── default_config.py  # ExperimentConfig 정의
        ├── experiment_specs/
        │   └── experiment_market1501_resnet.yaml  # 실험 설정
        ├── model/
        │   └── pl_reid_model.py   # PyTorch Lightning 모델 (로깅 구현)
        ├── scripts/
        │   ├── train.py           # 훈련 엔트리포인트
        │   └── sweep.py           # W&B Sweep 실행
        └── sweeps/
            └── *.yaml             # Sweep 설정 파일
```

### 2.2 핵심 컴포넌트

#### 2.2.1 WandBConfig 데이터클래스

W&B 설정을 위한 데이터클래스가 코어 모듈에 정의되어 있습니다:

```python
@dataclass
class WandBConfig:
    """Configuration element wandb client."""
    
    enable: bool = BOOL_FIELD(value=True)
    project: str = STR_FIELD(value="TAO Toolkit")
    entity: Optional[str] = STR_FIELD(value="")
    tags: List[str] = LIST_FIELD(arrList=["tao-toolkit"])
    reinit: bool = BOOL_FIELD(value=False)
    sync_tensorboard: bool = BOOL_FIELD(value=False)
    save_code: bool = BOOL_FIELD(value=False)
    name: str = BOOL_FIELD(value="TAO Toolkit Training")
```

이 설정은 `CommonExperimentConfig`에 기본적으로 포함됩니다.

#### 2.2.2 W&B 유틸리티 함수

W&B 연동을 위한 핵심 함수들:

**check_wandb_logged_in()**
- WANDB_API_KEY 환경 변수 확인
- ~/.netrc 파일 존재 확인
- wandb.login() 호출

**initialize_wandb()**
- WandbLogger 인스턴스 생성
- PyTorch Lightning과 호환되는 로거 반환
- 타임스탬프를 포함한 실험 이름 자동 생성
- TensorBoard 동기화 옵션 제공

#### 2.2.3 PyTorch Lightning 통합

`ReIdentificationModel` 클래스는 `TAOLightningModule`을 상속하며, PyTorch Lightning의 `self.log()` 메서드를 사용하여 자동으로 W&B에 메트릭을 기록합니다.

### 2.3 설정 구조

#### 2.3.1 YAML 설정 파일 구조

실험 설정 파일에서 W&B 섹션을 추가하여 설정합니다:

```yaml
results_dir: "/results/market1501"
encryption_key: nvidia_tao

model:
  backbone: resnet_50
  feat_dim: 256
  # ... 기타 모델 설정

dataset:
  train_dataset_dir: "/data/market1501/bounding_box_train"
  batch_size: 64
  # ... 기타 데이터셋 설정

train:
  num_epochs: 5
  checkpoint_interval: 1
  optim:
    name: Adam
    base_lr: 0.00035
    # ... 기타 옵티마이저 설정

wandb:
  enable: true
  project: "TAO Toolkit"
  entity: "jongphago"
  tags: ["training", "reid", "market1501"]
  name: "reid_resnet50"
```

#### 2.3.2 설정 필드 상세

- `enable`: W&B 로깅 활성화/비활성화
- `project`: W&B 프로젝트 이름
- `entity`: W&B 팀/사용자 계정 (선택)
- `tags`: 실험 태그 리스트
- `name`: 실험 이름 (타임스탬프가 자동 추가됨)
- `sync_tensorboard`: TensorBoard 로그 동기화 여부
- `save_code`: 코드 저장 여부

### 2.4 초기화 및 실행 흐름

#### 2.4.1 훈련 초기화 프로세스

1. **실험 설정 로드** (`train.py`)
   - Hydra로 YAML 설정 로드
   - ExperimentConfig 스키마 검증

2. **W&B 로거 초기화** (`initialize_experiments.py`)
   - WANDB_API_KEY 확인
   - `wandb.login()` 실행
   - WandbLogger 생성
   - PyTorch Lightning Trainer에 로거 추가

3. **모델 및 데이터 준비**
   - REIDDataModule 초기화
   - ReIdentificationModel 초기화

4. **Trainer 실행**
   - 로거 리스트 전달 (TensorBoard + WandB)
   - 훈련 시작

#### 2.4.2 초기화 코드 흐름

```python
# initialize_experiments.py에서 W&B 로거 생성
if hasattr(cfg, "wandb"):
    wandb_config = cfg.wandb
    wandb_logged_in = check_wandb_logged_in()
    if wandb_logged_in and wandb_config.enable:
        wandb_logger = initialize_wandb(
            project=wandb_config.project,
            entity=wandb_config.entity,
            name=wandb_config.name,
            results_dir=results_dir,
            wandb_logged_in=wandb_logged_in,
            tags=wandb_config.tags,
            config=dict(cfg)
        )
        loggers.append(wandb_logger)
```

```python
# train.py에서 Trainer에 로거 전달
trainer = Trainer(
    logger=ptl_loggers,  # [TensorBoardLogger, WandbLogger]
    devices=len(gpus),
    max_epochs=num_epochs,
    # ... 기타 설정
)
trainer.fit(reid_model, dm, ckpt_path=resume_ckpt)
```

### 2.5 메트릭 로깅

#### 2.5.1 훈련 메트릭

`training_step()` 메서드에서 자동 로깅:

```python
def training_step(self, batch, batch_idx):
    data, label = batch
    # ... 모델 추론
    loss = self.my_loss_func(score, feat, label)
    self.train_accuracy.update(score, label)
    
    # W&B 자동 로깅
    self.log("train_loss", loss, on_step=True, on_epoch=True, 
             prog_bar=True, sync_dist=True, batch_size=batch_size)
    self.log("base_lr", self.scheduler.get_lr()[0], 
             on_step=False, on_epoch=True, prog_bar=True)
    self.log("train_acc_1", self.train_accuracy, 
             on_step=True, on_epoch=False, prog_bar=True)
    
    return loss
```

로깅되는 훈련 메트릭:
- `train_loss`: 스텝별 및 에포크별 손실
- `base_lr`: 현재 학습률
- `train_acc_1`: 훈련 정확도

#### 2.5.2 검증 메트릭

`on_validation_epoch_end()` 메서드에서 평가 메트릭 로깅:

```python
def on_validation_epoch_end(self):
    if self.trainer.global_rank == 0:
        cmc, mAP = self.metrics.compute()
        
        # CMC Rank 로깅
        for r in [1, 5, 10]:
            self.log(f"cmc_rank_{r}", cmc[r - 1], 
                     on_step=False, on_epoch=True, 
                     prog_bar=True, sync_dist=True, rank_zero_only=True)
        
        # mAP 로깅
        self.log("mAP", mAP, on_step=False, on_epoch=True, 
                 prog_bar=True, sync_dist=True, rank_zero_only=True)
```

로깅되는 검증 메트릭:
- `cmc_rank_1`, `cmc_rank_5`, `cmc_rank_10`: Cumulative Matching Characteristics
- `mAP`: Mean Average Precision

#### 2.5.3 로깅 옵션

- `on_step`: 매 스텝마다 로깅
- `on_epoch`: 에포크 종료 시 로깅
- `prog_bar`: Progress bar에 표시
- `sync_dist`: 분산 훈련 시 동기화
- `rank_zero_only`: Rank 0 프로세스에서만 로깅

### 2.6 Sweep 기능

#### 2.6.1 Sweep 구조

W&B Sweep 기능이 `scripts/sweep.py`에 완전히 구현되어 있습니다. 주요 특징:

- Grid, Random, Bayesian 서치 지원
- 다양한 하이퍼파라미터 튜닝 가능
- 각 실험마다 독립적인 결과 디렉토리 생성
- Early Termination (Hyperband) 지원

#### 2.6.2 Sweep 설정 파일 예시

```yaml
name: reid_market1501_resnet_perf_sweep
method: random
metric:
  name: mAP
  goal: maximize
parameters:
  lr: [1.0e-4, 3.0e-4, 1.0e-3, 3.0e-3, 1.0e-2]
  weight_decay: [1.0e-5, 5.0e-5, 1.0e-4, 5.0e-4, 1.0e-3]
  warmup_factor: [0.01, 0.05, 0.1]
  warmup_iters: [0, 10, 20]
  triplet_loss_margin: [0.2, 0.3, 0.4]
count: 0  # 0이면 전체 조합 실행
results_dir_base: /results/market1501/resnet50
early_terminate:
  type: hyperband
  max_iter: 12
  s: 2
  eta: 3
  min_iter: 3
```

#### 2.6.3 Sweep 지원 하이퍼파라미터

기본 하이퍼파라미터:
- `lr`: 학습률
- `weight_decay`: 가중치 감쇠
- `warmup_factor`: 워밍업 시작 배율
- `warmup_iters`: 워밍업 반복 횟수
- `triplet_loss_margin`: 트리플릿 손실 마진

추가 지원 하이퍼파라미터:
- `batch_size`: 배치 크기
- `feat_dim`: 특징 차원
- `gamma`: 학습률 감쇠율
- `warmup_method`: 워밍업 방법 (linear/cosine)
- `num_instances`: ID당 인스턴스 수
- `prob`: 변환 확률
- `re_prob`: 재변환 확률
- `with_center_loss`: 센터 로스 사용 여부
- `with_flip_feature`: 플립 피처 사용 여부

#### 2.6.4 Sweep 실행 프로세스

1. **Sweep 초기화**
   - W&B 서버에 Sweep 생성
   - Sweep ID 발급

2. **Agent 실행**
   - `wandb.agent()` 호출
   - 각 시도마다 `train_sweep()` 함수 실행

3. **훈련 서브프로세스 실행**
   - 새로운 프로세스로 train 명령 실행
   - 하이퍼파라미터 오버라이드 전달
   - WANDB_RUN_ID, WANDB_SWEEP_ID 환경 변수 설정

4. **결과 수집**
   - W&B에서 자동으로 메트릭 수집
   - 최적 하이퍼파라미터 선택

#### 2.6.5 Sweep 실행 명령

```bash
# Sweep 설정 파일 사용
python re_identification.py sweep \
  -e /specs/experiment_market1501_resnet.yaml \
  --sweep-config /specs/reid_market1501_resnet_sweep.yaml

# CLI 옵션 사용
python re_identification.py sweep \
  -e /specs/experiment_market1501_resnet.yaml \
  --method random \
  --count 10 \
  --lr_values "1e-4,3e-4,1e-3"

# 기존 Sweep 재개
python re_identification.py sweep \
  -e /specs/experiment_market1501_resnet.yaml \
  --sweep_id <SWEEP_ID>
```

### 2.7 환경 설정

#### 2.7.1 WANDB_API_KEY 설정

W&B 인증을 위한 API 키는 다음 방법으로 제공:

**방법 1: 환경 변수** (권장)
```bash
export WANDB_API_KEY="your_api_key_here"
```

**방법 2: Docker 환경 변수 주입**
```json
{
  "Envs": [
    {
      "variable": "WANDB_API_KEY",
      "value": "your_api_key_here"
    }
  ]
}
```

**방법 3: ~/.netrc 파일**
```
machine api.wandb.ai
  login user
  password your_api_key_here
```

#### 2.7.2 Docker 마운트 설정

TAO 런처 사용 시 필요한 마운트 설정:

```json
{
  "Mounts": [
    {
      "source": "/host/path/to/experiments",
      "destination": "/workspace/tao-experiments"
    },
    {
      "source": "/host/path/to/data",
      "destination": "/data"
    },
    {
      "source": "/host/path/to/results",
      "destination": "/results"
    }
  ],
  "DockerOptions": {
    "shm_size": "16G",
    "ulimits": {
      "memlock": -1,
      "stack": 67108864
    }
  },
  "Envs": [
    {
      "variable": "WANDB_API_KEY",
      "value": "$WANDB_API_KEY"
    }
  ]
}
```

#### 2.7.3 인증 확인 프로세스

`check_wandb_logged_in()` 함수의 동작:

1. `WANDB_API_KEY` 환경 변수 확인
2. `~/.netrc` 파일 존재 확인
3. `wandb.login(key=wandb_api_key)` 호출
4. 성공 시 True 반환, 실패 시 False 반환

인증 실패 시 W&B 로깅이 비활성화되며, 경고 메시지가 출력됩니다.

#### 2.7.4 추가 환경 변수

Sweep 실행 시 자동 설정되는 환경 변수:

- `WANDB_DISABLE_GIT`: Git 메타데이터 스캔 비활성화
- `WANDB_RUN_ID`: 현재 실행 ID
- `WANDB_SWEEP_ID`: Sweep ID
- `WANDB_RESUME`: 실행 재개 허용
- `WANDB_START_METHOD`: 시작 방법 (thread)

---

## 결론

### 핵심 요약

TAO Pytorch Backend의 W&B 구현은 다음과 같은 특징을 가집니다:

1. **계층적 구조**: 코어 모듈에서 공통 설정과 유틸리티를 제공하고, 각 CV 태스크에서 이를 활용
2. **PyTorch Lightning 통합**: `self.log()` 메서드를 통한 자동 로깅
3. **유연한 설정**: YAML 파일에서 모든 W&B 옵션 제어 가능
4. **완전한 Sweep 지원**: 다양한 하이퍼파라미터 튜닝 및 Early Termination
5. **환경 변수 기반 인증**: WANDB_API_KEY를 통한 안전한 인증

### 다른 프로젝트 적용 시 고려사항

`reid-strong-baseline` 프로젝트에 적용 시 필요한 작업:

1. **설정 구조 구현**
   - WandBConfig 데이터클래스 추가
   - ExperimentConfig에 wandb 필드 포함

2. **초기화 로직 구현**
   - check_wandb_logged_in() 함수 구현
   - initialize_wandb() 함수 구현
   - 훈련 초기화에서 WandbLogger 추가

3. **PyTorch Lightning 통합**
   - LightningModule에서 self.log() 호출
   - Trainer에 WandbLogger 전달

4. **Sweep 기능 (선택)**
   - sweep.py 스크립트 작성
   - Sweep 설정 YAML 파일 작성

5. **환경 설정**
   - WANDB_API_KEY 설정
   - Docker/런처 설정 파일 업데이트

### 장점

- **최소한의 코드 수정**: PyTorch Lightning 사용 시 self.log()만 호출하면 자동 연동
- **유연한 제어**: YAML 파일에서 모든 설정 관리
- **완전한 기능**: 기본 로깅부터 고급 Sweep까지 모두 지원
- **재현성**: 설정 파일 저장으로 실험 재현 가능

---

## 참조 목록

### 설정 및 구조

- `nvidia_tao_pytorch/core/common_config.py:126-136`
  - WandBConfig 클래스 정의

- `nvidia_tao_pytorch/core/common_config.py:145-151`
  - CommonExperimentConfig에 wandb 필드 포함

- `nvidia_tao_pytorch/cv/re_identification/config/default_config.py:173-203`
  - ExperimentConfig 클래스 정의 (CommonExperimentConfig 상속)

### 초기화 및 유틸리티

- `nvidia_tao_pytorch/core/mlops/wandb.py:53-63`
  - check_wandb_logged_in() 함수

- `nvidia_tao_pytorch/core/mlops/wandb.py:66-127`
  - initialize_wandb() 함수

- `nvidia_tao_pytorch/core/initialize_experiments.py:76-89`
  - 훈련 초기화에서 W&B 로거 추가

### 훈련 및 로깅

- `nvidia_tao_pytorch/cv/re_identification/scripts/train.py:45-76`
  - run_experiment() 함수, Trainer 설정

- `nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:152-176`
  - training_step() 메서드, 훈련 메트릭 로깅

- `nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:178-191`
  - on_train_epoch_end() 메서드

- `nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:200-208`
  - validation_step() 메서드

- `nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:209-228`
  - on_validation_epoch_end() 메서드, 검증 메트릭 로깅

### Sweep 기능

- `nvidia_tao_pytorch/cv/re_identification/scripts/sweep.py:1-381`
  - 전체 Sweep 구현

- `nvidia_tao_pytorch/cv/re_identification/scripts/sweep.py:38-50`
  - _load_wandb_project_entity() 함수

- `nvidia_tao_pytorch/cv/re_identification/scripts/sweep.py:178-212`
  - Sweep 설정 구성

- `nvidia_tao_pytorch/cv/re_identification/scripts/sweep.py:220-329`
  - train_sweep() 함수, 실제 훈련 실행

### 설정 파일 예시

- `nvidia_tao_pytorch/cv/re_identification/experiment_specs/experiment_market1501_resnet.yaml:56-62`
  - wandb 섹션 설정 예시

- `nvidia_tao_pytorch/cv/re_identification/sweeps/reid_market1501_resnet_final_config.yaml:66-74`
  - wandb 섹션 설정 예시 (최종 모델)

- `nvidia_tao_pytorch/cv/re_identification/sweeps/reid_market1501_resnet_sweep.yaml:1-19`
  - Sweep 설정 파일 예시

### 디렉토리 구조

```
/home/jongphago/projects/tao_pytorch_backend/
├── nvidia_tao_pytorch/
│   ├── core/
│   │   ├── common_config.py
│   │   ├── initialize_experiments.py
│   │   └── mlops/
│   │       └── wandb.py
│   └── cv/
│       └── re_identification/
│           ├── config/
│           │   ├── default_config.py
│           │   └── default_config.md
│           ├── experiment_specs/
│           │   ├── experiment_market1501_resnet.yaml
│           │   └── experiment_market1501_swin.yaml
│           ├── model/
│           │   └── pl_reid_model.py
│           ├── scripts/
│           │   ├── train.py
│           │   └── sweep.py
│           └── sweeps/
│               ├── reid_market1501_resnet_sweep.yaml
│               └── reid_market1501_resnet_final_config.yaml
```

### 외부 문서

- [TAO Toolkit - Running from Source](https://docs.nvidia.com/tao/tao-toolkit/text/quick_start_guide/advanced.html#running-tao-from-source)
- [Weights & Biases Documentation](https://docs.wandb.ai/)
- [PyTorch Lightning Loggers](https://pytorch-lightning.readthedocs.io/en/stable/extensions/logging.html)
- [W&B Sweeps](https://docs.wandb.ai/guides/sweeps)

---

**보고서 생성일**: 2025-10-15  
**분석 대상 프로젝트**: `/home/jongphago/projects/tao_pytorch_backend`  
**적용 대상 프로젝트**: `~/projects/reid-strong-baseline`

