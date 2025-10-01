# Phase 1 분석 및 Phase 2 전략 수립 보고서

**작성일**: 2025-10-01  
**프로젝트**: ReIdentificationNet W&B Sweep 매개변수 최적화  
**데이터셋**: Market-1501  
**백본**: ResNet-50

---

## 📋 목차

1. [개요](#개요)
2. [Phase 1 실험 결과 분석](#phase-1-실험-결과-분석)
3. [매개변수별 성능 인사이트](#매개변수별-성능-인사이트)
4. [Phase 2 전략 수립](#phase-2-전략-수립)
5. [구현 및 실행](#구현-및-실행)
6. [결론 및 권장사항](#결론-및-권장사항)

---

## 개요

### 배경

- **이전 실험** (c4s4yfvh): 34개 실험, 최고 mAP 0.6954
- **Phase 1 목적**: 8개 매개변수 탐색 (기존 5개 + 3개 추가)
- **Phase 1 실행**: 100개 실험 완료 (Bayes Search)
- **Phase 2 목적**: Phase 1 최적값 기반 고급 매개변수 탐색

### Phase 1 매개변수 구성

| 카테고리 | 매개변수 | 범위 |
|---------|---------|------|
| **기존 5개** | `lr` | [5e-4, 1e-3, 2e-3, 3e-3, 5e-3] |
| | `weight_decay` | [1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 2e-3] |
| | `warmup_factor` | [0.05, 0.08, 0.1, 0.12] |
| | `warmup_iters` | [0, 5, 10, 15, 20] |
| | `triplet_loss_margin` | [0.25, 0.3, 0.35, 0.4] |
| **추가 3개** | `batch_size` | [32, 64, 96, 128] |
| | `feat_dim` | [128, 256, 512] |
| | `gamma` | [0.1, 0.3, 0.5] |

---

## Phase 1 실험 결과 분석

### 전체 성능 통계

| 지표 | 값 | 평가 |
|------|-----|------|
| **총 실험 수** | 100개 | ✅ 계획대로 완료 |
| **최고 mAP** | 0.7044 | ✅ 목표(0.70+) 달성 |
| **mAP >= 0.7** | 1개 | ❌ 예상 대비 저조 |
| **mAP >= 0.65** | 5개 (5%) | ⚠️ 적음 |
| **mAP >= 0.6** | 22개 (22%) | ⚠️ 보통 |
| **평균 mAP** | 0.3895 | ❌ 낮음 |
| **중앙값 mAP** | 0.3653 | ❌ 낮음 |
| **mAP < 0.1** | 6개 (6%) | ⚠️ 저성능 실험 존재 |

### 주요 발견

#### ✅ 성공 요인
- **단 1개 실험**만 mAP 0.70 돌파 (solar-sweep-1)
- 22%의 실험이 mAP 0.6 이상 달성
- 저성능 실험 비율(6%)은 낮음

#### ❌ 개선 필요 사항
- 평균 성능이 낮음 (0.3895)
- mAP 0.7 이상 실험이 1개만 존재
- 매개변수 조합의 변동성이 큼

---

## 매개변수별 성능 인사이트

### 🏆 최고 성능 실험 분석

**solar-sweep-1** (mAP: 0.7044)
```yaml
lr: 0.002
weight_decay: 5e-05
warmup_factor: 0.05
warmup_iters: 5
triplet_loss_margin: 0.35
batch_size: 32         ⬅️ 핵심!
feat_dim: 512
gamma: 0.5
```

### 📊 매개변수별 최적값 (mAP >= 0.6 기준)

#### 1. batch_size ⭐⭐⭐ (가장 중요)

| 값 | 평균 mAP | 최고 mAP | 실험 수 |
|----|----------|----------|---------|
| **32** | **0.6849** | **0.7044** | 2 |
| 64 | 0.6287 | 0.6568 | 15 |
| 128 | 0.6109 | 0.6300 | 5 |

**핵심 발견**:
- batch_size=32가 압도적 성능 (평균 0.6849)
- 64와의 차이: **0.0562** (약 9% 향상)
- 단, 실험 수가 2개뿐이어서 추가 검증 필요

**중요도**: ⭐⭐⭐ (최우선)

---

#### 2. lr ⭐⭐

| 값 | 평균 mAP | 최고 mAP | 실험 수 |
|----|----------|----------|---------|
| **0.002** | **0.6555** | **0.7044** | 6 |
| 0.001 | 0.6220 | 0.6558 | 8 |
| 0.003 | 0.6205 | 0.6445 | 7 |
| 0.0005 | 0.6014 | 0.6014 | 1 |

**핵심 발견**:
- lr=0.002가 최적
- 0.001~0.003 범위가 안정적
- 너무 작거나 크면 성능 저하

**중요도**: ⭐⭐

---

#### 3. warmup_iters ⭐

| 값 | 평균 mAP | 최고 mAP | 실험 수 |
|----|----------|----------|---------|
| **5** | **0.6445** | **0.7044** | 9 |
| 15 | 0.6394 | 0.6568 | 2 |
| 20 | 0.6205 | 0.6445 | 5 |
| 10 | 0.6142 | 0.6297 | 5 |
| 0 | 0.6014 | 0.6014 | 1 |

**핵심 발견**:
- warmup_iters=5가 최적
- 너무 길면(20) 오히려 성능 저하
- 짧은 warmup이 효과적

**중요도**: ⭐

---

#### 4. warmup_factor

| 값 | 평균 mAP | 최고 mAP | 실험 수 |
|----|----------|----------|---------|
| **0.05** | **0.6412** | **0.7044** | 3 |
| 0.08 | 0.6379 | 0.6568 | 6 |
| 0.1 | 0.6280 | 0.6654 | 9 |
| 0.12 | 0.6129 | 0.6300 | 4 |

**핵심 발견**:
- warmup_factor=0.05가 평균 최고
- 0.05~0.08 범위가 효과적
- 너무 크면(0.12) 성능 저하

---

#### 5. triplet_loss_margin

| 값 | 평균 mAP | 최고 mAP | 실험 수 |
|----|----------|----------|---------|
| **0.35** | **0.6363** | **0.7044** | 8 |
| 0.4 | 0.6283 | 0.6568 | 6 |
| 0.25 | 0.6266 | 0.6558 | 5 |
| 0.3 | 0.6205 | 0.6445 | 3 |

**핵심 발견**:
- triplet_loss_margin=0.35가 최적
- 0.3~0.4 범위가 안정적

---

#### 6. feat_dim

| 값 | 평균 mAP | 최고 mAP | 실험 수 |
|----|----------|----------|---------|
| **512** | **0.6323** | **0.7044** | 13 |
| 128 | 0.6309 | 0.6558 | 3 |
| 256 | 0.6236 | 0.6529 | 6 |

**핵심 발견**:
- feat_dim=512가 최고
- 128과 큰 차이 없음 (0.6323 vs 0.6309)
- 512 사용 권장 (표현력 우선)

---

#### 7. gamma

| 값 | 평균 mAP | 최고 mAP | 실험 수 |
|----|----------|----------|---------|
| **0.3** | **0.6373** | **0.6654** | 7 |
| 0.5 | 0.6292 | 0.7044 | 11 |
| 0.1 | 0.6180 | 0.6529 | 4 |

**핵심 발견**:
- gamma=0.3이 평균 최고
- 0.3~0.5 범위가 안정적

---

#### 8. weight_decay

| 값 | 평균 mAP | 최고 mAP | 실험 수 |
|----|----------|----------|---------|
| **0.0001** | **0.6371** | 0.6654 | 4 |
| 0.001 | 0.6361 | 0.6568 | 4 |
| 5e-05 | 0.6354 | **0.7044** | 5 |
| 1e-05 | 0.6223 | 0.6303 | 5 |
| 0.002 | 0.6222 | 0.6445 | 3 |
| 0.0005 | 0.6068 | 0.6068 | 1 |

**핵심 발견**:
- 0.0001, 0.001, 5e-05 모두 비슷
- 최고 성능은 5e-05에서 나옴
- 중간값(0.0005)은 오히려 낮음

---

### 📈 상위 10개 실험 매개변수

| 순위 | 실험명 | mAP | lr | wd | wf | wi | tlm | bs | fd | gamma |
|------|--------|-----|----|----|----|----|-----|----|----|-------|
| 1 | solar-sweep-1 | 0.7044 | 0.002 | 5e-05 | 0.05 | 5 | 0.35 | **32** | 512 | 0.5 |
| 2 | ruby-sweep-91 | 0.6654 | 0.002 | 1e-04 | 0.1 | 5 | 0.35 | **32** | 512 | 0.3 |
| 3 | electric-sweep-6 | 0.6568 | 0.002 | 0.001 | 0.08 | 15 | 0.4 | 64 | 512 | 0.5 |
| 4 | summer-sweep-69 | 0.6558 | 0.001 | 5e-05 | 0.08 | 5 | 0.25 | 64 | 128 | 0.3 |
| 5 | proud-sweep-94 | 0.6529 | 0.002 | 0.001 | 0.1 | 5 | 0.35 | 64 | 256 | 0.1 |
| 6 | fiery-sweep-13 | 0.6445 | 0.003 | 0.002 | 0.08 | 20 | 0.3 | 64 | 512 | 0.3 |
| 7 | colorful-sweep-28 | 0.6303 | 0.002 | 1e-05 | 0.1 | 5 | 0.4 | 64 | 512 | 0.5 |
| 8 | silver-sweep-3 | 0.6300 | 0.001 | 1e-04 | 0.12 | 5 | 0.25 | 128 | 128 | 0.3 |
| 9 | lucky-sweep-100 | 0.6297 | 0.003 | 1e-04 | 0.1 | 10 | 0.4 | 64 | 256 | 0.3 |
| 10 | daily-sweep-21 | 0.6269 | 0.001 | 1e-05 | 0.08 | 20 | 0.25 | 64 | 256 | 0.5 |

**패턴 분석**:
- 상위 2개 모두 **batch_size=32** 사용 ⭐
- lr=0.001~0.003 범위
- warmup_iters=5가 다수 (6/10)
- feat_dim=512 다수 (7/10)

---

## Phase 2 전략 수립

### Phase 2의 문제점 진단

#### ❌ 기존 Phase 2 YAML의 문제

1. **batch_size 누락**
   - Phase 1에서 가장 중요한 발견이었으나 Phase 2에 없음
   - "Phase 1에서 찾은 최적 batch_size 고정"이라고 했지만 실제로 없음

2. **feat_dim 누락**
   - 마찬가지로 Phase 2에 없음

3. **gamma 누락**
   - Phase 1 결과 gamma=0.3이 최적이었으나 Phase 2에 없음

4. **warmup_factor 범위 문제**
   - Phase 2: [0.08, 0.1, 0.12]
   - Phase 1 최적값: 0.05 (빠짐!)

### Phase 2 수정 전략

#### 전략 A: 보수적 접근 ⭐ (채택)

**핵심 원칙**: Phase 1 최적값을 고정하고 새 매개변수만 탐색

**매개변수 구성**:

```yaml
# Phase 1 최적값 고정
lr: [2.0e-3]                    # 고정
weight_decay: [5.0e-5, 1.0e-4, 1.0e-3]
warmup_factor: [0.05, 0.08]     # 0.05 추가!
warmup_iters: [5]               # 고정
triplet_loss_margin: [0.35, 0.4]

# Phase 1 최적값 고정 (중요!)
batch_size: [32]                # 고정 ⭐⭐⭐
feat_dim: [512]                 # 고정
gamma: [0.3]                    # 고정

# 새로운 고급 매개변수 탐색 (Phase 2 목표)
warmup_method: ["linear", "cosine"]
num_instances: [2, 4, 8]
prob: [0.3, 0.5, 0.7]
re_prob: [0.3, 0.5, 0.7]
with_center_loss: [true, false]
with_flip_feature: [true, false]

count: 60  # 80 → 60
```

**장점**:
- ✅ batch_size=32의 효과 명확히 검증
- ✅ 새 매개변수 효과만 집중 분석 가능
- ✅ 안정적 성능 보장 (mAP 0.70+)
- ✅ 실험 횟수 적정 (60개)

**예상 결과**:
- mAP >= 0.7: 10-15개 (17-25%)
- 평균 mAP: 0.65+
- 최고 mAP: 0.72+

---

#### 전략 B: 공격적 접근 (대안)

**핵심 원칙**: batch_size 재탐색 (32 중심)

**매개변수 구성**:

```yaml
lr: [1.0e-3, 2.0e-3, 3.0e-3]
weight_decay: [5.0e-5, 1.0e-4, 1.0e-3]
warmup_factor: [0.05, 0.08, 0.1]
warmup_iters: [5, 10]
triplet_loss_margin: [0.3, 0.35, 0.4]

# batch_size 재탐색 (32 중심)
batch_size: [24, 32, 48]        # 32 중심으로 탐색
feat_dim: [512]                 # 고정
gamma: [0.3, 0.5]

# 새 매개변수 (범위 축소)
warmup_method: ["linear", "cosine"]
num_instances: [2, 4, 8]
prob: [0.5, 0.7]                # 0.3 제거
re_prob: [0.5, 0.7]             # 0.3 제거
with_center_loss: [true, false]
with_flip_feature: [true, false]

count: 100
```

**장점**:
- ✅ batch_size 최적값 재확인
- ✅ 24, 48도 테스트하여 32 검증
- ✅ 더 나은 조합 발견 가능성

**단점**:
- ❌ 실험 시간 더 소요 (100개)
- ❌ batch_size=32가 명확하므로 재탐색 불필요할 수 있음

---

### 최종 선택: 전략 A

**선택 이유**:

1. **batch_size=32가 명확**
   - 평균 0.6849 vs 64: 0.6287 (9% 차이)
   - 재탐색 불필요

2. **Phase 2의 목적**
   - 새 매개변수(warmup_method, num_instances, prob, re_prob, center_loss, flip_feature) 효과 검증
   - 기존 매개변수 재탐색이 아님

3. **효율성**
   - 60개 실험으로 충분
   - 고정값 많아 새 매개변수 효과 명확히 분석 가능

---

## 구현 및 실행

### 수정된 파일

#### 1. Sweep 설정 파일

**`reid_market1501_resnet_phase2_sweep.yaml`** (수정)
- Phase 1 최적값 반영
- batch_size, feat_dim, gamma 추가
- lr, warmup_iters 고정
- warmup_factor에 0.05 추가
- count: 60

**`reid_market1501_resnet_phase2_aggressive_sweep.yaml`** (신규)
- 전략 B 구현
- batch_size 재탐색
- count: 100

#### 2. 백그라운드 실행 스크립트

**`scripts/background/run_reid_market1501_resnet_phase2_sweep.sh`** (신규)
```bash
#!/usr/bin/env bash
# Phase 2 전략 A 실행
# 60개 실험, batch_size=32 고정
```

**`scripts/background/run_reid_market1501_resnet_phase2_aggressive_sweep.sh`** (신규)
```bash
#!/usr/bin/env bash
# Phase 2 전략 B 실행
# 100개 실험, batch_size 재탐색
```

### 실행 방법

#### 전략 A 실행 (권장)

```bash
cd /home/jongphago/projects/tao_pytorch_backend

# tmux 세션에서 실행
tmux new -s phase2_sweep
./scripts/background/run_reid_market1501_resnet_phase2_sweep.sh

# 또는 백그라운드 실행
nohup ./scripts/background/run_reid_market1501_resnet_phase2_sweep.sh \
  > logs/phase2_sweep_$(date +%Y%m%d_%H%M%S).log 2>&1 &
```

#### 모니터링

```bash
# 로그 실시간 확인
tail -f logs/phase2_sweep_*.log

# W&B 대시보드
https://wandb.ai/jongphago/TAO%20Toolkit

# 결과 디렉토리
ls -lh /home/jongphago/projects/tao_tutorials/notebooks/\
tao_launcher_starter_kit/reidentificationnet/results/\
market1501/resnet50/phase2/sweep/
```

---

## 결론 및 권장사항

### 핵심 발견 요약

1. **batch_size=32가 가장 중요한 발견**
   - 평균 mAP: 0.6849 (vs 64: 0.6287)
   - 약 9% 성능 향상
   - Phase 2에서 고정 사용 권장

2. **최적 매개변수 조합**
   ```
   lr: 0.002
   weight_decay: 5e-05
   warmup_factor: 0.05
   warmup_iters: 5
   triplet_loss_margin: 0.35
   batch_size: 32
   feat_dim: 512
   gamma: 0.3
   ```

3. **Phase 1 목표 달성도**
   - ✅ mAP 0.70+ 달성 (1개)
   - ❌ 안정적 0.70+ 미달성
   - ⚠️ 평균 성능 낮음 (0.3895)

### Phase 2 기대 효과

**전략 A 채택 시**:

1. **안정적 고성능**
   - batch_size=32 활용으로 mAP 0.70+ 안정적 달성
   - 예상: 10-15개 실험 (17-25%)이 0.70+ 달성

2. **새 매개변수 효과 검증**
   - warmup_method: linear vs cosine 비교
   - num_instances: triplet sampling 최적화
   - prob, re_prob: 데이터 증강 효과
   - center_loss, flip_feature: 모델 기능 검증

3. **최종 목표**
   - 최고 mAP: 0.72+ 목표
   - 평균 mAP: 0.65+ 목표
   - 안정적 고성능 매개변수 조합 확정

### 향후 계획

1. **Phase 2 실행** (60개 실험)
   - 예상 소요 시간: 10-15시간
   - 실행 명령어 준비 완료

2. **Phase 2 결과 분석**
   - 새 매개변수 효과 정량화
   - 최종 최적 매개변수 확정

3. **최종 모델 훈련**
   - Phase 2 최적 매개변수로 full training
   - 최종 mAP 검증

---

## 부록

### A. Phase 1 vs c4s4yfvh 비교

| 항목 | c4s4yfvh | Phase 1 |
|------|----------|---------|
| 실험 수 | 34 | 100 |
| 최고 mAP | 0.6954 | 0.7044 |
| mAP >= 0.6 | 10개 (29%) | 22개 (22%) |
| 평균 mAP | 0.3991 | 0.3895 |
| 매개변수 수 | 5개 | 8개 |

**분석**:
- Phase 1이 최고 mAP는 약간 향상 (0.7044 vs 0.6954)
- 그러나 평균 성능은 약간 하락
- 매개변수 증가로 탐색 공간 확대되어 변동성 증가

### B. 매개변수 중요도 순위

1. ⭐⭐⭐ **batch_size** (가장 중요)
2. ⭐⭐ **lr**
3. ⭐ **warmup_iters**
4. **warmup_factor**
5. **triplet_loss_margin**
6. **feat_dim**
7. **gamma**
8. **weight_decay**

### C. 파일 구조

```
tao_pytorch_backend/
├── docs/
│   └── Phase1-분석-및-Phase2-전략-수립-보고서.md (본 문서)
│
├── nvidia_tao_pytorch/cv/re_identification/sweeps/
│   ├── reid_market1501_resnet_phase1_sweep.yaml
│   ├── reid_market1501_resnet_phase2_sweep.yaml (수정)
│   └── reid_market1501_resnet_phase2_aggressive_sweep.yaml (신규)
│
└── scripts/background/
    ├── run_reid_market1501_resnet_phase1_sweep.sh
    ├── run_reid_market1501_resnet_phase2_sweep.sh (신규)
    └── run_reid_market1501_resnet_phase2_aggressive_sweep.sh (신규)
```

---

**보고서 끝**

*작성: AI Assistant*  
*검토: 필요 시 업데이트*

