import time
from datetime import datetime
from app.models import citas

class MyCronJob():
    hora = time.strftime("%H:%M:%Sq")
    hora = str(hora)
    fecha = datetime.today().strftime('%Y-%m-%d')
    allCitas =  citas.objects.filter(peticion = "activo")
    for c in allCitas:
        cita = citas.objects.get(id=c.id)
        horaHorario = c.idHorario.horaInicio
        fechaHorario = c.idHorario.fecha
        if fecha == fechaHorario:
            horasHorario = int(horaHorario[0:2])
            horas = int(hora[0:2])
            minutosHorarios  =  int(horaHorario[3:5])
            minutos =  int(hora[3:5])
            if horas>horasHorario:
                if minutosHorarios > 20:
                    cita.peticion = "cancelada"
                else:
                    faltante = 60 - minutos 
                    sumaMinutos = faltante + minutosHorarios
                    if sumaMinutos > 20:
                        cita.peticion = "cancelada"
            elif horas == horasHorario:
                restaMinutos = minutosHorarios - minutos
                if restaMinutos < 20: 
                    cita.peticion = "cancelada"
        cita.save()
            

