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
      - resnet 설정 가능한 값 정의(`arch_settings`): [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:144](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)
      - swin 설정 가능한 값 매핑: [nvidia_tao_pytorch/cv/re_identification/model/build_nn_model.py:34](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/build_nn_model.py)

  - `last_stride`
    - 기본값
      - `1`
    - 설명
      - 백본 마지막 스테이지의 스트라이드
    - 설정 가능한 값
      - 고정: `1` (변경 불가 설정)
    - 참고 문헌
      - 기본값/유효값 정의: [nvidia_tao_pytorch/cv/re_identification/config/default_config.py:34](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/config/default_config.py)

  - `pretrain_choice`
    - 기본값
      - `imagenet`
    - 설명
      - 사전학습 가중치 소스
    - 설정 가능한 값
      - imagenet
      - self
    - 참고 문헌
      - 이미지넷 선택 시 로딩 분기: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:156](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)
      - 실험 예시(`self` 사용): [nvidia_tao_pytorch/cv/re_identification/experiment_specs/experiment_market1501_swin.yaml:6](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/experiment_specs/experiment_market1501_swin.yaml)

  - `pretrained_model_path`
    - 기본값
      - `None`
    - 설명
      - 사전학습 가중치 파일 경로(선택)
    - 참고 문헌
      - 로드 사용처(ResNet): [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:158](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `input_channels`
    - 기본값
      - `3`
    - 설명
      - 입력 채널 수
    - 설정 가능한 값
      - 고정: `3`

  - `input_width`, `input_height`
    - 기본값
      - `128`, `256`
    - 설명
      - 입력 이미지 크기
    - 설정 가능한 값
      - 현재 기본값 고정

  - `neck`
    - 기본값
      - `bnneck`
    - 설명
      - 넥 구조 선택
    - 설정 가능한 값
      - ''(빈 값, 넥 없음)
      - bnneck
    - 참고 문헌
      - 넥 분기(없음/BNNeck): [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:168](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `feat_dim`
    - 기본값
      - `256`
    - 설명
      - 피처 차원
    - 유효 범위
      - 32 ~ 768

  - `neck_feat`
    - 기본값
      - `after`
    - 설명
      - 테스트 시 사용할 피처 위치
    - 설정 가능한 값
      - after
      - before
    - 참고 문헌
      - after 분기 사용: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:220](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `metric_loss_type`
    - 기본값
      - `triplet`
    - 설명
      - 메트릭 손실 종류
    - 설정 가능한 값
      - triplet
      - center (with_center_loss가 True인 경우)
      - triplet_center (with_center_loss가 True인 경우)
    - 참고 문헌
      - triplet 사용 분기: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:387](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)
      - center/triplet_center 분기: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:431](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py), [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:435](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `with_center_loss`
    - 기본값
      - `False`
    - 설명
      - 센터 로스 사용 여부

  - `with_flip_feature`
    - 기본값
      - `False`
    - 설명
      - flip feature 사용 여부

  - `label_smooth`
    - 기본값
      - `True`
    - 설명
      - 라벨 스무딩 적용 여부
    - 참고 문헌
      - 스무딩 적용 교차엔트로피: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:394](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `pretrain_hw_ratio`
    - 기본값
      - `2`
    - 설명
      - 이미지넷 사전학습 모델의 H/W 비율
    - 비고
      - Swin 이미지넷 로딩 시 사용

  - `id_loss_type`
    - 기본값
      - `softmax`
    - 설명
      - ID 분류 손실의 종류
    - 설정 가능한 값
      - softmax
      - arcface
      - cosface
      - amsoftmax
      - circle
    - 참고 문헌
      - 기본값 정의: [nvidia_tao_pytorch/cv/re_identification/config/default_config.py:48](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/config/default_config.py)
      - Swin(Transformer)에서 분류기 선택: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:277](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)
      - Swin+JPM(TransformerLocal)에서 분류기 선택: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:418](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)
      - 각 손실 구현(ArcFace/CosFace/AMSoftmax/Circle): [nvidia_tao_pytorch/cv/re_identification/model/losses/metric_learning.py:131](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/losses/metric_learning.py), [199](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/losses/metric_learning.py), [257](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/losses/metric_learning.py), [80](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/losses/metric_learning.py)

  - `id_loss_weight`
    - 기본값
      - `1.0`
    - 설명
      - ID 손실 가중치
    - 유효 범위
      - 0.0 ~ 1.0
    - 모호 사항
      - 현재 코드에서 직접 가중 합산 사용처 미확인

  - `triplet_loss_weight`
    - 기본값
      - `1.0`
    - 설명
      - 트리플릿 손실 가중치
    - 유효 범위
      - 0.0 ~ 1.0
    - 모호 사항
      - 현재 코드에서 직접 가중 합산 사용처 미확인

  - `no_margin`
    - 기본값
      - `False`
    - 설명
      - 마진 미사용 플래그
    - 모호 사항
      - 현재 로스 계산 분기에서 직접 사용처 미확인

  - `cos_layer`
    - 기본값
      - `False`
    - 설명
      - 코사인 레이어 사용 여부
    - 모호 사항
      - 설정만 존재, 활성 분기/사용처 미확인

  - `dropout_rate`
    - 기본값
      - `0.0`
    - 설명
      - 분류기 입력 드롭아웃 비율

  - `reduce_feat_dim`
    - 기본값
      - `False`
    - 설명
      - FC로 피처 차원 축소 사용 여부

  - `drop_path`, `drop_out`, `att_drop_rate`
    - 기본값
      - `0.1`, `0.0`, `0.0`
    - 설명
      - Swin 백본 내 드롭 경로/드롭아웃/어텐션 드롭아웃 비율
    - 참고 문헌
      - Swin 생성자 인자: [nvidia_tao_pytorch/cv/re_identification/model/backbones/swin_transformer.py:1149](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/swin_transformer.py)

  - `stride_size`
    - 기본값
      - `[16, 16]`
    - 설명
      - Swin 로컬 피처 브랜치에서 사용되는 stride 설정
    - 참고 문헌
      - TransformerLocal 생성 인자: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:400](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `gem_pooling`, `stem_conv`
    - 기본값
      - `False`, `False`
    - 설명
      - GEM 풀링/Stem Conv 사용 여부
    - 모호 사항
      - 코드 내 직접 사용처 미확인

  - `jpm`
    - 기본값
      - `False`
    - 설명
      - 로컬 브랜치(JPM) 활성화 시 TransformerLocal 사용
    - 참고 문헌
      - JPM 여부에 따른 모델 선택: [nvidia_tao_pytorch/cv/re_identification/model/build_nn_model.py:41](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/build_nn_model.py)

  - `shift_num`, `shuffle_group`, `devide_length`, `re_arrange`
    - 기본값
      - `5`, `2`, `4`, `True`
    - 설명
      - 로컬 피처 재배열 관련 하이퍼파라미터
    - 모호 사항
      - 재배열 파라미터의 상세 사용처 제한적(외부 모듈/실험적 기능)

  - `sie_coe`, `sie_camera`, `sie_view`
    - 기본값
      - `3.0`, `False`, `False`
    - 설명
      - SIE(Spatial Information Enhancement) 관련 계수/사용 여부
    - 참고 문헌
      - Swin 백본 생성 인자(`sie_xishu`, camera, view): [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:400](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `semantic_weight`
    - 기본값
      - `1.0`
    - 설명
      - Transformer 세만틱 손실 가중
    - 참고 문헌
      - Transformer 생성 인자 전달: [nvidia_tao_pytorch/cv/re_identification/model/build_nn_model.py:44](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/build_nn_model.py)

- `dataset`
  - `train_dataset_dir`, `test_dataset_dir`, `query_dataset_dir`
    - 기본값
      - `None`
    - 설명
      - 각 데이터셋 루트 경로

  - `num_classes`
    - 기본값
      - `751`
    - 설명
      - 클래스 수
    - 유효 범위
      - 1 이상

  - `batch_size`, `val_batch_size`, `num_workers`
    - 기본값
      - `64`, `128`, `8`
    - 설명
      - 배치/검증 배치/워커 수

  - `pixel_mean`, `pixel_std`, `padding`
    - 기본값
      - `[0.485, 0.456, 0.406]`, `[0.226, 0.226, 0.226]`, `10`
    - 설명
      - 정규화/패딩 설정

  - `prob`, `re_prob`
    - 기본값
      - `0.5`, `0.5`
    - 설명
      - 각종 변환 확률

  - `sampler`
    - 기본값
      - `softmax_triplet`
    - 설명
      - 로스 구성에 맞는 샘플러 타입
    - 설정 가능한 값
      - softmax
      - triplet
      - softmax_triplet
    - 참고 문헌
      - 샘플러별 손실 구성: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:396](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py), [400](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py), [402](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)
      - RandomIdentitySampler 사용: [nvidia_tao_pytorch/cv/re_identification/dataloader/build_data_loader.py:123](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/dataloader/build_data_loader.py)

  - `num_instances`
    - 기본값
      - `4`
    - 설명
      - ID당 인스턴스 수(샘플러 파라미터)
    - 참고 문헌
      - 샘플러 인자: [nvidia_tao_pytorch/cv/re_identification/dataloader/build_data_loader.py:125](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/dataloader/build_data_loader.py)

- `re_ranking`
  - `re_ranking`
    - 기본값
      - `False`
    - 설명
      - Re-ranking 사용 여부

  - `k1`, `k2`, `lambda_value`, `max_rank`, `num_query`
    - 기본값
      - `20`, `6`, `0.3`, `10`, `10`
    - 설명
      - Re-ranking 하이퍼파라미터

- `train.optim`
  - `name`
    - 기본값
      - `Adam`
    - 설명
      - 옵티마이저 이름
    - 설정 가능한 값
      - Adam, SGD, AdamW, (그 외 torch.optim 내 등록명)
    - 참고 문헌
      - SGD/AdamW 특수 처리 및 일반 처리: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:140](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `lr_monitor`
    - 기본값
      - `val_loss`
    - 설명
      - 스케줄 모니터 메트릭

  - `lr_steps`, `gamma`
    - 기본값
      - `[40, 70]`, `0.1`
    - 설명
      - 멀티스텝 스케줄러 마일스톤/감쇠율

  - `bias_lr_factor`, `weight_decay`, `weight_decay_bias`
    - 기본값
      - `1`, `0.0005`, `0.0005`
    - 설명
      - 옵티마이저 계수/가중감쇠

  - `warmup_factor`, `warmup_iters`, `warmup_epochs`, `warmup_method`
    - 기본값
      - `0.01`, `10`, `20`, `linear`
    - 설명
      - 워밍업 설정 및 스케줄러 선택
    - 설정 가능한 값
      - warmup_method: linear, cosine
    - 참고 문헌
      - cosine 선택 시 코사인 스케줄러: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:105](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)
      - 그 외 WarmupMultiStepLR 사용: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:108](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `base_lr`, `momentum`
    - 기본값
      - `0.00035`, `0.9`
    - 설명
      - 기본 학습률/모멘텀

  - `center_loss_weight`, `center_lr`
    - 기본값
      - `0.0005`, `0.5`
    - 설명
      - 센터 로스 가중/학습률
    - 참고 문헌
      - 센터 로스 결합 계산: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:446](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py), [453](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `triplet_loss_margin`
    - 기본값
      - `0.3`
    - 설명
      - 트리플릿 마진
    - 참고 문헌
      - TripletLoss 초기화 인자: [nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py:388](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/pl_reid_model.py)

  - `large_fc_lr`
    - 기본값
      - `False`
    - 설명
      - FC 계층에 큰 LR 적용 여부

  - `cosine_margin`, `cosine_scale`
    - 기본값
      - `0.5`, `30`
    - 설명
      - 코사인 마진/스케일(ArcFace 등에서 사용)
    - 참고 문헌
      - 분류기 생성 시 전달: [nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py:279](/home/jongphago/projects/tao_pytorch_backend/nvidia_tao_pytorch/cv/re_identification/model/backbones/baseline.py)

  - `trp_l2`
    - 기본값
      - `False`
    - 설명
      - 트리플릿 L2 정규화 사용 여부

  - `grad_clip`
    - 기본값
      - `0.0`
    - 설명
      - 그래디언트 클리핑 최대 노름

- `inference`
  - `output_file`, `test_dataset`, `query_dataset`
    - 기본값
      - `None`, `None`, `None`
    - 설명
      - 추론 결과/테스트/쿼리 경로

- `evaluate`
  - `output_sampled_matches_plot`, `output_cmc_curve_plot`, `test_dataset`, `query_dataset`
    - 기본값
      - `None`, `None`, `None`, `None`
    - 설명
      - 평가 결과 플롯/데이터 경로

- `export`
  - `results_dir`, `checkpoint`, `onnx_file`, `gpu_id`
    - 기본값
      - `None`, `None`, `None`, `0`
    - 설명
      - 내보내기 설정(체크포인트/ONNX 경로/GPU ID)