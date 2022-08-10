import time
from datetime import datetime
from app.models import citas, horarios

class MyCronJob():
    hora = time.strftime("%H:%M:%Sq")
    hora = str(hora)
    fecha = datetime.today().strftime('%Y-%m-%d')
    allCitas =  citas.objects.filter(peticion = "pendiente")
    allHorarios = horarios.objects.filter(estado = "activo")
    for h in allHorarios:
        horarioid = horarios.objects.get(id=h.id)
        tiempoFecha = h.fecha
        fAñosHorarios = int(tiempoFecha.year)
        fMesesHorarios = int(tiempoFecha.month)
        fDiasHorarios = int(tiempoFecha.day)
        if fAñosHorarios == int(fecha[0:4]):
            if fMesesHorarios == int(fecha[5:7]):
                if fDiasHorarios < int(fecha[8:10]):
                    horarioid.estado = "inactivo"
            else:
                restaMesesHorarios = fMesesHorarios - int(fecha[5:7])
                if restaMesesHorarios < 0:
                    horarioid.estado = "inactivo"
        else:
            restaAñosHorarios = fAñosHorarios - int(fecha[0:4])
            if restaAñosHorarios < 0:
                horarioid.estado = "inactivo" 
        horarioid.save()
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
        else:
            if int(fecha[0:4]) == int(fechaHorario.year):
                if int(fecha[5:7]) == int(fechaHorario.month):
                    if int(fecha[8:10]) > int(fechaHorario.days):
                        cita.peticion = "cancelada"
                else:
                    restaMeses = int(fechaHorario.month) - int(fecha[5:7]) 
                    if restaMeses < 0:
                        cita.peticion = "cancelada"
                
            elif  int(fecha[0:4]) >= int(fechaHorario.year):
                cita.peticion = "cancelada"
        cita.save()
            

