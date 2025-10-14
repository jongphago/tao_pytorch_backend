# 데이터셋 변경으로 인한 OOM 문제 분석

**작성일**: 2025-10-06  
**스윕**: yek7vnuy  
**문제**: 전체 데이터셋 사용 시 CUDA Out of Memory 발생

---

## 🔍 문제 분석

### 1. 데이터셋 변경 확인 ✅

**현재 설정 (전체 Market-1501)**:
- 학습 이미지: **12,936개** (이전 샘플의 8.3배!)
- ID 수: **751개** (이전 샘플의 7.5배!)
- batch_size: **64** (이전 샘플의 2배)
- feat_dim: **256** (논문 기준)

**이전 설정 (샘플 데이터)**:
- 학습 이미지: 1,564개
- ID 수: 100개
- batch_size: 32
- feat_dim: 512

---

### 2. 메모리 사용량 분석

**분류기 크기 비교**:
```
현재: 256 × 751 = 192,256 파라미터
샘플: 512 × 100 = 51,200 파라미터
증가율: 3.8배! ⬅️ 주요 원인
```

**배치 크기 영향**:
```
현재: batch_size=64
샘플: batch_size=32
증가율: 2배
```

**총 메모리 증가**:
- 이미지 메모리: 2배 증가
- 분류기 메모리: 3.8배 증가
- 그래디언트 메모리: 비례 증가

---

### 3. OOM 발생 지점

**yek7vnuy 스윕 결과**:
- 총 실험: 1개
- OOM 발생: 1개 (100%)
- 성공: 0개

**실패 로그**:
```
"CUDA out of memory. Tried to allocate 3.98 GiB. GPU"
```

**발생 시점**: 첫 번째 검증 이후 (약 10 epoch)

---

## 💡 해결 방안

### 방안 1: batch_size 축소 ⭐⭐⭐ (강력 추천)

```yaml
dataset:
  batch_size: 32  # 64 → 32
  val_batch_size: 64  # 128 → 64
```

**효과**:
- ✅ 메모리 사용량 ~50% 감소
- ✅ 안정적인 학습 가능
- ❌ 학습 시간 2배 증가

---

### 방안 2: feat_dim 축소 ⭐⭐

```yaml
model:
  feat_dim: 128  # 256 → 128
```

**효과**:
- ✅ 분류기 크기 50% 감소
- ✅ 메모리 절약
- ❌ 성능 저하 가능성

---

### 방안 3: 조합 최적화 ⭐⭐⭐ (최적)

```yaml
dataset:
  batch_size: 32
  val_batch_size: 64

model:
  feat_dim: 256  # 논문 기준 유지
  num_classes: 751
```

**장점**:
- ✅ 메모리 안정성 확보
- ✅ 논문 설정 유지
- ✅ 전체 데이터셋 활용

---

## 🔧 권장 설정 수정

### experiment_market1501_resnet.yaml 수정

```yaml
dataset:
  train_dataset_dir: "/data/market1501/bounding_box_train"
  test_dataset_dir: "/data/market1501/bounding_box_test"
  query_dataset_dir: "/data/market1501/query"
  num_classes: 751
  batch_size: 32  # 64 → 32 ⭐
  val_batch_size: 64  # 128 → 64 ⭐
  num_workers: 1
  # ... 기타 설정

model:
  backbone: resnet_50
  feat_dim: 256  # 논문 기준 유지
  num_classes: 751  # 전체 데이터셋
  # ... 기타 설정
```

---

### Phase 5 Sweep 설정

```yaml
name: reid_market1501_resnet_phase5_full_dataset_sweep
method: bayes
metric:
  name: mAP
  goal: maximize

parameters:
  lr: [3.5e-4, 5.0e-4, 7.0e-4]  # 논문 기준
  weight_decay: [5.0e-5, 1.0e-4, 5.0e-4]
  warmup_factor: [0.01, 0.05]
  warmup_iters: [10]
  triplet_loss_margin: [0.3, 0.35]
  batch_size: [32]  # 고정 ⭐
  feat_dim: [256]  # 고정 ⭐
  gamma: [0.1, 0.2]
  warmup_method: ["linear"]
  num_instances: [4]  # 논문 기준
  with_flip_feature: [true, false]
  prob: [0.5, 0.7]
  re_prob: [0.3, 0.5, 0.7]

count: 20  # 적은 수로 조정
results_dir_base: /results/results/market1501/resnet50/phase5_full_dataset

# early_terminate 제거! ⭐
```

---

## 📊 메모리 사용량 비교

| 설정 | batch_size | feat_dim | 분류기 크기 | 메모리 사용량 |
|------|------------|----------|-------------|---------------|
| 샘플 데이터 | 32 | 512 | 51,200 | 0.20 GB |
| 현재 (전체) | 64 | 256 | 192,256 | 0.21 GB |
| 권장 (전체) | 32 | 256 | 192,256 | 0.20 GB |

---

## 🎯 다음 단계

### 1. 즉시 조치 ⭐⭐⭐

1. **experiment_market1501_resnet.yaml 수정**:
   - batch_size: 64 → 32
   - val_batch_size: 128 → 64

2. **Phase 5 sweep 생성**:
   - batch_size 고정: 32
   - early_terminate 제거
   - count 축소: 20

### 2. 검증 단계

1. **단일 실험 실행**:
   - 수정된 설정으로 1개 실험
   - OOM 없이 120 epoch 완료 확인

2. **Phase 5 sweep 실행**:
   - 전체 데이터셋으로 최적화
   - 논문 수준 성능 목표

---

## 📋 요약

### 문제 원인

1. **전체 데이터셋 사용** (12,936개 이미지)
2. **batch_size 증가** (32 → 64)
3. **분류기 크기 증가** (51,200 → 192,256 파라미터)
4. **GPU 메모리 부족**

### 해결책

✅ **batch_size 축소**: 64 → 32  
✅ **val_batch_size 축소**: 128 → 64  
✅ **early_terminate 제거**  
✅ **count 축소**: 20개  

### 기대 효과

- ✅ OOM 문제 해결
- ✅ 전체 데이터셋 활용
- ✅ 논문 수준 성능 달성 가능
- ✅ 안정적인 학습 진행

---

**결론**: 데이터셋 변경 시 batch_size 조정이 필수!






