# Phase 2 Sweep 실패 원인 분석 보고서

**스윕 ID**: 8uslnc5i  
**작성일**: 2025-10-01  
**상태**: 실행 중 (일부 실패)

---

## 📊 현황

| 항목 | 개수 | 비율 |
|------|------|------|
| **총 실험** | 36개 | 100% |
| **성공** | 0개 | 0% |
| **실패** | 18개 | 50% |
| **실행 중** | 18개 | 50% |

---

## ❌ 실패 원인

### 에러 메시지

```
Expected METRIC_LOSS_TYPE with center should be center, triplet_center
but got triplet
```

### 근본 원인

**Phase 2 설정 문제**: `with_center_loss`와 `metric_loss_type` 불일치

#### 실패한 실험 설정
```yaml
model:
  with_center_loss: true
  metric_loss_type: triplet  ← 문제!
```

#### 성공한 실험 설정
```yaml
model:
  with_center_loss: false
  metric_loss_type: triplet  ← 정상
```

### TAO 검증 규칙

`with_center_loss=true`일 때 `metric_loss_type`은 다음 중 하나여야 함:
- `"center"`
- `"triplet_center"`

**현재 문제**:
- Phase 2 sweep에서 `with_center_loss: [true, false]` 추가
- 하지만 `metric_loss_type`은 항상 `"triplet"`로 고정
- → `with_center_loss=true`인 18개 실험 모두 시작 직후 실패

---

## ✅ 해결 방법

### 방법 1: sweep.py 수정 (권장)

**수정 위치**: `nvidia_tao_pytorch/cv/re_identification/scripts/sweep.py`

```python
# with_center_loss 전달 부분 수정 (Line 239-257 근처)
if with_center_loss is not None:
    cmd_parts.append(f"model.with_center_loss={with_center_loss}")
    
    # metric_loss_type도 함께 조정
    if with_center_loss:
        cmd_parts.append("model.metric_loss_type=triplet_center")
    # else는 기본값(triplet) 사용
```

### 방법 2: Phase 2 설정 수정 (임시 해결)

**Phase 2 YAML에서 `with_center_loss` 제거**:

```yaml
# 수정 전
with_center_loss: [true, false]
with_flip_feature: [true, false]

# 수정 후 (with_center_loss 제거)
with_flip_feature: [true, false]
```

`with_center_loss`는 Phase 3에서 별도로 테스트

---

## 📋 영향 분석

### 실패한 18개 실험
- 모두 `with_center_loss=true` 설정
- 학습 시작 직후 (3초 이내) 실패
- GPU 자원 낭비 없음 (빠른 실패)

### 실행 중인 18개 실험
- 모두 `with_center_loss=false` 설정
- 정상적으로 학습 진행 중
- 예상대로 동작

### Phase 2 목표 달성도
- 원래 목표: 60개 실험
- 현재: 18개만 유효
- **달성률**: 30% (18/60)

---

## 🎯 권장 조치

### 즉시 조치 (진행 중인 스윕)

1. **현재 스윕 계속 진행**
   - 18개 실험이라도 유의미한 데이터
   - `with_flip_feature` 효과 검증 가능

2. **결과 분석 시 주의**
   - `with_center_loss` 효과는 미검증
   - 18개 실험 결과로 Phase 2 목표 일부 달성

### 후속 조치

1. **sweep.py 수정**
   - `with_center_loss`와 `metric_loss_type` 연동
   - 코드 수정 및 테스트

2. **Phase 2 재실행 또는 Phase 3 계획**
   
   **옵션 A**: Phase 2 재실행
   - sweep.py 수정 후 60개 전체 재실행
   - `with_center_loss` 효과 포함 검증
   
   **옵션 B**: Phase 3 별도 실행
   - Phase 2 현재 결과 활용
   - Phase 3에서 `with_center_loss` 집중 테스트
   ```yaml
   # Phase 3 설정 예시
   with_center_loss: [true, false]
   metric_loss_type: ["triplet", "triplet_center"]
   # 조건: with_center_loss=true일 때만 metric_loss_type=triplet_center
   ```

---

## 📌 교훈

### 발견된 문제
1. **sweep.py의 한계**: 조건부 매개변수 처리 미지원
2. **Phase 2 설계 검토 부족**: TAO 검증 규칙 미확인
3. **사전 테스트 부족**: 소규모 테스트 없이 바로 60개 실행

### 개선 사항
1. ✅ **조건부 매개변수 처리 추가**
   - `with_center_loss` → `metric_loss_type` 자동 조정
   
2. ✅ **Phase 설계 시 TAO 규칙 확인**
   - 매개변수 간 의존성 사전 파악
   - 코드 레벨 검증 로직 확인

3. ✅ **사전 테스트 프로세스**
   - 새 매개변수 추가 시 2-3개 실험으로 검증
   - 성공 확인 후 전체 스윕 실행

---

## 📊 다음 단계

### 단기 (현재 스윕 완료 후)

1. **18개 실험 결과 분석**
   - `with_flip_feature` 효과 검증
   - 다른 매개변수 조합 분석

2. **sweep.py 수정**
   - 조건부 매개변수 처리 구현
   - 테스트 및 검증

### 중기 (1-2일 내)

1. **Phase 2 재실행 여부 결정**
   - 18개 결과로 충분한지 평가
   - 필요 시 수정된 sweep.py로 재실행

2. **Phase 3 계획 수립**
   - `with_center_loss` 집중 테스트
   - 최종 최적 매개변수 확정

---

## 부록: 실패한 실험 목록

```
breezy-sweep-9
smart-sweep-24
flowing-sweep-25
... (총 18개)
```

**공통점**: 모두 `with_center_loss=true`

---

**보고서 끝**

*작성: AI Assistant*  
*상태: 실험 진행 중 (18개 유효)*

