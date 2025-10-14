# Sweep 조기 종료 원인 분석

**작성일**: 2025-10-06  
**스윕**: nyork0eg, ck4jzokv 등  
**문제**: 120 에포크까지 가지 않고 조기 종료

---

## 🔍 원인 분석

### 1. W&B Hyperband Early Termination ⭐⭐⭐

**모든 sweep 설정에 포함된 설정**:

```yaml
early_terminate:
  type: hyperband
  max_iter: 12
  s: 2
  eta: 3
  min_iter: 5
```

### Hyperband 동작 방식

**max_iter: 12** 의미:
- 각 실험이 실행할 수 있는 **최대 resource**
- Resource = **validation 횟수**
- validation_interval=10이면: 10, 20, 30, ..., 120 epoch에서 validation

**계산**:
```
max_iter: 12
validation_interval: 10
→ 최대: 12 × 10 = 120 epoch까지 가능
```

하지만 **Hyperband는 성능이 낮은 실험을 조기 종료**합니다!

---

### Hyperband 알고리즘

**조기 종료 조건**:
1. **eta=3**: 상위 1/3만 다음 단계로 진행
2. **s=2**: 2번의 halving 수행
3. **min_iter=5**: 최소 5번의 validation은 보장

**예시**:
```
40개 실험 시작
  ↓ min_iter=5 (50 epoch까지 모두 실행)
  ↓ 성능 평가
  
상위 1/3 (약 13개) 계속
  ↓ 다음 단계 진행
  
상위 1/3 (약 4개) 계속  
  ↓ max_iter=12 (120 epoch까지)
  
최종 상위 실험만 120 epoch 완료
```

---

### 2. CUDA Out of Memory (일부 실험)

**nyork0eg 스윕**:
- **실패**: 2개 (CUDA OOM)
- 원인: `batch_size=64` + `feat_dim=256` 조합
- GPU 메모리 부족

**ck4jzokv 스윕**:
- 대부분 정상 진행 (batch_size에 따라 다름)

---

## 📊 Early Termination 영향

### ck4jzokv 스윕 분석

- 모든 실험: **정확히 12번의 evaluation**
- 즉: 12 × 10 = **120 epoch 완료** 또는 조기 종료

**실험 종류**:
1. **120 epoch 완료**: 성능 좋은 실험 (상위 25-33%)
2. **50-100 epoch에서 종료**: 성능 낮은 실험 (Hyperband가 조기 종료)

---

## 🔍 1647 step의 의미

**추정**:
```
batch_size=64, 1564개 이미지
→ Epoch당 step: 1564 / 64 ≈ 24.4 steps
→ 1647 steps / 24.4 ≈ 67.5 epochs

또는

batch_size=96
→ Epoch당 step: 1564 / 96 ≈ 16.3 steps
→ 1647 steps / 16.3 ≈ 101 epochs
```

**결론**: Hyperband가 **70-100 epoch에서 조기 종료**시킨 것!

---

## 💡 해결 방법

### 방법 1: early_terminate 제거 ⭐⭐⭐ (강력 추천)

```yaml
# early_terminate 섹션 전체 제거 또는 주석

# early_terminate:
#   type: hyperband
#   max_iter: 12
#   s: 2
#   eta: 3
#   min_iter: 5
```

**효과**:
- 모든 실험이 **120 epoch 완료**
- 정확한 성능 평가 가능

**단점**:
- 실험 시간 증가 (저성능 실험도 120 epoch까지 실행)

---

### 방법 2: max_iter 증가

```yaml
early_terminate:
  type: hyperband
  max_iter: 120  # 12 → 120 (10배 증가!)
  s: 2
  eta: 3
  min_iter: 12  # 5 → 12
```

**효과**:
- 더 많은 epoch 허용
- 여전히 조기 종료 이점 유지

---

### 방법 3: early_terminate 비활성화하고 count 축소

```yaml
# early_terminate 제거

count: 10  # 40 → 10
```

**효과**:
- 소수 실험만 실행
- 모두 120 epoch 완료
- 빠른 검증

---

## 📋 Sweep별 early_terminate 영향

| Sweep | max_iter | validation_interval | 최대 epoch | 조기 종료 |
|-------|----------|---------------------|-----------|----------|
| Phase 1-4 | 12 | 10 | 120 | ✅ 발생 |
| 논문 재현 | 제거 필요 | 10 | 120 | ❌ 없음 |

---

## 🎯 권장 조치

### Phase 5 sweep 설정 시

**early_terminate 완전 제거** ⭐⭐⭐

```yaml
name: reid_market1501_resnet_phase5_sweep
method: bayes
metric:
  name: mAP
  goal: maximize

parameters:
  # ... (매개변수 설정)

count: 20  # 적은 수로 조정
results_dir_base: /results/results/market1501/resnet50/phase5

# early_terminate 섹션 제거! ⭐
```

**이유**:
1. 모든 실험 120 epoch 완료
2. 정확한 최종 성능 비교 가능
3. count를 줄여서 시간 조절

---

## 📊 요약

### 조기 종료 원인

1. **W&B Hyperband** ⭐⭐⭐ (주요 원인)
   - max_iter=12 설정
   - 성능 낮은 실험을 50-100 epoch에서 조기 종료

2. **CUDA OOM** (일부)
   - batch_size 64/96에서 발생
   - GPU 메모리 부족

### 해결책

✅ **early_terminate 제거**
✅ count 축소 (20-30개)
✅ batch_size 조정 (메모리 고려)

---

**결론**: early_terminate 때문에 조기 종료됨!

---

**권장**: Phase 5부터 early_terminate 제거하세요!






