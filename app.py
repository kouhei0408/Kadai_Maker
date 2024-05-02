from flask import Flask, render_template, request
import calendar

app = Flask(__name__)

subjects = ['国語', '数学', '理科', '社会', '英語']

def generate_schedule(start_date, end_date, increase_day, decrease_day):
    schedule = []
    current_date = start_date
    while current_date <= end_date:
        day_of_week = current_date.weekday()  # 0:月曜日, 1:火曜日, ..., 6:日曜日
        tasks = {subject: 1 for subject in subjects}  # デフォルトで全ての教科に1つずつの課題を設定
        if day_of_week in increase_day:
            for subject in subjects:
                tasks[subject] += 1  # 指定された曜日の課題数を増やす
        if day_of_week in decrease_day:
            for subject in subjects:
                tasks[subject] -= 1  # 指定された曜日の課題数を減らす
        schedule.append((current_date, tasks))
        current_date = current_date + timedelta(days=1)
    return schedule

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        increase_day = [int(day) for day in request.form.getlist('increase_day')]
        decrease_day = [int(day) for day in request.form.getlist('decrease_day')]
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        schedule = generate_schedule(start_date, end_date, increase_day, decrease_day)
        return render_template('schedule.html', schedule=schedule)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
