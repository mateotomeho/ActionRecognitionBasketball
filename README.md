# 🏀 Basketball Action Recognition using R(2+1)D CNN

## 📌 Project Overview

This project builds a deep learning model capable of classifying key basketball actions from video clips. Leveraging advanced sports analytics and transfer learning, the model identifies **four primary actions**:

* **Pass**
* **Dribble**
* **Shoot**
* **Defense**

The final model uses a **fine-tuned R(2+1)D-18 architecture**, a powerful 3D CNN designed to capture motion and spatial structure across video frames.

---

## 🎯 Key Results

| Metric                  | Result                        |
| ----------------------- | ----------------------------- |
| **Final Model**         | Fine-Tuned R(2+1)D-18         |
| **Validation Accuracy** | **86.46%** (Best Epoch)       |
| **Test Accuracy**       | **81.96%**                    |
| **Target Classes**      | Pass, Dribble, Shoot, Defense |

---

## 🧠 Model Architecture

### **R(2+1)D-18 Backbone**

The backbone of this project is the **R(2+1)D (Residual 2D + 1D)** network:

* Factorizes traditional 3D convolutions into:

  * **2D spatial convolution** → learns court, players, shapes
  * **1D temporal convolution** → learns motion across frames
* Pre-trained on **Kinetics-400**, a large-scale video action dataset.

### **Input Format**

Each video is converted into:

```
16 RGB frames × 64×64 resolution
Tensor shape: [Batch, 3, 16, 64, 64]
```

### **Custom Classification Head**

After the R(2+1)D backbone, a custom fully connected head was implemented:

```
1024 → 512 → 4 (output classes)
Activation: ReLU
```

This allows the model to specialize in basketball-specific motions.

---

## 📂 Repository Structure

The repo is organized for clarity and reproducibility:

To be added soon...

---

## 📊 Dataset Details

* Source: **SpaceJam Basketball Action Dataset**
* Actions used: **pass, dribble, shoot, defense**
* Frames extracted: **593,456 total**
* Each video → 16–frame clip at 64×64
* For baseline: **grayscale inputs**
* For final model: **RGB inputs** (led to higher accuracy)

---

## 🚀 Training Summary

### Final Model Hyperparameters

* **Optimizer:** Adam
* **Learning Rate:** 1e-4
* **Batch Size:** 8
* **Epochs:** 20
* **Loss Function:** Cross-Entropy
* **Training Strategy:** Full fine-tuning (all layers unfrozen)

---

## 📈 Performance

* The R(2+1)D model outperformed the baseline 3D CNN by **+19% absolute accuracy**.
* RGB frames improved motion/ball detection compared to grayscale.
* High F1 scores across all classes (≥82%).

---

## 📥 Demo 

Two game clips (one shooting, one dribbling) were tested:

* Shoot → **96.77% confidence**
* Dribble → **99.74% confidence**

---
