import calendar
import datetime

ano_atual = datetime.datetime.now().year
mes_atual = datetime.datetime.now().month

semanas_do_mes_atual = calendar.monthcalendar(ano_atual, mes_atual)

print(semanas_do_mes_atual)