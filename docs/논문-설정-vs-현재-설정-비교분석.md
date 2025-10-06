# 논문 설정 vs 현재 설정 비교 분석 보고서

**논문**: Bag of Tricks and A Strong Baseline for Deep Person Re-identification (CVPR 2019)  
**작성일**: 2025-10-06  
**목적**: 성능 차이 원인 분석 및 Phase 4 전략 수립

---

## 🚨 핵심 문제 발견

### 성능 차이
- **논문 성능**: mAP **85.9%** (Re-ranking: 94.2%)
- **현재 Phase 3**: mAP **70.2%**
- **차이**: **-15.7%** (약 22% 낮음)

이는 **심각한 성능 저하**입니다!

---

## ⚠️ 설정 차이 분석

### 1. Learning Rate (가장 심각!) ⭐⭐⭐

| 항목 | 논문 | 현재 | 차이 |
|------|------|------|------|
| **초기 LR** | **0.00035** | **0.002** | **6배 높음!** ❌ |
| Warmup epochs | 10 | 5 | 절반 |
| Warmup 시작 LR | 0.000035 (0.1×base) | 0.0001 (0.05×base) | 다름 |

**문제**:
- 현재 lr=0.002는 **6배 높음**
- 과도한 학습률로 인한 수렴 불안정
- 최적점 주변에서 진동 가능성

**논문 인용**:
> "Adam method is adopted to optimize the model. The initial learning rate is set to be **0.00035**"

---

### 2. Batch Size & Triplet Sampling ⭐⭐

| 항목 | 논문 | 현재 | 차이 |
|------|------|------|------|
| **Total Batch** | **64** | **32** | **절반** ❌ |
| **P (persons)** | **16** | **8** (추정) | 절반 |
| **K (images/person)** | **4** | **2** | **절반** ❌ |

**문제**:
- Batch size 32는 **절반**
- num_instances=2는 **절반**
- Triplet loss의 hard sample mining 부족

**논문 인용**:
> "we randomly sample **P=16** identities and **K=4** images of per person"  
> "the batch size equals to P×K"  
> "In this paper, we set P=16 and K=4"

---

### 3. LR Schedule (Gamma) ⭐

| 항목 | 논문 | 현재 | 차이 |
|------|------|------|------|
| **gamma** | **0.1** | **0.5** | **5배 높음** ❌ |
| LR decay epochs | 40, 70 | 40, 70 | 동일 |

**문제**:
- gamma=0.5는 너무 완만함
- Epoch 40: LR이 0.001 → 0.0005 (논문은 0.000035)
- Epoch 70: LR이 0.0005 → 0.00025 (논문은 0.0000035)

**논문 인용**:
> "the learning rate is decreased by **0.1** at the 40th epoch and 70th epoch"

---

### 4. Triplet Loss Margin

| 항목 | 논문 | 현재 | 차이 |
|------|------|------|------|
| margin | **0.3** | **0.35** | 약간 높음 |

**논문 인용**:
> "The margin of triplet loss is set to be **0.3**"

---

## 📊 논문의 Ablation Study (Table 1)

### Trick별 성능 향상 (Market-1501)

| 모델 | Rank-1 | mAP | 향상 |
|------|--------|-----|------|
| Baseline-S | 87.7% | 74.0% | - |
| +Warmup | 88.7% | 75.2% | +1.2% |
| +REA | 91.3% | 79.3% | +4.1% ⭐ |
| +Label Smoothing | 91.4% | 80.3% | +1.0% |
| +Last Stride=1 | 92.0% | 81.7% | +1.4% |
| **+BNNeck** | **94.1%** | **85.7%** | **+4.0%** ⭐⭐⭐ |
| +Center Loss | 94.5% | 85.9% | +0.2% |

**핵심 발견**:
- **BNNeck**이 가장 큰 향상 (81.7% → 85.7%)
- **REA**가 두 번째 큰 향상 (75.2% → 79.3%)
- Center Loss는 미미한 향상 (0.2%)

---

## 🎯 Phase 4 전략: 논문 설정으로 회귀

### Phase 4A: 논문 설정 완전 복원 ⭐⭐⭐ (강력 추천)

```yaml
name: reid_market1501_resnet_phase4_paper_aligned_sweep
method: bayes
metric:
  name: mAP
  goal: maximize

parameters:
  # 논문 핵심 설정으로 회귀
  lr: [3.5e-4, 5.0e-4, 7.0e-4]  # 논문: 0.00035 중심
  weight_decay: [5.0e-4, 1.0e-3]  # 논문 범위
  warmup_factor: [0.01, 0.05]
  warmup_iters: [10]  # 논문: 10 epochs
  triplet_loss_margin: [0.3, 0.35]  # 논문: 0.3
  
  # Batch 설정 (중요!)
  batch_size: [64, 96]  # 논문: 64
  num_instances: [4]  # 논문: 4
  
  # 모델 설정
  feat_dim: [256, 512]  # 논문: 256
  gamma: [0.1, 0.2]  # 논문: 0.1
  
  # 검증된 설정
  warmup_method: ["linear"]
  prob: [0.5]
  re_prob: [0.5]
  with_flip_feature: [false]

count: 40
```

**예상 결과**:
- mAP: **80-85%** (논문 수준)
- Rank-1: 90-94%
- 논문 성능에 근접

---

### Phase 4B: 논문 정확값 검증

```yaml
name: reid_market1501_resnet_phase4_paper_exact_sweep
method: grid
parameters:
  # 논문 exact 설정
  lr: [3.5e-4]  # 논문 정확값
  weight_decay: [5.0e-4]  # 추정
  warmup_factor: [0.01]  # 계산: 0.00035 / 0.00035 × 0.1 = 0.01
  warmup_iters: [10]
  triplet_loss_margin: [0.3]
  batch_size: [64]  # P=16, K=4
  num_instances: [4]
  feat_dim: [256]  # 논문
  gamma: [0.1]  # 논문
  warmup_method: ["linear"]
  prob: [0.5]
  re_prob: [0.5]
  with_flip_feature: [false]

count: 1  # 정확히 논문 설정 재현
```

**목적**: 논문 설정 정확히 재현하여 베이스라인 확인

---

## 📈 예상 성능 향상 경로

```
현재 Phase 3: mAP 70.2%
   ↓ lr 수정 (0.002 → 0.00035)
Phase 4 예상: mAP 75-80%
   ↓ batch_size 증가 (32 → 64)
Phase 4 예상: mAP 80-83%
   ↓ num_instances 증가 (2 → 4)
Phase 4 예상: mAP 82-85%
   ↓ gamma 감소 (0.5 → 0.1)
Phase 4 최종: mAP 85% 목표 ⭐
```

---

## 🔍 왜 Phase 1-3에서 발견하지 못했나?

### 탐색 범위 문제

**Phase 1 설정**:
- lr: [5e-4, 1e-3, 2e-3, 3e-3, 5e-3]
- → **0.00035가 범위에 없었음!**
- → 가장 작은 값(5e-4)도 논문보다 43% 높음

**Phase 1 batch_size**:
- [32, 64, 96, 128]
- → batch_size=64는 있었지만 **lr이 너무 높아서** 효과 못 봄
- → batch_size=32가 최고였던 이유: **lr=0.002일 때 상대적으로 안정적**

---

## 💡 Phase 4 최종 제안

### 🎯 Phase 4A: 논문 설정 회귀 ⭐⭐⭐ (강력 추천)

**전략**: 논문 설정 중심으로 탐색

**핵심 변경**:
```yaml
# 가장 중요한 수정
lr: [3.5e-4, 5.0e-4, 7.0e-4]  # 현재 0.002에서 1/3~1/6로 감소!
batch_size: [64, 96]  # 32 → 64로 증가
num_instances: [4]  # 2 → 4로 증가
gamma: [0.1, 0.2]  # 0.5 → 0.1로 감소
warmup_iters: [10]  # 5 → 10으로 증가
```

**예상 결과**:
- mAP: **80-85%** (15% 향상!)
- 논문 수준 도달

**실험 수**: 40개  
**소요 시간**: 10-15시간  
**성공 확률**: ⭐⭐⭐ 매우 높음

---

### Phase 4B: 논문 정확 재현

**목적**: 논문 설정 100% 재현

**설정**:
```yaml
lr: [3.5e-4]
weight_decay: [5.0e-4]  # 추정
batch_size: [64]
num_instances: [4]
gamma: [0.1]
warmup_iters: [10]
warmup_factor: [0.01]
triplet_loss_margin: [0.3]
feat_dim: [256]
(모든 값 고정)
```

**실험 수**: 1개  
**목적**: 베이스라인 확인

---

## 🚀 즉시 실행 권장

**Phase 4A를 먼저 실행** 후 결과 확인하시길 강력히 추천합니다!

현재 설정으로는 논문 성능(85.9%)에 도달할 수 없습니다.
