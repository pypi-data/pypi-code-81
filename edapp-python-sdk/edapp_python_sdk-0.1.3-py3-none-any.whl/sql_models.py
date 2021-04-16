usergroups_sql = """(
  id text PRIMARY KEY, name text, email text, 
  hasChildren boolean, last_export datetime
)"""

group_users_sql = """(
  user_id text, group_id text, last_export datetime
)"""

users_sql = """(
  id text PRIMARY KEY, name text, email text, 
  firstName text, lastName text, externalId text, 
  lastActiveDate datetime, userGroupsManaged text, 
  roles text, last_export datetime
)"""

user_children_sql = """(
    id text PRIMARY KEY, name text,
    inviteCode text, hasChildren boolean,
    parentGroupId text, last_export datetime
)"""

course_sql = """(
  id text PRIMARY KEY, externalId text, 
  title text, description text, status text, 
  locale text, duration integer, thumbnailUrl text, 
  createdDateTime datetime, modifiedDateTime datetime, 
  last_export datetime
)
"""

courses_sql = """(
  id text PRIMARY KEY, externalId text, 
  title text, description text, status text, 
  locale text, duration integer, thumbnailUrl text, 
  createDateTime datetime, modifiedDateTime text, 
  last_export datetime
)
"""

lessons_sql = """(
  id text PRIMARY KEY, externalId text, 
  title text, description text, status text, courseId text,
  last_export datetime
)
"""

lessonprogress_sql = """(
  id text PRIMARY KEY, userId text, userEmail text,
  userFirstName text, userLastName text,
  courseId text, courseTitle text,
  courseExternalId text, lessonId text,
  lessonTitle text, lessonExternalId text,
  eventName text, eventDateTime datetime,
  lessonScore integer, last_export datetime
)
"""

custom_fields_sql = """(
  user_id text, user_email text, custom_field text, 
  custom_value text, last_export datetime
)
"""

surveyanswers_sql = """(
  id text PRIMARY KEY, courseid text, courseexternalid text, 
  lessonid text, lessonexternalid text, 
  slideid text, userid text, userexternalid text, 
  attemptid text, questionid text, questioncontent text, 
  answerdefinitionid text, answercontent text, 
  answereddatetime datetime, last_export datetime
)
"""

attempts_sql = """(
  id text PRIMARY KEY, userId text, userExternalId text, 
  courseId text, courseExternalId text, 
  lessonId text, lessonExternalId text, 
  startedDateTime datetime, completedDateTime datetime, 
  score int, success boolean, earnedStars int, 
  last_export datetime
)
"""

courseprogress_sql = """(
  id text PRIMARY KEY, unlocked boolean, unlockedDateTime datetime, 
  opened boolean, openedDateTime datetime, completed boolean, 
  completedDateTime datetime, lessonsTotal integer, 
  lessonsUnlocked integer, lessonsCompleted integer, courseId text,
  courseExternalId text, courseTitle text, userName text, 
  userFirstName text, userLastName text, userId text, 
  userExternalId text, archived boolean, percentageCompleted float,
  score float, last_export datetime
)
"""

coursestatistics_sql = """(
  courseId text, totalUsers integer, 
  completedCount integer, openedCount integer, last_export datetime
)
"""
