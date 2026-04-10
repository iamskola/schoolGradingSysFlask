from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_grade(score):
    if score >= 70:
        return 'A', 'Excellent'
    elif score >= 60:
        return 'B', 'Very Good'
    elif score >= 50:
        return 'C', 'Good'
    elif score >= 45:
        return 'D', 'Needs Improvement'
    elif score >= 40:
        return 'E', 'Urgent Assistance Needed'
    else:
        return 'F', 'Consider Strong Academic Intervention'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    try:
        name = request.form.get('name')
        level = request.form.get('level')

        # Collect subjects
        subjects = {
            "Math": request.form.get('math'),
            "English": request.form.get('english'),
            "Science": request.form.get('science'),
            "Social": request.form.get('social'),
            "Civic": request.form.get('civic'),
            "Agric": request.form.get('agric'),
            "C R S": request.form.get('crs'),
            "CCA": request.form.get('cca'),
            "Business": request.form.get('business'),
            "Computer": request.form.get('computer'),
            "Economics": request.form.get('economics'),
        }

        # Check for empty fields
        if not name  or level or any(v == '' or v is None for v in subjects.values()):
            return render_template('index.html', error="All fields are required!")

        # Convert to integers safely
        scores = {}
        for subject, value in subjects.items():
            try:
                score = int(value)
                if score < 0 or score > 100:
                    return render_template('index.html', error=f"{subject} must be between 0 and 100")
                scores[subject] = score
            except ValueError:
                return render_template('index.html', error=f"{subject} must be a number")

        total = sum(scores.values())
        average = round(total / len(scores), 2)

        grade, remark = calculate_grade(average)

        return render_template('result.html',
                               name=name,
                               level=level,
                               scores=scores,
                               total=total,
                               average=average,
                               grade=grade,
                               remark=remark)

    except Exception as e:
        return render_template('index.html', error="Something went wrong. Please try again.")

if __name__ == '__main__':
    app.run()