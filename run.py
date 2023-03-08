from flask import Flask, render_template 
from datetime import *
import datetime

app = Flask(__name__)

def invertir_fecha(fecha):
    anyo = str(fecha.year)
    mes  = str(fecha.month)
    dia  = str(fecha.day)

    myfecha = (dia, mes, anyo)

    fecha = '-'.join(myfecha)
    return fecha
    

@app.route('/')
def index():
    
    # Recuperamos la fecha del día
    fecha_actual = fecha = date.today()
    
    # Calcular el lunes de la fecha actual
    primer_dia = fecha_actual - timedelta(days=fecha_actual.weekday() % 7)

    print ('Lunes: ', str(primer_dia))
    
    semana = []
    
    for day in range(0, 6):

        fecha = primer_dia + timedelta(days=day)
        fecha_invertida = invertir_fecha(fecha)        
        semana.append(fecha_invertida)
        
    
    return render_template('index.html', semana=semana)
    


if __name__ == '__main__':
    app.run(debug=True)