# 🛡️ AI-Powered Security Threat Detection in X-Ray Scans(TEAM BIT BANDITS)

![Status](https://img.shields.io/badge/Status-Prototype_Complete-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Framework](https://img.shields.io/badge/Framework-MMDetection-red?style=for-the-badge)
![UI](https://img.shields.io/badge/Interface-Gradio-orange?style=for-the-badge)

> **Welcome to our Security Baggage Scanner AI!** This project automates the critical task of identifying concealed threats—specifically **Guns** and **Knives**—in baggage X-ray images to enhance public safety and dramatically reduce human error.

---

## 🎥 Project Demonstration
*(Click the image below to watch our 2-Minute Demo Video on YouTube)*

[![Project Demo Video](https://via.placeholder.com/800x400.png?text=Watch+Demo)](https://drive.google.com/file/d/14gV4YRkszi9vaT26Icj4Tkhp_q4IJR3R/view?usp=sharing)


---

## ✨ Key Features
- **Real-Time Threat Detection**: Instantly analyzes X-Ray imaging for dangerous concealed objects.
- **High-Fidelity Tracking**: Powered by a **Cascade Mask R-CNN (ResNet-50)** deep learning architecture for superior accuracy in messy, overlapping baggage environments.
- **Professional Web Interface**: Built with Gradio to ensure security personnel can upload scans and make split-second decisions easily.
- **Color-Coded Intelligence**: Threat categories are heavily color-coded (🟩 Knives, 🟥 Guns) alongside automated confidence scores.

---

## 📊 Dataset & The "Road to Production"
To swiftly build this **functioning proof-of-concept prototype**, we trained the AI on a highly-focused subset consisting of exactly **4,000 images** (heavily weighted towards knives). 

While the knife detection is highly accurate today, we fully acknowledge that the gun detection algorithms are still actively scaling. **However, we are already prepared for Phase 2.**

### 🚀 The 30,000 Image Future
We have successfully processed, filtered, and labeled a massive, high-quality production dataset of **nearly 30,000 X-ray images**. The immediate future scope of this project is executing the training across this entire massive dataset. This will dramatically maximize the detection accuracy across all threat categories and elevate the project into a highly robust, enterprise-ready utility.

---

## ⚙️ Installation & Usage

### 1. Prerequisites
Ensure you have Python 3.8+ installed along with PyTorch. 

### 2. Install Dependencies
```bash
pip install torch torchvision
pip install -r requirements.txt
pip install gradio opencv-python numpy
```

### 3. Model Weights
Due to file size constraints, the `.pth` weights for the neural network are hosted externally.
- Download `epoch_3.pth` from [Google Drive Link Here](#).
- Place it inside the `work_dirs/fast_train_gun_knife/` directory.

### 4. Run the Interface
To start the Gradio web interface, simply run:
```bash
python app.py
```
Then navigate to `http://127.0.0.1:7860/` in your web browser to upload images and test the AI!

---

## 🤝 Acknowledgments
This prototype was developed as part of our endeavor to build smarter, safer public infrastructure. Thank you to the judges and reviewers for your time!
