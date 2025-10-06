
# Phase 4 전략 최종 요약

**작성일**: 2025-10-06  
**긴급도**: ⭐⭐⭐ 높음  
**이유**: 논문 설정과 심각한 차이 발견

---

## 🚨 중대한 발견!

### 현재 성능이 논문보다 15% 낮은 이유

**논문 성능**: mAP **85.9%** (Re-ranking: 94.2%)  
**Phase 3 성능**: mAP **70.2%**  
**차이**: **-15.7%**

---

## ⚠️ 핵심 문제 (4가지)

### 1. Learning Rate 6배 높음! ⭐⭐⭐

```
논문: 0.00035
현재: 0.002
→ 6배 차이!
```

**영향**: 과도한 학습률로 수렴 불안정

---

### 2. Batch Size 절반! ⭐⭐

```
논문: 64 (P=16, K=4)
현재: 32 (P=8, K=2 추정)
→ 절반!
```

**영향**: Triplet loss의 hard sample mining 부족

---

### 3. num_instances 절반! ⭐⭐

```
논문: K=4
현재: K=2
→ 절반!
```

**영향**: Hard positive pair 부족

---

### 4. gamma 5배 높음!

```
논문: 0.1 (LR을 1/10로 감소)
현재: 0.5 (LR을 1/2로 감소)
→ 5배 차이!
```

**영향**: LR 감소가 너무 완만함

---

## 🎯 Phase 4 전략

### Phase 4A: 논문 설정 회귀 ⭐⭐⭐

**파일**: `reid_market1501_resnet_phase4_paper_aligned_sweep.yaml`

**핵심 변경**:
- lr: 0.002 → **0.00035** (1/6로 감소!)
- batch_size: 32 → **64** (2배 증가!)
- num_instances: 2 → **4** (2배 증가!)
- gamma: 0.5 → **0.1** (1/5로 감소!)
- warmup_iters: 5 → **10** (2배 증가!)

**예상 결과**:
- mAP: **80-85%** (현재 70%에서 15% 향상!)
- 논문 수준 도달

---

## 🚀 실행 방법

```bash
cd /home/jongphago/projects/tao_pytorch_backend

# tmux 세션
tmux new -s phase4_sweep
./scripts/background/run_reid_market1501_resnet_phase4_paper_aligned_sweep.sh

# 또는 백그라운드
nohup ./scripts/background/run_reid_market1501_resnet_phase4_paper_aligned_sweep.sh \
  > logs/phase4_paper_aligned_$(date +%Y%m%d_%H%M%S).log 2>&1 &
```

---

## 📊 논문 설정 요약

| 매개변수          | 논문 값 | 현재 Phase 3 | 수정 필요  |
| ----------------- | ------- | ------------ | ---------- |
| lr                | 0.00035 | 0.002        | ❌ 6배 높음 |
| batch_size        | 64      | 32           | ❌ 절반     |
| P (persons)       | 16      | 8            | ❌ 절반     |
| K (images/person) | 4       | 2            | ❌ 절반     |
| gamma             | 0.1     | 0.5          | ❌ 5배 높음 |
| warmup_iters      | 10      | 5            | ❌ 절반     |
| warmup_factor     | 0.01    | 0.05         | 약간 다름  |
| triplet_margin    | 0.3     | 0.35         | 약간 다름  |
| feat_dim          | 256     | 512          | 확인 필요  |
| last_stride       | 1       | 1            | ✅ 동일     |
| BNNeck            | 사용    | 사용         | ✅ 동일     |
| label_smooth      | 0.1     | True         | ✅ 동일     |
| RE probability    | 0.5     | 0.5          | ✅ 동일     |

---

## 💡 최종 권장

**Phase 4A를 즉시 실행하세요!** ⭐⭐⭐

현재 설정으로는 논문 성능(85.9%)에 절대 도달할 수 없습니다.

---

**긴급도**: 높음  
**예상 향상**: +15% (70% → 85%)

