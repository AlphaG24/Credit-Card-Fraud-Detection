# Evaluation Report – Credit Card Fraud Detection System

## 1. Problem Definition
Credit card fraud accounts for only 0.17% of transactions, making it a highly imbalanced classification problem.  
The goal is to build an accurate fraud detection system that:

- Works in real time  
- Handles the imbalance effectively  
- Provides explainable predictions  
- Supports bulk fraud analysis  
- Is deployable on cloud platforms  

---

## 2. Dataset Overview
Dataset: **European Credit Card Fraud (2013)**  
Source: Kaggle  
Rows: 284,807  
Fraud: 492 (0.172%)  
Features: Time, Amount, V1–V28 (PCA components)

Dataset is **not included** in the repository because:
- It is large
- It is not needed for deployment
- Only used during training

---

## 3. Model Benchmarking & Comparison

### Models Evaluated
| Model | Pros | Cons |
|-------|------|------|
| Logistic Regression | Very fast | Fails to capture PCA fraud relations |
| Random Forest | Good non-linear learning | Heavy; slower inference |
| LightGBM | Fast and accurate | Overfits small fraud classes |
| **XGBoost (Selected)** | Best recall, best fraud detection | Requires tuning |

### Why XGBoost Won
- Best in handling imbalanced data  
- Strong performance on PCA data  
- Excellent fraud recall  
- Lightweight and fast inference  
- Tunable with scale_pos_weight  

---

## 4. Training Strategy

### Imbalance Handling

scale_pos_weight = negatives / positives


### Decision Threshold


fraud = probability >= 0.20


### Preprocessing
- No scaling (PCA is already normalized)
- Missing values filled with zeros
- No outlier removal (fraud signals might be outliers)

---

## 5. System Architecture
- **FastAPI backend**  
- **Interactive HTML/CSS/JS frontend**  
- **Single + Bulk predictions**  
- **XGBoost model (.pkl)**  
- **Dockerized deployment**  
- **Hosted on Render**  
  https://credit-card-fraud-detection-1nll.onrender.com

---

## 6. Evaluation Metrics

| Metric | Score |
|--------|--------|
| Accuracy | ~99.8% |
| Fraud Recall | ~84% |
| Fraud Precision | ~86% |
| ROC-AUC | 0.977 |

Explanation:
- Accuracy is deceptive due to imbalance  
- Fraud recall and precision matter most  
- Chosen threshold gives best balance  

---

## 7. Limitations
- PCA features cannot be manually created  
- Fraud predictions require real PCA signatures  
- Manual/random input → almost always NOT fraud  
- Dataset imbalance limits synthetic detection  

---

## 8. Conclusion
This project delivers:

- A production-ready fraud detection system  
- Real-time predictions via FastAPI  
- Bulk CSV fraud scoring  
- Explainability via top features  
- Cloud deployment using Docker + Render  
- Best-performing model based on comparison  

This meets all evaluation criteria for the AI capstone proje