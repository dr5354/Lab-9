# Импорт модулей Flask, SQLAlchemy и datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Инициализация Flask-приложения и настройка базы данных SQLite
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visits.db'
db = SQLAlchemy(app)

# Модель Visit для таблицы в базе данных
class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    town = db.Column(db.String(80), nullable=False)
    visit_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Visit: {self.town} on {self.visit_date}>"

# Создание таблиц в базе данных
with app.app_context():
    db.create_all()

# Маршрут для главной страницы, обрабатывает GET и POST запросы
@app.route('/', methods=['GET', 'POST'])
def index():
    # Обработка POST-запроса
    if request.method == 'POST':
        # Добавление нового посещения
        if 'add_visit' in request.form:
            town = request.form['town']
            try:
                visit_date = datetime.strptime(request.form['visit_date'], '%Y-%m-%d').date()
                new_visit = Visit(town=town, visit_date=visit_date)
                db.session.add(new_visit)
                db.session.commit()
                return redirect(url_for('index'))
            except ValueError:
                error = "Некорректный формат даты (ГГГГ-ММ-ДД)"
                visits = Visit.query.all()
                return render_template('index.html', visits=visits, error=error)
        # Очистка всех записей
        elif 'clear_all' in request.form:
            db.session.query(Visit).delete()
            db.session.commit()
            return redirect(url_for('index'))

    # Отображение списка посещений для GET-запроса
    visits = Visit.query.all()
    return render_template('index.html', visits=visits)

# Запуск приложения в режиме отладки
if __name__ == '__main__':
    app.run(debug=True)