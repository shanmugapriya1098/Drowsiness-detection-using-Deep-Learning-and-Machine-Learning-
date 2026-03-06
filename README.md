# Drowsiness Detection using Deep Learning and Machine Learning

This repository contains a project that detects driver drowsiness using both **Machine Learning** and **Deep Learning** approaches in Python. The system leverages computer vision techniques to monitor eye activity and trigger alerts when signs of drowsiness are detected.


## 📌 Features
- Real-time drowsiness detection using webcam input.
- Two approaches implemented:
  - **Machine Learning** (traditional classifiers).
  - **Deep Learning** (CNN-based models).
- Haar Cascade classifiers for face and eye detection.
- Alarm sound (`alarm.wav`) to alert the driver when drowsiness is detected.
- Scripts for model training, evaluation, and deployment.
- Utility scripts for:
  - File retrieval and cloud bucket upload.
  - Screen recording and server streaming.


## 📂 Project Structure
```
driver-drowsiness-detection/
│
├── haar_cascade_files/          # Haar cascade XML files for face/eye detection
│   ├── haarcascade_frontalface_alt.xml
│   ├── haarcascade_lefteye_2splits.xml
│   └── haarcascade_righteye_2splits.xml
│
├── models/                      # Pre-trained and custom-trained models
│   ├── model.h5
│   └── model2.h5
│
├── alarm.wav                                # Alert sound file
├── machine_learning.jpg                     # Output image file
├── driver-drowsiness.py                     # 🚗 Main script (Deep Learning)
├── driver-drowsiness by machine learning.py # 🤖 ML-based implementation
├── deep learning-fast.py                    # ⚡ Optimized deep learning
├── em.py                                    # 😴 Emotion/drowsiness detection
├── serverstream.py                          # 🌐 Server streaming utility
├── README.md                                # Project documentation
└── project_requirements.txt                         # 📦 Python dependencies
```

## ⚙️ Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/shanmugapriya1098/Drowsiness-detection-using-Deep-Learning-and-Machine-Learning-.git
   cd Drowsiness-detection-using-Deep-Learning-and-Machine-Learning-
2. Install dependencies:
'''bash
  pip install -r project_requirements.txt
3. Ensure you have a working webcam connected.
🚀 Usage
1. Run the deep learning implementation:
'''bash
  python deep\ learning-fast.py
2. Run the machine learning implementation:

'''bash
  python driver-drowsiness\ by\ machine\ learning.py
3. Run the main detection script:
'''bash
  python driver-drowsiness.py
When drowsiness is detected, the system will play an alarm sound (alarm.wav) to alert the driver.


## 🧠 Technologies Used
Python
- OpenCV (for image processing and Haar cascades)
- TensorFlow/Keras (for deep learning models)
- Scikit-learn (for machine learning models)
- NumPy, Pandas (data handling)
- Matplotlib/Seaborn (visualization)

  
## 📈 Future Improvements
- Integration with IoT devices for real-time vehicle alerts.
- Deployment as a mobile/desktop application.

  
## 👩‍💻 Author
Developed by shanmugapriya1098 (github.com in Bing)


## ⚡ Output 
<p align="center">
  <img src="machine_learning.jpg" oncontextmenu="return false;" width="50%" alt="Output image" />
</p>

