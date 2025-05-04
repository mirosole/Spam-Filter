---

# **Spam Filter** 📨🚫

## 📌 About the Project

This project is a **Python-based spam filter** that analyzes email text and classifies it as either **SPAM** or **OK**. The filter is trained using a labeled corpus and can then be used to classify new messages.

---

## 📂 Project Structure

📁 **The project consists of the following modules:**

* **`corpus.py`** — loads and processes email texts from a corpus.
* **`filter.py`** — core spam filter logic (text analysis and classification).
* **`confmat.py`** — computes the **confusion matrix** (True Positives, False Positives, etc.).
* **`quality.py`** — evaluates the filter’s performance using standard metrics.
* **`utils.py`** — helper functions (file I/O and utilities).

---

## 🎯 Main Features

✅ **Model training** based on a labeled email corpus
✅ **Analysis of new emails** to determine if they are spam
✅ **Basic NLP**: normalization, stop-word removal, and stemming
✅ **Performance metrics** calculation (accuracy, errors, etc.)

---

## 📜 Usage

### **Train the Filter**

```python
from filter import MyFilter

my_filter = MyFilter()
my_filter.train('path_to_training_corpus')
```

### **Test the Filter**

```python
my_filter.test('path_to_test_corpus')
```

### **Classify a Single Email**

```python
email_text = "You have won a free lottery! Claim your prize now!"
is_spam = my_filter.is_spam(email_text)
print("This is SPAM" if is_spam else "This is a normal email")
```

---

## ⚙️ Requirements

📌 Python 3.x
📌 Built-in libraries: **os, re, collections**

---

## 🚀 Development & Authors

👨‍💻 Developed as part of a university assignment.

---
