from datetime import datetime, timedelta
from flask import render_template, request
from modelos.ModelFichaje import modelFichaje


dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
formato_hhmmss = "%H:%M"


def get_current_week():
    """
    Get the current week of the year to show by default.

    """
    fecha = datetime.today()
    numero_semana = fecha.isocalendar()[1]
    anyo = fecha.year
    # convertir a formato 'YYYY-WW'
    week = f"{anyo}-W{numero_semana:02d}"
    return week


def get_week(week, hab_dias, bd):
    """
    Return the full week from a given week of the year.
    """

    year, week_num = map(int, week.split("-W"))
    inicio_semana = datetime.strptime(f"{year}-{week_num}-1", "%Y-%W-%w").date()
    fecha_hoy = datetime.now().date()

    # Se crea el diccionario de la semana en vacio.
    semana_dict = dict()

    for i in range(7):
        dia = inicio_semana + timedelta(days=i)
        # dia_date = dia.date()
        fecha_str = dia.strftime("%d-%m-%Y")

        # Se crea un diccionario con los valores inciales de hora de entrada/salida y comentario.
        # La clave {fecha_str} es la fecha del dia de la semana.
        dict_val_iniciales = {
            fecha_str: {
                "id": "",
                "day_week": "",
                "hora_entrada": "00:00",
                "hora_salida": "00:00",
                "horas_jornada": "",
                "comentario": "",
                "habilitado": "disabled",
            }
        }

        # Agrega el diccionario con los valores inciales al de la semana.
        # Se inserta la fecha (clave) con los valores por defecto
        semana_dict.update(dict_val_iniciales)

        # Se informa el dia de la semana "Lunes, Martes, Miercoles..." a partir de los
        # datos de la lista: dias_semana.
        semana_dict[fecha_str]["day_week"] = dias_semana[i]
        semana_dict[fecha_str]["id"] = dias_semana[i][0:3]

        ##----->>

        if dia <= fecha_hoy:
            if hab_dias:
                semana_dict[fecha_str]["habilitado"] = ""

            fichaje = modelFichaje.check_date(dia, bd)

            if fichaje != None:
                fecha_bd, h_entrada_bd, h_salida_bd, comentario_bd = fichaje

                h_entrada_bd_str = str(h_entrada_bd)
                h_salida_bd_str = str(h_salida_bd)

                # Si la hora en bbdd es anterior a las 10:00, se muestra en pantalla como "--:--"
                # En esos casos se calcula la longitud y se completa con un cero a la izquierda,
                # ejemplo "7:30" (len=7) -> "07:30" (len=8)

                if len(h_entrada_bd_str) == 7:
                    h_entrada_bd_str = "0" + h_entrada_bd_str

                if len(h_salida_bd_str) == 7:
                    h_salida_bd_str = "0" + h_salida_bd_str

                print(f"h_entrada_str = {h_entrada_bd_str}")

                semana_dict[fecha_str]["hora_entrada"] = h_entrada_bd_str
                semana_dict[fecha_str]["hora_salida"] = h_salida_bd_str
                semana_dict[fecha_str]["comentario"] = comentario_bd

                # dt_h_entrada = datetime.strptime(h_entrada_bd, formato_hhmmss)
                # dt_h_salida  = datetime.strptime(bbdd_fechas[fecha_str]['h_salida'], formato_hhmmss)

                dt_h_entrada = h_entrada_bd
                dt_h_salida = h_salida_bd

                horas_dia = dt_h_salida - dt_h_entrada

                horas = horas_dia / timedelta(hours=1)

                # Si la diferencia de horas es negativa, no lo muestro en la tabla HTMl.
                if horas > 0:
                    horas_dia = str(dt_h_salida - dt_h_entrada)
                    semana_dict[fecha_str]["horas_jornada"] = horas_dia

    return semana_dict
