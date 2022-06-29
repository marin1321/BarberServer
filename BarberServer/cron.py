from django_cron import CronJobBase, Schedule
import time
from datetime import datetime
from app.models import citas

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'    

    def do(self):
        hora = time.strftime("%H:%M:%Sq")
        fechaRegistroCita = datetime.today().strftime('%Y-%m-%d')
        CitaHora = citas.objects.all()
        print("-->"+CitaHora.idHorario.horaInicio)