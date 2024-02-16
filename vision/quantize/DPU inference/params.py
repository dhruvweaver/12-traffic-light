TRAINING_PARAMS = \
{
    "model_params": {
        "backbone_name": "darknet_53",
        "backbone_pretrained": "",
    },
    "yolo": {
        "anchors": [[[116, 90], [156, 198], [373, 326]],
                    [[30, 61], [62, 45], [59, 119]],
                    [[10, 13], [16, 30], [33, 23]]],
        "classes": 3,
    },
    "batch_size": 32,
    "confidence_threshold": 0.5,
    "images_path": "../test/images/",
    "classes_names_path": "../data/coco.names",
    "img_h": 640,
    "img_w": 640,
    "parallels": [0],
    "pretrain_snapshot": "../../vision-prototype/custom-train/weights/best.pt",
}
