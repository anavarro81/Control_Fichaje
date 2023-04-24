from flask import Flask, render_template, request
from datetime import datetime, timedelta, time
from util import get_current_week, get_week
from config import config
from flask_mysqldb import MySQL
from modelos.ModelFichaje import modelFichaje

import locale

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

app = Flask(__name__)
bd = MySQL(app)

star_day = time(7, 0, 0)

wrong_entry_time = "La hora de entrada no puede ser anterior a las 7:00"


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/week", methods=["GET", "POST"])
def show_weerk():
    week = request.args.get("week")
    source = request.args.get("source")
    enable_days = True

    # En funcion desde donde se llame se habilita o no la edición.
    if source == "resultados":
        enable_days = False

    week = get_week(week, enable_days, bd)

    return render_template("resultado.html", week=week, source=source)


@app.route("/clock_in", methods=["GET", "POST"])
def fichar():
    today_date = datetime.now()
    clock_in_time = today_date.time()
    message = ""
    edit_days = False

    if clock_in_time < star_day:
        message = wrong_entry_time
        return render_template("error.html", message=message)

    today_date_str = today_date.strftime(("%Y-%m-%d"))
    clock_in_time_str = clock_in_time.strftime("%H:%M")

    # Devuelve una tupla con los datos del fichaje (fecha, hora entrada, hora salida y comentario)
    clockin = modelFichaje.check_date(today_date_str, bd)

    # Si ha encontrado la fecha en la BBDD (¡Ya se ha fichado hoy!)
    # Se informa la de salida.
    if clockin != None:
        modelFichaje.update_clock_in(bd, today_date_str, h_salida=clock_in_time_str)
    else:
        modelFichaje.insert_new_day(bd, today_date_str)
        modelFichaje.update_clock_in(bd, today_date_str, h_entrada=clock_in_time_str)

    current_week = get_current_week()
    week = get_week(current_week, edit_days, bd)

    return render_template(
        "resultado.html", week=week, fecha=current_week, source="clock_in"
    )


@app.route("/declare presence", methods=["GET", "POST"])
def declare_presence():
    current_week = get_current_week()
    edit_days = True
    week = get_week(current_week, edit_days, bd)
    select_date = True

    return render_template(
        "resultado.html",
        week=week,
        fecha=current_week,
        select_date=select_date,
        source="declare_presence",
    )


@app.route("/results", methods=["GET", "POST"])
def results():
    current_week = get_current_week()
    edit_days = False
    week = get_week(current_week, edit_days, bd)
    select_date = True

    return render_template(
        "resultado.html",
        week=week,
        fecha=current_week,
        select_date=True,
        source="results",
    )


@app.route("/validate", methods=["GET", "POST"])
def validate():
    for elem in request.form.keys():
        date_str = elem[0:10]
        sufix = elem[10:]
        elem = date_str + sufix

        # Converite el string de la fecha de la tabla HTML a fotmato datetime.
        dt_ddmmaaaa = datetime.strptime(date_str, "%d-%m-%Y")

        # Dia de la semana en formato dd-mm-yyyy. Ejemplo: 2023-04-04
        f_str_yymmdd = dt_ddmmaaaa.strftime("%Y-%m-%d")

        # Consultamos si existe esa fecha en bbdd.
        clockin = modelFichaje.check_date(f_str_yymmdd, bd)

        if clockin == None:
            modelFichaje.insert_new_day(bd, date_str[::-1])

        if sufix == "_h_ent":
            modelFichaje.update_clock_in(bd, f_str_yymmdd, h_entrada=request.form[elem])
        elif sufix == "_h_sal":
            modelFichaje.update_clock_in(bd, f_str_yymmdd, h_salida=request.form[elem])
        else:
            modelFichaje.update_clock_in(
                bd, f_str_yymmdd, comentario=request.form[elem]
            )

    current_week = get_current_week()
    edit_days = True
    week = get_week(current_week, edit_days, bd)
    select_date = True

    return render_template(
        "resultado.html",
        week=week,
        fecha=current_week,
        select_date=select_date,
        source="declare presence",
    )


if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.run()
