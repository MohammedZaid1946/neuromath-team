Dyscalculia Risk Classification Engine

Overview
This project is a Flask-based prototype for dyscalculia cognitive assessment and risk prediction.

Current Features
- Flask backend
- Question API
- Arithmetic questions
- Sequence questions
- Answer checking
- Accuracy calculation
- Demo Gradient Boosting risk prediction

Routes

1. Home Route
/

Purpose:
Shows whether the Flask engine is running.

Example:
http://127.0.0.1:5000/

2. Arithmetic Questions
/questions/arithmetic

Purpose:
Returns arithmetic questions in JSON format.

Example:
http://127.0.0.1:5000/questions/arithmetic

3. Sequence Questions
/questions/sequence

Purpose:
Returns sequence questions.

Example:
http://127.0.0.1:5000/questions/sequence

4. Demo Prediction
/demo

Purpose:
Runs a demo submission and predicts:

- Score
- Accuracy
- Risk level

Technologies Used
- Python
- Flask
- NumPy
- Scikit-learn
- Gradient Boosting Classifier

Current Status
Prototype / Demo Engine

Future Work
- Real dataset integration
- Adaptive difficulty
- Cognitive profiling
- Real dyscalculia risk model
- Database integration

How To Run

1. Install packages:

pip install flask scikit-learn numpy

2. Run:

python app.py

3. Open browser and test routes.