---
marp: false
theme: rose-pine-moon-report
paginate: true
marpit: true
headingDivider: [1,2,3]
---

# 📊 ReIdentificationNet W&B Sweep 매개변수 최적화 업데이트 요약

## 📈 1. 기존 실험 (c4s4yfvh) 분석 결과

### 실험 개요
- **총 실험 수**: 34개
- **실험 상태**: 모두 RUNNING 상태에서 중단 (일부 epoch만 완료)
- **mAP 기록**: 34개 전체

### 성능 분포

| 지표       | 값         |
| ---------- | ---------- |
| 최고 mAP   | 0.6954     |
| 최저 mAP   | 0.0387     |
| 평균 mAP   | 0.3991     |
| 중앙값 mAP | 0.5219     |
| mAP > 0.6  | 10개 (29%) |
| mAP < 0.1  | 9개 (26%)  |

### 최고 성능 실험: driven-sweep-9
- **mAP**: 0.6954
- **lr**: 0.003
- **weight_decay**: 0.001
- **warmup_factor**: 0.1
- **warmup_iters**: 10
- **triplet_loss_margin**: 0.3


## 🔍 2. 매개변수별 성능 인사이트

### 핵심 발견 사항

#### 1️⃣ Learning Rate (가장 중요!)
- ✅ **최적**: lr = 0.001~0.003 (평균 mAP 0.55-0.61)
- ❌ **피해야 함**: lr = 0.0001 (평균 mAP 0.07)
- **결론**: lr이 너무 작으면 학습 실패

#### 2️⃣ Weight Decay
- ✅ **최적**: 극단값 (1e-5 또는 0.001) (평균 mAP 0.59-0.60)
- ⚠️ **중간값**: 0.0001~0.0005 (평균 mAP 0.24)
- **결론**: 극단값이 중간값보다 효과적

#### 3️⃣ Warmup Factor
- ✅ **최적**: 0.1 (평균 mAP 0.50)
- ⚠️ 0.01: (평균 mAP 0.39)
- ⚠️ 0.05: (평균 mAP 0.33)
- **결론**: 0.1이 가장 안정적

#### 4️⃣ Warmup Iters
- ✅ **최적**: 0 또는 10 (평균 mAP 0.44)
- ⚠️ 20: (평균 mAP 0.34)
- **결론**: 너무 긴 warmup은 비효율적

#### 5️⃣ Triplet Loss Margin
- ✅ **최적**: 0.4 (평균 mAP 0.48)
- → 0.3 (평균 mAP 0.41)
- ⚠️ 0.2 (평균 mAP 0.33)
- **결론**: 큰 마진이 더 효과적


## 🎯 3. 새로운 최적화 전략 (4가지)

### 기존 설정 (reid_market1501_resnet_sweep.yaml)
- **매개변수**: 5개 (lr, weight_decay, warmup_factor, warmup_iters, triplet_loss_margin)
- **방법**: random
- **문제점**: 저성능 조합 많음 (26% mAP < 0.1)

### 전략별 비교

| 전략          | 매개변수 | 실험 횟수 | 예상 mAP  | 소요시간 | 추천순위       |
| ------------- | -------- | --------- | --------- | -------- | -------------- |
| Improved      | 5개      | 50회      | 0.65-0.70 | 짧음     | 4위 (안전)     |
| **Phase 1** ⭐ | **8개**  | **100회** | **0.70+** | **중간** | **1위 (추천)** |
| Phase 2       | 11개     | 80회      | 0.75+     | 중간     | 2위 (고급)     |
| Aggressive    | 12개     | 200회     | 0.70-0.80 | 김       | 3위 (공격)     |


## 📁 4. 생성된 파일

### Sweep 설정 파일
```
nvidia_tao_pytorch/cv/re_identification/sweeps/
├── reid_market1501_resnet_sweep.yaml           (기존)
├── reid_market1501_resnet_improved_sweep.yaml  (신규) ⚡ 빠른 개선
├── reid_market1501_resnet_phase1_sweep.yaml    (신규) ⭐ 추천
├── reid_market1501_resnet_phase2_sweep.yaml    (신규) 🔬 고급 최적화
└── reid_market1501_resnet_aggressive_sweep.yaml(신규) 💪 공격적 탐색
```

### 실행 코드
```
nvidia_tao_pytorch/cv/re_identification/scripts/
└── sweep.py (수정) ✅
    - 9개 추가 매개변수 지원
    - 동적 sweep_config 생성
    - Hydra 경로 매핑
```


## 🚀 5. 실행 계획 (추천)

### Phase 1 실행 (지금 시작) ⭐

```bash
# 1. 컨테이너 접속
tao_pt \
  --mounts_file $REPOSITORY_ROOT/docker/tlt_mounts.json \
  --env WANDB_API_KEY=$WANDB_API_KEY

# 2. Sweep 실행
sweep \
  -e /specs/experiment_market1501_resnet.yaml \
  --sweep-config /sweeps/reid_market1501_resnet_phase1_sweep.yaml \
  results_dir=/results \
  encryption_key=nvidia_tao

# 3. 결과 경로
# /results/results/market1501/resnet50/phase1/sweep/{sweep_id}/
```

**예상 결과**:
- 100개 실험 (Bayes Search로 효율적)
- mAP 0.70+ 달성 가능
- 실험 시간: 중간 (기존 대비 3배)

### Phase 2 실행 (Phase 1 완료 후)

```bash
# Phase 1 최적값으로 phase2_sweep.yaml 수정 후 실행
sweep \
  -e /specs/experiment_market1501_resnet.yaml \
  --sweep-config /sweeps/reid_market1501_resnet_phase2_sweep.yaml \
  results_dir=/results \
  encryption_key=nvidia_tao
```

**예상 결과**:
- 80개 실험
- mAP 0.75+ 달성 목표
- 데이터 증강/손실 함수 최적화


## 📊 6. 전략별 상세 비교

### 전략 1: Improved Sweep (빠른 개선)

**매개변수 (5개)**:
- `lr`: [1e-3, 2e-3, 3e-3, 5e-3] ← 0.0001 제거
- `weight_decay`: [1e-5, 5e-5, 1e-3] ← 중간값 제거
- `warmup_factor`: [0.05, 0.1] ← 0.01 제거
- `warmup_iters`: [0, 10] ← 20 제거
- `triplet_loss_margin`: [0.3, 0.4] ← 0.2 제거

**설정**:
- method: bayes
- count: 50
- 예상 조합: ~96개

**장점**: 빠른 개선, 안정적  
**단점**: 제한적 성능 향상


### 전략 2: Phase 1 Sweep (단계적 확장) ⭐ 추천

**매개변수 (8개)**:

기존 5개 + 추가 3개
- `batch_size`: [32, 64, 96, 128] ← 메모리 최적화
- `feat_dim`: [128, 256, 512] ← 표현력 최적화
- `gamma`: [0.1, 0.3, 0.5] ← LR 스케줄링

**설정**:
- method: bayes
- count: 100
- 예상 조합: 수천 개 (Bayes가 선택)

**장점**: 체계적, 높은 성능 기대  
**단점**: 중간 시간 소요


### 전략 3: Phase 2 Sweep (고급 최적화)

**매개변수 (11개)**:

Phase 1 최적값 + 추가 6개
- `warmup_method`: [linear, cosine]
- `num_instances`: [2, 4, 8]
- `prob`: [0.3, 0.5, 0.7]
- `re_prob`: [0.3, 0.5, 0.7]
- `with_center_loss`: [true, false]
- `with_flip_feature`: [true, false]

**설정**:
- method: bayes
- count: 80
- Phase 1 결과 기반 범위 조정 필요

**장점**: 최고 성능 추구  
**단점**: Phase 1 선행 필요


### 전략 4: Aggressive Sweep (공격적 탐색)

**매개변수 (12개)**:

모든 매개변수 동시 탐색 (넓은 범위)

**설정**:
- method: bayes
- count: 200
- 예상 조합: 수만 개

**장점**: 예상치 못한 최적 조합 발견 가능  
**단점**: 오래 걸림, 리소스 집약적


## 💻 7. sweep.py 코드 수정 사항

### 수정 위치 및 내용

#### 📌 Line 151-165: 추가 매개변수 읽기
- YAML 파일에서 새 매개변수 추출
- None 체크 및 타입 변환

#### 📌 Line 173-202: Sweep Config 구성
- 매개변수가 있을 때만 추가
- 동적으로 sweep_config 생성

#### 📌 Line 190-198: WandB Config 가져오기
- wandb.config.get()로 각 값 추출
- None 처리 포함

#### 📌 Line 217-223: Run Name 구성
- batch_size, feat_dim, gamma를 이름에 포함
- 예: `lr_0.003_wd_0.001_bs_64_fd_256`

#### 📌 Line 239-257: Training Command 전달
- Hydra 경로로 각 매개변수 전달
- `dataset.*`, `model.*`, `train.optim.*` 형식

#### 📌 Line 343-361: Total Grid 계산
- 추가 매개변수 포함한 조합 수 계산
- count 자동 결정에 사용


## 🎯 8. 매개변수 최적화 전체 목록

### 기존 5개 (Optimizer)

| 매개변수              | 기존 범위         | 개선 범위 (Phase 1) |
| --------------------- | ----------------- | ------------------- |
| `lr`                  | [1e-4 ~ 1e-2]     | [5e-4 ~ 5e-3] ✅     |
| `weight_decay`        | [1e-5 ~ 1e-3]     | [1e-5 ~ 2e-3] ✅     |
| `warmup_factor`       | [0.01, 0.05, 0.1] | [0.05 ~ 0.12] ✅     |
| `warmup_iters`        | [0, 10, 20]       | [0, 5, 10, 15, 20]  |
| `triplet_loss_margin` | [0.2, 0.3, 0.4]   | [0.25 ~ 0.4] ✅      |

### 추가 3개 (Phase 1)

| 매개변수           | 범위              | 영향             |
| ------------------ | ----------------- | ---------------- |
| `batch_size` (NEW) | [32, 64, 96, 128] | 메모리/성능 균형 |
| `feat_dim` (NEW)   | [128, 256, 512]   | 특징 표현력      |
| `gamma` (NEW)      | [0.1, 0.3, 0.5]   | LR 감소 정도     |

### 추가 6개 (Phase 2)

| 매개변수              | 범위             | 영향               |
| --------------------- | ---------------- | ------------------ |
| `warmup_method` (NEW) | [linear, cosine] | Warmup 스케줄      |
| `num_instances` (NEW) | [2, 4, 8]        | Triplet sampling   |
| `prob` (NEW)          | [0.3, 0.5, 0.7]  | Augmentation       |
| `re_prob` (NEW)       | [0.3, 0.5, 0.7]  | Random erasing     |
| `with_center_loss`    | [true, false]    | Center loss 활성화 |
| `with_flip_feature`   | [true, false]    | Flip feature       |


## 🔑 9. 핵심 개선 사항

### 방법론 변경
- **random → bayes** ✅
  - 이전 실험 결과 학습
  - 효율적인 탐색 공간 탐색

### 매개변수 범위 최적화
- **저성능 값 제거** ✅
  - lr=0.0001 제거 (mAP 0.07)
  - warmup_iters=20 축소
  
- **고성능 범위 집중** ✅
  - lr: 0.001~0.003 중심
  - weight_decay: 극단값 강조

### 확장 가능성
- **단계적 매개변수 추가** ✅
  - Phase 1 → Phase 2 → ...
  - 점진적 복잡도 증가


## 📈 10. 예상 성능 로드맵

```
현재 (c4s4yfvh) → Phase 1      → Phase 2      → 최종
─────────────────────────────────────────────────────
mAP: 0.6954     → mAP: 0.70+   → mAP: 0.75+   → mAP: 0.80+
34개 실험        100개 실험      80개 실험      최적화 완료
5개 매개변수     8개 매개변수    11개 매개변수      
random method   bayes method   bayes method      
```


## ✅ 11. 다음 액션 아이템

- [ ] 1. Phase 1 Sweep 실행
- [ ] 2. 100개 실험 완료 대기 (~하루)
- [ ] 3. Phase 1 결과 분석
- [ ] 4. Phase 2 YAML 파일 최적값으로 수정
- [ ] 5. Phase 2 Sweep 실행
- [ ] 6. 최종 최적 매개변수 확정


## 📌 핵심 요약

- **현재 최고**: mAP 0.6954
- **목표**: mAP 0.75+
- **방법**: 단계적 확장 (Phase 1 → Phase 2)
- **주요 개선**: 저성능 값 제거 + 신규 매개변수 추가


## 📚 참고 파일

### Sweep 설정 파일

1. **`reid_market1501_resnet_improved_sweep.yaml`** ⚡
   - 현재 분석 결과 직접 반영
   - 저성능 값 제거
   - 빠르고 안전한 개선

2. **`reid_market1501_resnet_phase1_sweep.yaml`** ⭐ **추천**
   - 8개 매개변수 (기존 5개 + 3개 추가)
   - batch_size, feat_dim, gamma 추가
   - 체계적 성능 향상

3. **`reid_market1501_resnet_phase2_sweep.yaml`** 🔬
   - 11개 매개변수 (Phase 1 최적값 + 6개 추가)
   - warmup_method, num_instances, prob, re_prob, center_loss, flip_feature
   - Phase 1 완료 후 실행

4. **`reid_market1501_resnet_aggressive_sweep.yaml`** 💪
   - 12개 매개변수 (모든 것 동시 탐색)
   - 가장 넓은 범위
   - 최고 성능 추구

### 실행 코드

- **`scripts/sweep.py`** (수정됨)
  - 9개 추가 매개변수 지원
  - 동적 sweep_config 생성
  - Hydra 경로 매핑


## 🔧 Sweep.py 매개변수 매핑

| Sweep 매개변수        | Hydra 경로                        | 설명                       |
| --------------------- | --------------------------------- | -------------------------- |
| `lr`                  | `train.optim.base_lr`             | Learning rate              |
| `weight_decay`        | `train.optim.weight_decay`        | Weight decay               |
| `warmup_factor`       | `train.optim.warmup_factor`       | Warmup factor              |
| `warmup_iters`        | `train.optim.warmup_iters`        | Warmup iterations          |
| `triplet_loss_margin` | `train.optim.triplet_loss_margin` | Triplet loss margin        |
| `batch_size`          | `dataset.batch_size`              | Batch size                 |
| `feat_dim`            | `model.feat_dim`                  | Feature dimension          |
| `gamma`               | `train.optim.gamma`               | LR decay rate              |
| `warmup_method`       | `train.optim.warmup_method`       | Warmup method              |
| `num_instances`       | `dataset.num_instances`           | Triplet sampling           |
| `prob`                | `dataset.prob`                    | Augmentation probability   |
| `re_prob`             | `dataset.re_prob`                 | Random erasing probability |
| `with_center_loss`    | `model.with_center_loss`          | Center loss flag           |
| `with_flip_feature`   | `model.with_flip_feature`         | Flip feature flag          |


## 💡 최종 추천

**초기 단계 + 고성능 목표**를 위해:

1. ✅ **Phase 1 Sweep 실행** (reid_market1501_resnet_phase1_sweep.yaml)
   - 8개 매개변수로 체계적 탐색
   - mAP 0.70+ 목표
   
2. ✅ **Phase 1 결과 분석** 후 최적값 확인

3. ✅ **Phase 2 Sweep 실행** (최적값으로 수정 후)
   - 11개 매개변수로 정밀 최적화
   - mAP 0.75+ 목표


## 📞 문의 및 수정

- Phase 2 실행 전에 Phase 1 최적값으로 `phase2_sweep.yaml` 수정 필요
- 추가 매개변수 필요 시 `sweep.py` 코드 확장 가능
- 특정 전략 조정 필요 시 해당 YAML 파일 수정


*생성일: 2025-10-01*  
*버전: v1.0*

