from django import forms
from django.utils import timezone
from datetime import datetime, time, timedelta
from .models import Visit

class VisitScheduleForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    time = forms.ChoiceField(choices=[], required=True, label="Hora (1 hora)")

    def __init__(self, *args, property_obj=None, selected_date=None, **kwargs):
        super().__init__(*args, **kwargs)

        tz = timezone.get_current_timezone()
        now_local = timezone.localtime(timezone.now())  # aware -> local
        today = now_local.date()

        # --- Día seleccionado ---
        if selected_date is None:
            selected_date = today

        # Inicializamos el campo fecha y forzamos min en el widget HTML:
        self.fields["date"].initial = selected_date
        self.fields["date"].widget.attrs["min"] = today.isoformat()

        # Ventana de trabajo
        FIRST_HOUR = 7            # 07:00
        LAST_START_HOUR = 19      # última franja 19:00–20:00

        # Si la fecha es pasada, no hay nada que mostrar
        if selected_date < today:
            self.fields["time"].choices = []
            return

        # Si es hoy: arrancamos desde la siguiente hora en punto
        if selected_date == today:
            start_hour = max(FIRST_HOUR, now_local.hour + 1)
        else:
            start_hour = FIRST_HOUR

        if start_hour > LAST_START_HOUR:
            self.fields["time"].choices = []
            return

        # --- Horas ya ocupadas ese día (en local) ---
        taken_hours = set()
        qs = (
            Visit.objects.filter(property=property_obj, date_time__date=selected_date)
            .exclude(status="cancelled")
            .values_list("date_time", flat=True)
        )
        for dt in qs:
            # Convertimos a hora local y nos quedamos SOLO con la hora
            local_hour = timezone.localtime(dt, tz).hour
            taken_hours.add(local_hour)

        # --- Construimos opciones (1 hora) ---
        choices = []
        for h in range(start_hour, LAST_START_HOUR + 1):
            if h in taken_hours:
                continue
            label = f"{h:02d}:00 - {h+1:02d}:00"
            value = f"{h:02d}:00"
            choices.append((value, label))

        self.fields["time"].choices = choices

    def clean(self):
        cleaned = super().clean()
        d = cleaned.get("date")
        t = cleaned.get("time")
        if not d or not t:
            return cleaned

        tz = timezone.get_current_timezone()

        # Armar el datetime local para la franja elegida
        hh, mm = [int(x) for x in t.split(":")]
        start_naive = datetime.combine(d, time(hh, mm))
        start_local = timezone.make_aware(start_naive, tz)

        # 1) Rechazar días pasados o horas pasadas
        if start_local <= timezone.localtime(timezone.now()):
            raise forms.ValidationError("La hora seleccionada ya pasó.")

        cleaned["date_time"] = start_local
        return cleaned




