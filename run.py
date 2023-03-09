from flask import Flask, render_template
from datetime import *
import datetime

app = Flask(__name__)


def invertir_fecha(fecha):
    anyo = str(fecha.year)
    mes = str(fecha.month)
    dia = str(fecha.day)

    myfecha = (dia, mes, anyo)

    fecha = '-'.join(myfecha)
    return fecha


def get_weekdays(today):
    # Obtener el día de la semana como un número (0 es lunes, 6 es domingo)
    weekday = today.weekday()

    # Restar días para obtener el primer día de la semana (lunes)
    start_of_week = today - datetime.timedelta(days=weekday)

    # Crear una lista vacía para almacenar los días de lunes a viernes
    weekdays = []

    # Iterar por los próximos 5 días para obtener los días de lunes a viernes
    for i in range(5):
        day = start_of_week + datetime.timedelta(days=i)
        weekdays.append(day.strftime('%A: %Y-%m-%d'))

    return weekdays


@app.route('/')
def index():

    semana = []

    # Recuperamos la fecha del día
    fecha_actual = fecha = date.today()

    # Calcular el lunes de la fecha actual
    primer_dia = fecha_actual - timedelta(days=fecha_actual.weekday() % 7)

    for day in range(0, 7):

        fecha = primer_dia + timedelta(days=day)
        fecha_invertida = invertir_fecha(fecha)
        semana.append(fecha_invertida)
        print(semana)

    weekdays = get_weekdays(datetime.date.today())
    print(weekdays)

    return render_template('index.html', semana=weekdays)


if __name__ == '__main__':
    app.run(debug=True)
