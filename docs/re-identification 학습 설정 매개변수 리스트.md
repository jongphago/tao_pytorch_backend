# ReIdentification W&B Sweep Parameter Report

- `model`
  - `backbone`
    - 기본값
      - `resnet_50`
    - 설명
      - 모델의 백본 타입
    - 설정 가능한 값
      - resnet_18
      - resnet_34
      - resnet_50
      - resnet_101
      - resnet_152
      - swin_base_patch4_window7_224
      - swin_small_patch4_window7_224
      - swin_tiny_patch4_window7_224
    - 참고 문헌
      - ResNet 백본 정의(`arch_settings`): [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:144](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)
      - Swin 백본 팩토리 매핑: [nvidia_tao_pytorch/cv/re_identification/model/build_nn_model.py:34](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/build_nn_model.py)

  - `last_stride`
    - 기본값
      - `1`
    - 설명
      - ResNet 마지막 스테이지 stride (ResNet 변형에서 고정)
    - 설정 가능한 값
      - 고정: `1`
    - 참고 문헌
      - `last_stride` 인자 전달: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:152](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `pretrain_choice`
    - 기본값
      - `imagenet`
    - 설명
      - 사전 학습 가중치 로딩 여부
    - 설정 가능한 값
      - imagenet
      - self (사용자 제공 체크포인트)
    - 참고 문헌
      - ImageNet 분기 로직: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:156](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)
      - self 사용 예시: [nvidia_tao_pytorch/cv/re_identification/experiment_specs/experiment_market1501_swin.yaml:6](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/experiment_specs/experiment_market1501_swin.yaml)

  - `pretrained_model_path`
    - 기본값
      - `None`
    - 설명
      - 외부 사전 학습 모델 경로
    - 참고 문헌
      - ResNet 가중치 로드: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:157](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)
      - Swin 가중치 로드: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:244](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `input_channels`
    - 기본값
      - `3`
    - 설명
      - 입력 영상 채널 수 (RGB)
    - 설정 가능한 값
      - 고정: `3`
    - 참고 문헌
      - ONNX 더미 입력 생성 시 사용: [nvidia_tao_pytorch/cv/re_identification/scripts/export.py:115](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/scripts/export.py)

  - `input_width`, `input_height`
    - 기본값
      - `128`, `256`
    - 설명
      - 입력 영상 크기 (너비/높이)
    - 유효 범위
      - 코드상 명시된 제한 없음 (네트워크 구조와 데이터셋에 맞춰 조정)
    - 참고 문헌
      - 데이터 증강 시 사용: [nvidia_tao_pytorch/cv/re_identification/dataloader/transforms.py:44](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/dataloader/transforms.py)
      - ONNX 더미 입력 크기: [nvidia_tao_pytorch/cv/re_identification/scripts/export.py:115](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/scripts/export.py)

  - `neck`
    - 기본값
      - `bnneck`
    - 설명
      - 분류기 앞단 Neck 구성
    - 설정 가능한 값
      - 빈 문자열(넥 없음)
      - bnneck
    - 참고 문헌
      - Neck 분기 처리: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:168](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `feat_dim`
    - 기본값
      - `256`
    - 설명
      - 임베딩 피처 차원
    - 유효 범위
      - 32 ~ 768 (스키마 제한)
    - 참고 문헌
      - ResNet Baseline에서 feat_dim 사용: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:141](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `neck_feat`
    - 기본값
      - `after`
    - 설명
      - 평가 시 어떤 단계의 피처를 사용할지 결정
    - 설정 가능한 값
      - after
      - before
    - 참고 문헌
      - after 분기 처리: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:220](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `metric_loss_type`
    - 기본값
      - `triplet`
    - 설명
      - 메트릭 손실 종류
    - 설정 가능한 값
      - triplet
      - center (with_center_loss 사용 시)
      - triplet_center (with_center_loss 사용 시)
    - 참고 문헌
      - triplet 로스 생성: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:387](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)
      - center/triplet_center 분기: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:431](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `with_center_loss`
    - 기본값
      - `False`
    - 설명
      - 센터 로스 활성화 여부
    - 참고 문헌
      - 센터 로스 활성화 분기: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:62](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `with_flip_feature`
    - 기본값
      - `False`
    - 설명
      - 검증/추론 시 좌우 반전 특징 사용
    - 참고 문헌
      - flip 처리 분기: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:191](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `label_smooth`
    - 기본값
      - `True`
    - 설명
      - CrossEntropy에 라벨 스무딩 적용 여부
    - 참고 문헌
      - 스무딩 적용 로직: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:393](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `pretrain_hw_ratio`
    - 기본값
      - `2`
    - 설명
      - Swin 사전 학습 모델의 입력 높이/너비 비율 (가중치 로딩 시 필요)
    - 참고 문헌
      - Swin 가중치 로드시 비율 사용: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:403](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `id_loss_type`
    - 기본값
      - `softmax`
    - 설명
      - ID 분류 손실 종류 (Transformer/TransformerLocal에서 분기)
    - 설정 가능한 값
      - softmax
      - arcface
      - cosface
      - amsoftmax
      - circle
    - 참고 문헌
      - Transformer 분류기 선택: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:277](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)
      - TransformerLocal 분류기 선택: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:418](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `id_loss_weight`
    - 기본값
      - `1.0`
    - 설명
      - ID 분류 손실 가중치 (현 코드에서 직접 사용 흔적 없음)
    - 모호 사항
      - 가중 합산 지점 미확인 — 커스텀 실험 시 수동 적용 필요

  - `triplet_loss_weight`
    - 기본값
      - `1.0`
    - 설명
      - 트리플릿 손실 가중치 (현 코드에서 직접 사용 흔적 없음)
    - 모호 사항
      - 가중 합산 지점 미확인 — 필요 시 사용자 정의 손실에서 사용

  - `no_margin`
    - 기본값
      - `False`
    - 설명
      - TripletLoss에서 margin을 제거할지 결정하려는 플래그로 추정
    - 모호 사항
      - 코드 내 실제 사용처 미확인 (실험 시 영향도 검증 필요)

  - `cos_layer`
    - 기본값
      - `False`
    - 설명
      - Transformer 계열에서 cosine 기반 분류기 활성화 여부
    - 참고 문헌
      - cos_layer 저장 및 forward 주석: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:246](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `dropout_rate`
    - 기본값
      - `0.0`
    - 설명
      - Transformer 분류기 입력 드롭아웃 비율
    - 참고 문헌
      - 드롭아웃 초기화: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:306](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `reduce_feat_dim`
    - 기본값
      - `False`
    - 설명
      - Transformer에서 FC로 피처 차원 축소 여부
    - 참고 문헌
      - 차원 축소 분기: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:295](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `drop_path`, `drop_out`, `att_drop_rate`
    - 기본값
      - `0.1`, `0.0`, `0.0`
    - 설명
      - Swin 백본의 drop-path / dropout / attention-dropout 비율
    - 참고 문헌
      - Swin 생성자 인자 전달: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:265](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)
      - Swin 구현부의 semantic weight 설정: [nvidia_tao_pytorch/cv/re_identification/model/backbones/swin_transformer.py:1532](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/swin_transformer.py)

  - `stride_size`
    - 기본값
      - `[16, 16]`
    - 설명
      - TransformerLocal의 로컬 브랜치 stride 설정
    - 참고 문헌
      - Swin 생성 시 stride 전달: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:400](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `gem_pooling`, `stem_conv`
    - 기본값
      - `False`, `False`
    - 설명
      - 확장 옵션 (일반화 평균 풀링/GEM, stem conv) — 현재 코드 내 사용처 미확인
    - 모호 사항
      - 플래그만 존재, 실제 모델 구성에 반영되는 코드 미발견

  - `jpm`
    - 기본값
      - `False`
    - 설명
      - Joint Part-based branch 활성화 여부 (TransformerLocal 사용)
    - 참고 문헌
      - JPM 여부에 따른 모델 선택: [nvidia_tao_pytorch/cv/re_identification/model/build_nn_model.py:41](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/build_nn_model.py)
      - TransformerLocal에서 local_feature 플래그 사용: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:400](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `shift_num`, `shuffle_group`
    - 기본값
      - `5`, `2`
    - 설명
      - TransformerLocal에서 토큰 재배열 시 사용되는 하이퍼파라미터
    - 참고 문헌
      - 재배열 파라미터 로그 출력: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:463](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `devide_length`
    - 기본값
      - `4`
    - 설명
      - 로컬 토큰 분할 길이 (TransformerLocal)
    - 주의 사항
      - 코드 내에서 `cfg.model.DEVIDE_LENGTH`로 접근하는 오타 존재 → 값이 반영되지 않을 수 있음
    - 참고 문헌
      - divide length 접근 (오타 포함): [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:467](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `re_arrange`
    - 기본값
      - `True`
    - 설명
      - TransformerLocal에서 shuffle 기반 재배열 수행 여부
    - 참고 문헌
      - 재배열 분기: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:498](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `sie_coe`, `sie_camera`, `sie_view`
    - 기본값
      - `3.0`, `False`, `False`
    - 설명
      - Spatial Information Enhancement 관련 계수 및 카메라/뷰 조건
    - 참고 문헌
      - SIE 인자 전달: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:390](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `semantic_weight`
    - 기본값
      - `1.0`
    - 설명
      - Swin semantic branch 가중치
    - 참고 문헌
      - 모델 빌더에서 semantic_weight 전달: [nvidia_tao_pytorch/cv/re_identification/model/build_nn_model.py:44](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/build_nn_model.py)
      - Swin 내부 semantic embedding 로직: [nvidia_tao_pytorch/cv/re_identification/model/backbones/swin_transformer.py:1532](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/swin_transformer.py)

- `dataset`
  - `train_dataset_dir`, `test_dataset_dir`, `query_dataset_dir`
    - 기본값
      - `None`
    - 설명
      - 학습/갤러리/쿼리 데이터셋 루트 경로
    - 참고 문헌
      - Market1501 데이터 로더 경로 사용: [nvidia_tao_pytorch/cv/re_identification/dataloader/datasets/market1501.py:44](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/dataloader/datasets/market1501.py)
      - 학습 시 자동 클래스 수 계산: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:83](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `num_classes`
    - 기본값
      - `751`
    - 설명
      - 데이터셋 클래스 수 (평가/추론 시 사용)
    - 참고 문헌
      - 평가용 클래스 수 사용: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:88](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `batch_size`, `val_batch_size`
    - 기본값
      - `64`, `128`
    - 설명
      - 학습/검증 배치 크기
    - 참고 문헌
      - 학습 배치 사용: [nvidia_tao_pytorch/cv/re_identification/dataloader/build_data_loader.py:112](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/dataloader/build_data_loader.py)
      - 검증 배치 사용: [nvidia_tao_pytorch/cv/re_identification/dataloader/build_data_loader.py:134](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/dataloader/build_data_loader.py)

  - `num_workers`
    - 기본값
      - `8`
    - 설명
      - DataLoader worker 수 (GPU 수에 따라 곱해짐)
    - 참고 문헌
      - 워커 수 계산: [nvidia_tao_pytorch/cv/re_identification/dataloader/build_data_loader.py:103](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/dataloader/build_data_loader.py)

  - `pixel_mean`, `pixel_std`
    - 기본값
      - `[0.485, 0.456, 0.406]`, `[0.226, 0.226, 0.226]`
    - 설명
      - 영상 정규화 파라미터
    - 참고 문헌
      - Normalize 변환: [nvidia_tao_pytorch/cv/re_identification/dataloader/transforms.py:40](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/dataloader/transforms.py)

  - `padding`
    - 기본값
      - `10`
    - 설명
      - RandomCrop 이전 패딩 폭
    - 참고 문헌
      - 패딩 적용: [nvidia_tao_pytorch/cv/re_identification/dataloader/transforms.py:46](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/dataloader/transforms.py)

  - `prob`
    - 기본값
      - `0.5`
    - 설명
      - RandomHorizontalFlip 확률
    - 참고 문헌
      - 플립 확률 사용: [nvidia_tao_pytorch/cv/re_identification/dataloader/transforms.py:45](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/dataloader/transforms.py)

  - `re_prob`
    - 기본값
      - `0.5`
    - 설명
      - RandomErasing 적용 확률
    - 참고 문헌
      - RandomErasing 인자: [nvidia_tao_pytorch/cv/re_identification/dataloader/transforms.py:50](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/dataloader/transforms.py)

  - `sampler`
    - 기본값
      - `softmax_triplet`
    - 설명
      - 미니배치 구성 방식 (loss 결합에 영향)
    - 설정 가능한 값
      - softmax
      - triplet
      - softmax_triplet
    - 참고 문헌
      - 손실 함수 분기: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:396](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)
      - RandomIdentitySampler 구성: [nvidia_tao_pytorch/cv/re_identification/dataloader/build_data_loader.py:125](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/dataloader/build_data_loader.py)

  - `num_instances`
    - 기본값
      - `4`
    - 설명
      - ID당 인스턴스 수 (RandomIdentitySampler 파라미터)
    - 참고 문헌
      - sampler 인자 사용: [nvidia_tao_pytorch/cv/re_identification/dataloader/build_data_loader.py:125](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/dataloader/build_data_loader.py)

- `re_ranking`
  - `re_ranking`
    - 기본값
      - `False`
    - 설명
      - 평가 시 re-ranking 알고리즘 사용 여부
    - 참고 문헌
      - re_ranking 플래그로 메트릭 선택: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:194](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `k1`, `k2`, `lambda_value`
    - 기본값
      - `20`, `6`, `0.3`
    - 설명
      - re-ranking 알고리즘의 하이퍼파라미터 (Jaccard 조합)
    - 참고 문헌
      - rerank_gpu 호출 시 사용: [nvidia_tao_pytorch/cv/re_identification/utils/reid_metric.py:220](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/utils/reid_metric.py)

  - `max_rank`
    - 기본값
      - `10`
    - 설명
      - CMC/플롯 계산 시 고려할 최대 rank
    - 참고 문헌
      - R1_mAP 초기화: [nvidia_tao_pytorch/cv/re_identification/utils/reid_metric.py:84](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/utils/reid_metric.py)
      - 평가 플롯에서 사용: [nvidia_tao_pytorch/cv/re_identification/utils/eval_reid.py:111](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/utils/eval_reid.py)

  - `num_query`
    - 기본값
      - `10`
    - 설명
      - 샘플드 매치 플롯 생성 시 사용할 쿼리 수
    - 참고 문헌
      - 플롯 범위 정의: [nvidia_tao_pytorch/cv/re_identification/utils/common_utils.py:77](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/utils/common_utils.py)

- `train.optim`
  - `name`
    - 기본값
      - `Adam`
    - 설명
      - 옵티마이저 종류
    - 설정 가능한 값
      - Adam
      - SGD
      - AdamW
      - (torch.optim에 등록된 기타 옵티마이저 가능)
    - 참고 문헌
      - Optimizer 선택 로직: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:140](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `lr_monitor`
    - 기본값
      - `val_loss`
    - 설명
      - 러닝레이트 스케줄러 모니터 메트릭 이름
    - 참고 문헌
      - Lightning monitor 설정: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:116](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `lr_steps`, `gamma`
    - 기본값
      - `[40, 70]`, `0.1`
    - 설명
      - WarmupMultiStepLR 마일스톤/감쇠율
    - 참고 문헌
      - 스케줄러 생성 인자: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:108](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)
      - WarmupMultiStepLR 구현: [nvidia_tao_pytorch/cv/re_identification/lr_schedulers/warmup_multi_step_lr.py:43](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/lr_schedulers/warmup_multi_step_lr.py)

  - `bias_lr_factor`, `weight_decay`, `weight_decay_bias`
    - 기본값
      - `1`, `0.0005`, `0.0005`
    - 설명
      - 파라미터 그룹별 LR/가중감쇠 계수
    - 참고 문헌
      - 파라미터 그룹 구성: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:131](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `warmup_factor`, `warmup_iters`, `warmup_epochs`, `warmup_method`
    - 기본값
      - `0.01`, `10`, `20`, `linear`
    - 설명
      - 워밍업 설정 (cosine/linear/constant 등)
    - 설정 가능한 값
      - warmup_method: linear, constant, cosine
    - 참고 문헌
      - Cosine 스케줄러에서 warmup_epochs 사용: [nvidia_tao_pytorch/cv/re_identification/lr_schedulers/cosine_lr.py:38](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/lr_schedulers/cosine_lr.py)
      - WarmupMultiStepLR에서 허용 메서드: [nvidia_tao_pytorch/cv/re_identification/lr_schedulers/warmup_multi_step_lr.py:66](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/lr_schedulers/warmup_multi_step_lr.py)
      - cosine 선택 분기: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:105](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `base_lr`
    - 기본값
      - `0.00035`
    - 설명
      - 기본 학습률
    - 참고 문헌
      - 파라미터 그룹에서 사용: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:131](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `momentum`
    - 기본값
      - `0.9`
    - 설명
      - SGD 사용 시 모멘텀 값
    - 참고 문헌
      - SGD 생성 인자: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:141](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `center_loss_weight`, `center_lr`
    - 기본값
      - `0.0005`, `0.5`
    - 설명
      - 센터 로스 가중치 및 별도 옵티마이저 학습률
    - 참고 문헌
      - 센터 로스 옵티마이저 생성: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:148](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)
      - 로스 결합 시 가중치 사용: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:449](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `triplet_loss_margin`
    - 기본값
      - `0.3`
    - 설명
      - TripletLoss margin
    - 참고 문헌
      - TripletLoss 초기화: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:388](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `large_fc_lr`
    - 기본값
      - `False`
    - 설명
      - 분류기 파라미터에 대해 2배 학습률 적용 여부
    - 참고 문헌
      - FC 계층 LR 조정: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:136](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `cosine_margin`, `cosine_scale`
    - 기본값
      - `0.5`, `30`
    - 설명
      - ArcFace/CosFace/AMSoftmax/CircleLoss에 사용되는 하이퍼파라미터
    - 참고 문헌
      - 분류기 생성 시 전달: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:279](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `trp_l2`
    - 기본값
      - `False`
    - 설명
      - Triplet Loss 입력에 L2 정규화 적용 여부 (현 버전에서 미사용)

- `train`
  - `grad_clip`
    - 기본값
      - `0.0`
    - 설명
      - PyTorch Lightning `gradient_clip_val`
    - 참고 문헌
      - 훈련 스크립트에서 사용: [nvidia_tao_pytorch/cv/re_identification/scripts/train.py:52](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/scripts/train.py)

- `inference`
  - `output_file`
    - 기본값
      - `None`
    - 설명
      - 추론 결과(JSON) 저장 경로
    - 참고 문헌
      - 예측 종료 시 결과 저장: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:296](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `test_dataset`, `query_dataset`
    - 기본값
      - `None`
    - 설명
      - 추론용 갤러리/쿼리 데이터 경로
    - 참고 문헌
      - Market1501 데이터셋 분기: [nvidia_tao_pytorch/cv/re_identification/dataloader/datasets/market1501.py:47](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/dataloader/datasets/market1501.py)

- `evaluate`
  - `output_sampled_matches_plot`
    - 기본값
      - `None`
    - 설명
      - 샘플 매치 시각화 저장 경로
    - 참고 문헌
      - 평가 종료 시 플롯 저장: [nvidia_tao_pytorch/cv/re_identification/utils/eval_reid.py:110](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/utils/eval_reid.py)

  - `output_cmc_curve_plot`
    - 기본값
      - `None`
    - 설명
      - CMC 곡선 저장 경로
    - 참고 문헌
      - CMC 플롯 저장: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:278](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `test_dataset`, `query_dataset`
    - 기본값
      - `None`
    - 설명
      - 평가용 갤러리/쿼리 데이터 경로
    - 참고 문헌
      - Market1501 평가 분기: [nvidia_tao_pytorch/cv/re_identification/dataloader/datasets/market1501.py:50](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/dataloader/datasets/market1501.py)

- `export`
  - `results_dir`
    - 기본값
      - `None`
    - 설명
      - 내보내기 산출물 저장 폴더 (필요 시 사용자 지정)

  - `checkpoint`
    - 기본값
      - `None`
    - 설명
      - 내보낼 모델 체크포인트 경로
    - 참고 문헌
      - Lightning 모델 로드: [nvidia_tao_pytorch/cv/re_identification/scripts/export.py:99](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/scripts/export.py)

  - `onnx_file`
    - 기본값
      - `None`
    - 설명
      - ONNX 내보내기 파일 경로 (미지정 시 체크포인트 이름 기반 자동 생성)
    - 참고 문헌
      - ONNX 경로 기본값 처리: [nvidia_tao_pytorch/cv/re_identification/scripts/export.py:86](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/scripts/export.py)

  - `gpu_id`
    - 기본값
      - `0`
    - 설명
      - 내보내기 시 사용할 GPU ID
    - 참고 문헌
      - CUDA 디바이스 설정: [nvidia_tao_pytorch/cv/re_identification/scripts/export.py:72](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/scripts/export.py)
