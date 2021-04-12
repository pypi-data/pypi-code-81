from dateutil.relativedelta import relativedelta
from edc_visit_schedule import (
    Crf,
    FormsCollection,
    Schedule,
    Visit,
    VisitSchedule,
    site_visit_schedules,
)

crfs_baseline = FormsCollection(
    Crf(show_order=100, model="respond_test_app.clinicalreviewbaseline"),
    Crf(show_order=120, model="respond_test_app.hivinitialreview", required=False),
    Crf(show_order=130, model="respond_test_app.dminitialreview", required=False),
    Crf(show_order=140, model="respond_test_app.htninitialreview", required=False),
    Crf(show_order=150, model="respond_test_app.cholinitialreview", required=False),
    Crf(show_order=160, model="respond_test_app.hivreview", required=False),
    Crf(show_order=170, model="respond_test_app.dmreview", required=False),
    Crf(show_order=180, model="respond_test_app.htnreview", required=False),
    Crf(show_order=190, model="respond_test_app.cholreview", required=False),
    Crf(show_order=200, model="respond_test_app.medications", required=False),
)

crfs_followup = FormsCollection(
    Crf(show_order=100, model="respond_test_app.clinicalreview"),
    Crf(show_order=120, model="respond_test_app.hivinitialreview", required=False),
    Crf(show_order=130, model="respond_test_app.dminitialreview", required=False),
    Crf(show_order=140, model="respond_test_app.htninitialreview", required=False),
    Crf(show_order=150, model="respond_test_app.cholinitialreview", required=False),
    Crf(show_order=160, model="respond_test_app.hivreview", required=False),
    Crf(show_order=170, model="respond_test_app.dmreview", required=False),
    Crf(show_order=180, model="respond_test_app.htnreview", required=False),
    Crf(show_order=190, model="respond_test_app.cholreview", required=False),
    Crf(show_order=200, model="respond_test_app.medications", required=False),
)

crfs_missed = FormsCollection(
    Crf(show_order=10, model="respond_test_app.subjectvisitmissed"),
    name="missed",
)

requisitions = FormsCollection(name="requisitions")


visit_schedule = VisitSchedule(
    name="visit_schedule",
    offstudy_model="respond_test_app.subjectoffstudy",
    death_report_model="respond_test_app.deathreport",
    locator_model="edc_locator.subjectlocator",
)

schedule = Schedule(
    name="schedule",
    onschedule_model="respond_test_app.onschedule",
    offschedule_model="respond_test_app.offschedule",
    appointment_model="edc_appointment.appointment",
    consent_model="respond_test_app.subjectconsent",
)

visits = []
for index in range(0, 4):
    visits.append(
        Visit(
            code=f"{1 if index == 0 else index + 1}000",
            title=f"Day {1 if index == 0 else index + 1}",
            timepoint=index,
            rbase=relativedelta(days=7 * index),
            rlower=relativedelta(days=0),
            rupper=relativedelta(days=6),
            requisitions=requisitions,
            crfs=crfs_followup if index else crfs_baseline,
            crfs_missed=crfs_missed,
            requisitions_unscheduled=requisitions,
            crfs_unscheduled=crfs_followup,
            allow_unscheduled=True,
            facility_name="5-day-clinic",
        )
    )
for visit in visits:
    schedule.add_visit(visit)


visit_schedule.add_schedule(schedule)

site_visit_schedules.register(visit_schedule)
