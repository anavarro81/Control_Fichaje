from flask import Flask, render_template, request
from datetime import datetime, timedelta
import locale
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

app = Flask(__name__)


def invertir_fecha(fecha):
    anyo = str(fecha.year)
    mes = str(fecha.month)
    dia = str(fecha.day)

    myfecha = (dia, mes, anyo)

    fecha = '-'.join(myfecha)
    return fecha


def get_weekdays(week):
    # Convertir la semana en formato 'YYYY-WW' a una fecha
    year, week_num = map(int, week.split('-W'))
    date = datetime.strptime(f'{year}-W{week_num}-1', '%Y-W%W-%w')

    # Obtener el día de la semana como un número (0 es lunes, 6 es domingo)
    weekday = date.weekday()

    # Restar días para obtener el primer día de la semana (lunes)
    start_of_week = date - timedelta(days=weekday)

    # Crear una lista vacía para almacenar los días de lunes a viernes
    weekdays = []

    # Iterar por los próximos 5 días para obtener los días de lunes a viernes
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        weekdays.append(day.strftime('%A: %d-%m-%Y').capitalize())

    return weekdays


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        hora_entrada = request.form['hora_entrada']
        hora_salida = request.form['hora_salida']

        # Convertir las horas de entrada y salida a objetos de fecha y hora
        dt_entrada = datetime.strptime(hora_entrada, '%H:%M')
        dt_salida = datetime.strptime(hora_salida, '%H:%M')

        # Calcular la diferencia de tiempo entre las dos horas
        tiempo_transcurrido = dt_salida - dt_entrada

        # Formatear la diferencia de tiempo como HH:mm
        tiempo_formateado = str(tiempo_transcurrido).split('.')[0]

        return render_template('index.html', tiempo_formateado=tiempo_formateado)

     # ejemplo de fecha
    fecha = datetime.today()
    numero_semana = fecha.isocalendar()[1]
    anyo = fecha.year

    # convertir a formato 'YYYY-WW'
    week = f'{anyo}-W{numero_semana:02d}'
    print(week)
    weekdays = get_weekdays(week)

    print(weekdays)

    return render_template('index.html', semana=weekdays, fecha=week)


@app.route('/semana', methods=['GET', 'POST'])
def mostrar_semana():

    week = request.args.get('week')

    # year, week_num = map(int, week.split('-W'))
    # fecha = datetime.strptime(f'{year}-W{week_num}-1', '%Y-W%W-%w')

    # fecha_week = datetime.strptime(fecha, '%Y-%m-%d')
    weekdays = get_weekdays(week)

    return render_template('index.html', semana=weekdays, fecha=week)


if __name__ == '__main__':
    app.run(debug=True)
