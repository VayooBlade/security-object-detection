import gradio as gr
import cv2
import numpy as np
# Core inference pipeline for object detection
from mmdet.apis import init_detector, inference_detector

# --- CONFIGURATION ---
CONFIG_FILE = 'configs/train_gun_knife.py'
CHECKPOINT_FILE = 'work_dirs/fast_train_gun_knife/epoch_3.pth'
DEVICE = 'cuda:0'

print("Loading model...")
model = init_detector(CONFIG_FILE, CHECKPOINT_FILE, device=DEVICE)
model.CLASSES = ('Gun', 'Knife')
print("Model loaded successfully!")

def draw_boxes(img, result, score_thr=0.45):
    """
    Draw boxes directly on RGB image for Gradio.
    """
    colors = {
        'Gun': (220, 20, 60),    # Crimson Red
        'Knife': (34, 139, 34)   # Forest Green
    }
    
    # img is an RGB numpy array from Gradio
    out_img = img.copy()
    
    if isinstance(result, tuple):
        bbox_result, segm_result = result
    else:
        bbox_result, segm_result = result, None
        
    for i, class_bboxes in enumerate(bbox_result):
        if len(class_bboxes) > 0:
            for bbox in class_bboxes:
                score = bbox[4]
                if score >= score_thr:
                    x1, y1, x2, y2 = map(int, bbox[:4])
                    cls_name = model.CLASSES[i]
                    color = colors.get(cls_name, (0, 255, 0))
                    
                    # Draw bounding box
                    cv2.rectangle(out_img, (x1, y1), (x2, y2), color, 3)
                    
                    # Draw label background
                    label = f"{cls_name} {score:.2f}"
                    (tw, th), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                    cv2.rectangle(out_img, (x1, max(0, y1 - th - 10)), (x1 + tw + 10, y1), color, -1)
                    
                    # Draw text
                    cv2.putText(out_img, label, (x1 + 5, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    
    return out_img

def predict(image):
    if image is None:
        return None
        
    # MMDetection inference requires a BGR numpy array if passing an array directly
    # Gradio sends RGB numpy array
    img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Run inference
    result = inference_detector(model, img_bgr)
    
    # Draw boxes
    output_image = draw_boxes(image, result, score_thr=0.4)
    
    return output_image

# --- GRADIO INTERFACE ---
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue", secondary_hue="gray")) as demo:
    gr.Markdown("# 🔍 Professional Gun & Knife Detection")
    gr.Markdown(
        "Upload an X-Ray or standard image to detect the presence of **Guns** and **Knives**. "
        "The AI model processes the image in real-time and overlays bounding boxes with confidence scores."
    )
    
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(label="Upload Image", type="numpy")
            submit_btn = gr.Button("Detect Objects", variant="primary")
            
        with gr.Column():
            output_image = gr.Image(label="Detection Results", type="numpy")
            
    submit_btn.click(fn=predict, inputs=input_image, outputs=output_image)
    
    gr.Markdown("---")
    gr.Markdown("*Powered by MMDetection + Gradio* | Training Epoch: 3 | Resolution: 416x416")

if __name__ == "__main__":
    # Launch interface
    demo.launch(server_name="127.0.0.1", server_port=7860, show_api=False)
