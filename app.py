from flask import Flask, request, jsonify
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

app = Flask(__name__)

df = pd.read_csv('datasets/questions.csv')

risk_df = pd.read_csv(
    'datasets/risk_training.csv'
)
X = risk_df[
    ['accuracy','category_score']
]

y = risk_df['risk']

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = GradientBoostingClassifier()

model.fit(
    X_train,
    y_train
)
# TRAINING DATA

X = np.array([
    [90,2],
    [80,3],
    [40,8],
    [30,10]
])

y = np.array([
    0,
    0,
    1,
    1
])

model = GradientBoostingClassifier()
model.fit(X,y)

# ROUTES

@app.route('/')
def home():
    return jsonify({
        "message": "Dyscalculia Engine Running"
    })

@app.route('/questions/<category>/<age_group>/<int:count>')
def get_questions(category, age_group, count):

    filtered = df[
        (df['category'] == category) &
        (df['age_group'] == age_group)
    ]

    sample = filtered.sample(
        min(count, len(filtered))
    )

    student_view = sample.drop(
        columns=['answer']
    )

    result = student_view.to_dict(
        orient='records'
    )

    return jsonify(result)

@app.route('/submit', methods=['POST'])
def submit():

    data = request.json
    score = 0

    for item in data["answers"]:

        qid = item["question_id"]
        selected = item["selected"]

        for cat in questions.values():

            for q in cat:

                if q["id"] == qid:

                    if selected == q["answer"]:
                        score += 1

    accuracy = (score / len(data["answers"])) * 100
    avg_time = data["avg_time"]

    prediction = model.predict([[accuracy, avg_time]])

    risk = "Low Risk"

    if prediction[0] == 1:
        risk = "At Risk"

    return jsonify({
        "score": score,
        "accuracy": accuracy,
        "risk": risk
    })
@app.route('/submit_demo')
def submit_demo():

    answers = [
        {
            "question":"2+2=?",
            "selected":"4"
        },
        {
            "question":"5+3=?",
            "selected":"7"
        }
    ]

    score = 0
    total = len(answers)

    for item in answers:

        question = item["question"]
        selected = str(item["selected"])

        correct = df[
            df['question'] == question
        ]['answer'].values

        if len(correct) > 0:

            if selected == str(correct[0]):
                score += 1

    accuracy = (
        score / total
    ) * 100
    attempts = pd.read_csv(
        'datasets/attempts.csv'
    )

    new_attempt = pd.DataFrame([
        {
            "student":"demo_student",
            "category":"arithmetic",
            "accuracy":accuracy
        }
    ])

    attempts = pd.concat(
        [attempts, new_attempt],
        ignore_index=True
    )

    attempts.to_csv(
        'datasets/attempts.csv',
        index=False
    )

    return jsonify({
        "score": score,
        "total": total,
        "accuracy": accuracy
    })

@app.route('/progress_demo')
def progress_demo():

        attempts = pd.read_csv(
            'datasets/attempts.csv'
        )

        student_attempts = attempts[
            attempts['student']
            == 'demo_student'
        ]

        scores = student_attempts[
            'accuracy'
        ].tolist()

        if len(scores) < 2:

            status = "Need More Attempts"

        else:

            if scores[-1] > scores[-2]:
                status = "Improving"

            elif scores[-1] == scores[-2]:
                status = "Stable"

            else:
                status = "Needs Help"

        return jsonify({
            "attempts": scores,
            "status": status
        })
@app.route('/submit')
def submit_real():

    answers = [
        {
            "question":"2+2=?",
            "selected":"4"
        },
        {
            "question":"5+3=?",
            "selected":"8"
        },
        {
            "question":"7-2=?",
            "selected":"4"
        }
    ]

    score = 0
    total = len(answers)

    for item in answers:

        question = item['question']
        selected = str(item['selected'])

        correct = df[
            df['question'] == question
        ]['answer'].values

        if len(correct) > 0:

            if selected == str(correct[0]):
                score += 1

    accuracy = (
        score / total
    ) * 100

    attempts = pd.read_csv(
        'datasets/attempts.csv'
    )

    new_attempt = pd.DataFrame([
        {
            "student":"demo_student",
            "category":"mixed",
            "accuracy":accuracy
        }
    ])

    attempts = pd.concat(
        [attempts, new_attempt],
        ignore_index=True
    )

    attempts.to_csv(
        'datasets/attempts.csv',
        index=False
    )
    category_score = accuracy

    prediction = model.predict([
        [accuracy, category_score]
    ])  

    risk_map = {
        0:"Low Risk",
        1:"At Risk",
        2:"High Risk"
    }

    risk = risk_map[
        prediction[0]
    ]

    return jsonify({
        "score":score,
        "total":total,
        "accuracy":accuracy,
        "risk":risk
    })
@app.route('/category_demo')
def category_demo():

    answers = [
        {
            "question":"2+2=?",
            "selected":"4"
        },
        {
            "question":"5+3=?",
            "selected":"7"
        },
        {
            "question":"2 4 6 __",
            "selected":"8"
        }
    ]

    category_scores = {}

    for item in answers:

        question = item['question']
        selected = str(item['selected'])

        row = df[
            df['question'] == question
        ]

        if len(row) > 0:

            category = row.iloc[0]['category']
            correct = str(
                row.iloc[0]['answer']
            )

            if category not in category_scores:

                category_scores[
                    category
                ] = {
                    "correct":0,
                    "total":0
                }

            category_scores[
                category
            ]['total'] += 1

            if selected == correct:

                category_scores[
                    category
                ]['correct'] += 1

    performance = {}

    for cat, data in category_scores.items():

        accuracy = (
            data['correct']
            /
            data['total']
        ) * 100

        performance[cat] = accuracy

    return jsonify(
        performance
    )
@app.route('/predict_demo')
def predict_demo():

    accuracy = 65
    category_score = 60

    prediction = model.predict([
        [accuracy, category_score]
    ])

    risk_map = {
        0:"Low Risk",
        1:"At Risk",
        2:"High Risk"
    }

    risk = risk_map[
        prediction[0]
    ]

    return jsonify({
        "accuracy":accuracy,
        "category_score":category_score,
        "risk":risk
    })
if __name__ == '__main__':
    app.run(debug=True)