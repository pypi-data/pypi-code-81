import datetime
import ladok3

def add_command_options(parser):
  report_parser = parser.add_parser("report",
    help="Reports course results to LADOK",
    description="Reports course results to LADOK"
  )
  report_parser.set_defaults(func=command)
  report_parser.add_argument("student_id",
    help="Student identifier (personnummer or LADOK ID)"
  )

  report_parser.add_argument("course_code",
    help="The course code (e.g. DD1315) for which the grade is for"
  )

  report_parser.add_argument("component_code",
    help="The component code (e.g. LAB1) for which the grade is for"
  )

  report_parser.add_argument("grade",
    help="The grade (e.g. A or P)"
  )
  report_parser.add_argument("-d", "--date",
    help="Date on ISO format (e.g. 2021-03-18), "
      f"defaults to today's date ({datetime.date.today()})",
    type=datetime.date.fromisoformat,
    default=datetime.date.today()
  )
  report_parser.add_argument("-f", "--finalize",
    help="Finalize the grade (mark as ready/klarmarkera) for examiner to attest",
    action="store_true",
    default=False
  )

def command(ladok, args):
  try:
    student = ladok.get_student(args.student_id)
    course = student.courses(code=args.course_code)[0]
    result = course.results(component=args.component_code)[0]
    result.set_grade(args.grade, args.date)
    if args.finalize:
      result.finalize()
  except Exception as err:
    try:
      print(f"{student}: {err}")
    except ValueError as verr:
      print(f"{verr}: {args.student_id}: {err}")
