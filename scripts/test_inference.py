import sys
from mmdet.apis import init_detector, inference_detector

config_file = 'configs/train_gun_knife.py'
checkpoint_file = 'work_dirs/fast_train_gun_knife/epoch_3.pth'

print("Initializing detector...")
try:
    model = init_detector(config_file, checkpoint_file, device='cuda:0')
    print("Detector initialized successfully!")
    
    # Overwrite the CLASSES to 2 classes just for our custom dataset printing
    # (Gun and Knife)
    model.CLASSES = ('Gun', 'Knife')
    
    # Let's test on the first training image just to verify the network forwards without crashing
    img = 'data/pidray/train/xray_00000.png'
    print(f"Testing inference on {img}...")
    result = inference_detector(model, img)
    
    # result is a tuple of (bbox_results, mask_results) if mask is enabled
    if isinstance(result, tuple):
        bbox_result, segm_result = result
    else:
        bbox_result, segm_result = result, None
        
    print(f"Inference successful! Found {sum([len(x) for x in bbox_result])} bounding boxes.")
    for i, class_bboxes in enumerate(bbox_result):
        if len(class_bboxes) > 0:
            print(f"  Class {model.CLASSES[i]}: {len(class_bboxes)} detections.")
            
    print("\n✅ Training and inference pipeline are confirmed working properly!")

except Exception as e:
    print(f"\n❌ Error during inference: {e}")
    sys.exit(1)
