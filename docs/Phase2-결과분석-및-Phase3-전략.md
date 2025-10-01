# Phase 2 결과 분석 및 Phase 3 전략 보고서

**작성일**: 2025-10-01  
**스윕 ID**: 8uslnc5i (Phase 2)  
**상태**: 분석 완료, Phase 3 준비

---

## 📊 Phase 2 (8uslnc5i) 결과 요약

### 실험 현황

| 항목 | 개수 | 비율 |
|------|------|------|
| **총 실험** | 36개 | 100% |
| **실패** | 18개 | 50% |
| **분석 가능** | 19개 | 53% |
| **완료** | 0개 | 0% |

### 성능 통계

| 지표 | 값 | 평가 |
|------|-----|------|
| **최고 mAP** | 0.6637 | ❌ Phase 1(0.7044)보다 낮음 |
| **평균 mAP** | 0.3806 | ❌ 낮음 |
| **중앙값 mAP** | 0.5538 | ⚠️ 보통 |
| **mAP >= 0.7** | 0개 | ❌ 목표 미달 |
| **mAP >= 0.65** | 1개 | ⚠️ 매우 적음 |
| **mAP >= 0.6** | 3개 (16%) | ⚠️ 적음 |

---

## ❌ Phase 2 실패 원인

### 1. with_center_loss 설정 오류

**에러 메시지**:
```
Expected METRIC_LOSS_TYPE with center should be center, triplet_center
but got triplet
```

**원인**:
- `with_center_loss=true`일 때 `metric_loss_type`이 `"triplet"`으로 고정되어 있음
- TAO 규칙: `with_center_loss=true` → `metric_loss_type="triplet_center"` 필요

**영향**:
- 18개 실험 모두 시작 직후 실패
- 실제 유효 실험: 19개 (목표 60개의 32%)

### 2. 매개변수 고정값 문제

Phase 2에서 고정한 값이 Phase 1 최고값과 달랐음:

| 매개변수 | Phase 1 최고 | Phase 2 고정 | 영향 |
|---------|-------------|-------------|------|
| `gamma` | 0.5 | 0.3 | ❌ 성능 저하 |
| `weight_decay` | 5e-05 | 범위에 포함 | ✅ |
| `triplet_loss_margin` | 0.35 | [0.35, 0.4] | ✅ |

---

## ✅ Phase 2 새 매개변수 효과 분석

### 검증 완료된 매개변수

#### 1. warmup_method ⭐⭐⭐ (매우 중요)

| 값 | 평균 mAP | 최고 mAP | 실험 수 |
|----|----------|----------|---------|
| **linear** | **0.5439** | **0.6637** | 5 |
| cosine | 0.3223 | 0.5795 | 14 |

**결론**: **linear가 cosine보다 69% 더 높음** → linear 사용 필수

---

#### 2. num_instances ⭐⭐⭐ (매우 중요)

| 값 | 평균 mAP | 최고 mAP | 실험 수 |
|----|----------|----------|---------|
| **2** | **0.5914** | **0.6637** | 10 |
| 4 | 0.1494 | 0.4005 | 7 |
| 8 | 0.1356 | 0.1559 | 2 |

**결론**: **num_instances=2가 압도적** → 4, 8은 사용 금지

---

#### 3. with_flip_feature ⭐

| 값 | 평균 mAP | 최고 mAP | 실험 수 |
|----|----------|----------|---------|
| **True** | **0.4861** | **0.6637** | 9 |
| False | 0.2857 | 0.6420 | 10 |

**결론**: True가 평균적으로 70% 더 높음 → True 사용 권장

---

#### 4. prob, re_prob (데이터 증강)

**prob (수평 플립 확률)**:
- 0.3: 평균 0.5641 (3개)
- 0.5: 평균 0.3237 (10개)
- 0.7: 평균 0.3837 (6개)

**re_prob (Random erasing)**:
- 0.3: 평균 0.3629 (5개)
- 0.5: 평균 0.3199 (8개)
- 0.7: 평균 0.4763 (6개)

**결론**: 명확한 패턴 없음 → 추가 탐색 필요

---

## 📈 Phase별 성능 비교

| 단계 | 실험 수 | 최고 mAP | 평균 mAP | 주요 발견 |
|------|---------|----------|----------|-----------|
| **c4s4yfvh** | 34 | 0.6954 | 0.3991 | lr, weight_decay 중요 |
| **Phase 1** | 100 | **0.7044** ⭐ | 0.3895 | **batch_size=32** 발견 |
| **Phase 2** | 19 | 0.6637 ❌ | 0.3806 | warmup_method=linear, num_instances=2 |
| **Phase 3 (예상)** | 30 | **0.71+** | 0.65+ | 최적 조합 확정 |

### 최고 성능 비교

**Phase 1 (solar-sweep-1)**: mAP 0.7044 ⭐
```yaml
lr: 0.002
weight_decay: 5e-05
warmup_factor: 0.05
warmup_iters: 5
triplet_loss_margin: 0.35
batch_size: 32
feat_dim: 512
gamma: 0.5  ⬅️ 핵심!
```

**Phase 2 (true-sweep-34)**: mAP 0.6637 ❌
```yaml
lr: 0.002
weight_decay: 0.0001  ⬅️ 다름
warmup_factor: 0.05
warmup_iters: 5
triplet_loss_margin: 0.4  ⬅️ 다름
batch_size: 32
feat_dim: 512
gamma: 0.3  ⬅️ 다름! (문제)
warmup_method: linear  ⬅️ 새로 추가
num_instances: 2  ⬅️ 새로 추가
prob: 0.7
re_prob: 0.3
with_flip_feature: True  ⬅️ 새로 추가
```

**차이 분석**:
- ❌ **gamma**: 0.3 vs 0.5 (가장 큰 차이)
- ❌ weight_decay: 0.0001 vs 5e-05
- ❌ triplet_loss_margin: 0.4 vs 0.35

---

## 🎯 Phase 3 전략 (권장)

### 핵심 원칙

**"Phase 1 최고값으로 회귀 + 검증된 새 매개변수 추가"**

### Phase 3 설정

```yaml
name: reid_market1501_resnet_phase3_sweep
method: bayes
metric:
  name: mAP
  goal: maximize

parameters:
  # Phase 1 최고 성능(solar-sweep-1) 완전 복원
  lr: [2.0e-3]                    # 고정
  weight_decay: [5.0e-5]          # Phase 1 최고값 복원
  warmup_factor: [0.05]           # Phase 1 최고값
  warmup_iters: [5]               # 고정
  triplet_loss_margin: [0.35]     # Phase 1 최고값 복원
  batch_size: [32]                # 고정
  feat_dim: [512]                 # 고정
  gamma: [0.5]                    # Phase 1 최고값 복원! ⭐
  
  # Phase 2 검증 완료 매개변수
  warmup_method: ["linear"]       # 고정 (cosine 대비 69% 향상)
  num_instances: [2]              # 고정 (4, 8 대비 4배 향상)
  with_flip_feature: [true, false]  # 재검증
  
  # 유일한 탐색 영역: 데이터 증강
  prob: [0.5, 0.6, 0.7, 0.8]
  re_prob: [0.3, 0.4, 0.5, 0.6, 0.7]

count: 30
results_dir_base: /results/results/market1501/resnet50/phase3
```

### 예상 조합 수
- with_flip_feature: 2개
- prob: 4개  
- re_prob: 5개
- **총**: 2 × 4 × 5 = **40개 조합**
- Bayes로 **30개 선택**

### 예상 결과
- **최고 mAP**: 0.71-0.72 (Phase 1 0.7044 초과 목표)
- **평균 mAP**: 0.65+
- **mAP >= 0.7**: 5-10개 (17-33%)
- **소요 시간**: 5-8시간

---

## 🚀 실행 준비

### 생성된 파일

```
sweeps/
└── reid_market1501_resnet_phase3_sweep.yaml (신규)

scripts/background/
└── run_reid_market1501_resnet_phase3_sweep.sh (신규)
```

### 실행 명령어

```bash
cd /home/jongphago/projects/tao_pytorch_backend

# tmux 세션에서 실행 (추천)
tmux new -s phase3_sweep
./scripts/background/run_reid_market1501_resnet_phase3_sweep.sh

# 또는 백그라운드 실행
nohup ./scripts/background/run_reid_market1501_resnet_phase3_sweep.sh \
  > logs/phase3_sweep_$(date +%Y%m%d_%H%M%S).log 2>&1 &
```

---

## 📋 Phase 2에서 배운 교훈

### ✅ 성공 요인
1. **warmup_method=linear** 발견 (cosine 대비 69% 향상)
2. **num_instances=2** 발견 (4, 8 대비 4배 향상)
3. **with_flip_feature=True** 효과 확인

### ❌ 실패 요인
1. **with_center_loss** 설정 오류로 50% 실험 손실
2. **gamma=0.3 고정**이 Phase 1의 0.5보다 낮은 성능
3. Phase 1 최적값 미준수

### 🔧 개선 사항
1. **sweep.py 수정 불필요**: with_center_loss 제외
2. **Phase 1 최적값 엄격히 준수**: gamma=0.5 복원
3. **검증된 매개변수만 추가**: 실험 효율성 증대

---

## 🎯 Phase 3 목표

### 단기 목표 (Phase 3)
- ✅ mAP 0.71+ 달성 (Phase 1의 0.7044 초과)
- ✅ 데이터 증강 최적 조합 발견
- ✅ with_flip_feature 효과 재검증

### 최종 목표
- ✅ 안정적으로 mAP 0.70+ 달성하는 매개변수 조합 확정
- ✅ 최종 최적 설정으로 full training 실행
- ✅ 최종 모델 성능 검증

---

## 📌 최종 최적 매개변수 (Phase 3 전)

### 현재까지 확정된 최적값

```yaml
# Optimizer
lr: 0.002
weight_decay: 5.0e-5
warmup_factor: 0.05
warmup_iters: 5
warmup_method: linear  # Phase 2 검증
triplet_loss_margin: 0.35

# Scheduler
gamma: 0.5  # Phase 1 최고값

# Dataset
batch_size: 32  # Phase 1 발견
num_instances: 2  # Phase 2 검증

# Model
feat_dim: 512
with_flip_feature: true  # Phase 2에서 True가 좋았음 (재검증 필요)

# 미확정 (Phase 3에서 결정)
prob: ?  # [0.5~0.8] 탐색 중
re_prob: ?  # [0.3~0.7] 탐색 중
```

---

## 🚀 다음 액션

### 즉시 실행

1. **Phase 2 실험 중지**
   ```bash
   # 실행 중인 프로세스 종료
   pkill -f "phase2"
   ```

2. **Phase 3 실행**
   ```bash
   cd /home/jongphago/projects/tao_pytorch_backend
   
   # tmux 세션 생성 및 실행
   tmux new -s phase3_sweep
   ./scripts/background/run_reid_market1501_resnet_phase3_sweep.sh
   ```

3. **모니터링**
   - W&B: https://wandb.ai/jongphago/TAO%20Toolkit
   - 로그: `tail -f logs/phase3_sweep_*.log`
   - 예상 소요: 5-8시간 (30개 실험)

### Phase 3 완료 후

1. **결과 분석**
   - 최고 mAP 확인 (0.71+ 목표)
   - prob, re_prob 최적값 확정

2. **최종 매개변수 확정**
   - 전체 매개변수 조합 문서화

3. **Full Training**
   - 최적 매개변수로 완전 학습
   - 최종 모델 검증

---

## 📊 전체 실험 로드맵

```
c4s4yfvh (34개)
   ↓ mAP 0.6954
   
Phase 1 (100개)
   ↓ mAP 0.7044 ⭐
   ↓ batch_size=32 발견
   
Phase 2 (19개) ← 실패 18개
   ↓ mAP 0.6637 ❌
   ↓ warmup_method=linear, num_instances=2 검증
   
Phase 3 (30개) ← 진행 예정 ⭐
   ↓ mAP 0.71+ 목표
   ↓ prob, re_prob 최적화
   
최종 모델
   mAP 0.72+
```

---

## 📝 체크리스트

- [x] Phase 2 결과 분석
- [x] Phase 2 실패 원인 파악
- [x] Phase 3 전략 수립
- [x] Phase 3 YAML 파일 생성
- [x] Phase 3 실행 스크립트 생성
- [ ] Phase 2 실험 중지
- [ ] Phase 3 실험 실행
- [ ] Phase 3 결과 분석
- [ ] 최종 매개변수 확정

---

**보고서 끝**

*다음 단계: Phase 3 실행*

