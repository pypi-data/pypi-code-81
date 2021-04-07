"""CCURE Update class file."""
import csv
import datetime
import json


class Update:
    """CCURE Update class."""

    def __init__(
        self,
        ccure,
        credentials_path="credentials.csv",
        newpersonnel_path="newpersonnel.csv",
        personnel_path="personnel.csv",
    ):
        """Initialize an Update class instance."""
        self.ccure = ccure

        self.credentials_path = credentials_path
        self.newpersonnel_path = newpersonnel_path
        self.personnel_path = personnel_path

        self.credentials = None
        # self.personnel = None
        self.personnel_types = None

        self.people = None
        self.emplids = None
        self.missing_personnel_types = None

        self.ccure_people = None
        self.workday_people = None

        # output data
        self.new_personnel = None
        self.updated_personnel = None

        self.type_exceptions = [
            "105 Broadway",
            "Board Member",
            "Construction",
            "Emergency",
            "Facilities Contractor",
            "Facilities Temp",
            "Temp Contractor",
            "Temporary Card",
            "Terminated Contractor",
            "Visitor",
            "Workday Project",
        ]

        self.personnel_fieldnames = [
            "ObjectID",
            "GUID",
            "FirstName",
            "LastName",
            "MiddleName",
            "LegalName",
            "PersonnelType",
            "PID",
            "EMPLID",
            "Username",
            "Email",
            "AccessLevel",
            "HomeInstitution",
            "DepartmentName",
            "SupervisorName",
            "Title",
            "WorkerType",
            "OrgUnit",
            "Desk",
            "Parking",
            "Status",
            "ActivationDateTime",
            "ExpirationDateTime",
        ]

    def check_emplid_exceptions(self):
        if self.emplid_exceptions:
            print(f"\nCCURE-only Personnnel with a valid EMPLID [{len(self.emplid_exceptions)}]:")
        for p in sorted(self.emplid_exceptions, key=lambda x: x["first_name"] + x["last_name"]):
            oid = p["id"]
            emplid = p["emplid"]
            first_name = p["first_name"]
            last_name = p["last_name"]
            personnel_type_name = p["personnel_type_name"]
            title = p["title"]
            print(f" * {oid} {first_name} {last_name} [{personnel_type_name}] with emplid {emplid}")

    def check_matched_people(self, matched):
        """Check matched Workday people in CCURE."""
        updates = []
        for emplid in matched:
            p = matched[emplid]
            oid = p["id"]
            first_name = p["first_name"]
            last_name = p["last_name"]
            person = self.emplids[emplid]
            output = []
            for key in p:
                if key in [
                    "company",
                    "disabled",
                    "guid",
                    "id",
                    "personnel_type_id",
                    # "personnel_type_name",
                ]:
                    continue
                if key not in person:
                    print(f"   Missing key: {key} [{p[key]}]")
                o = p[key]
                n = person[key]
                if n is None:
                    n = ""
                if o != n:
                    output.append(f"   {key}: {json.dumps(o)} -> {json.dumps(n)}")
                    p[key] = n
            if output:
                person["id"] = oid
                person["guid"] = p["guid"]
                updates.append(person)
                print(f"\n{emplid} {first_name} {last_name} [{oid}]")
                print("\n".join(output))
        return updates

    def check_unmatched_people(self, unmatched):
        """Check unmatched Workday people in CCURE."""
        category = ""
        for p in sorted(unmatched, key=lambda x: x["personnel_type_name"] + str(x["id"])):
            oid = p["id"]
            if oid in [1000, 5000, 8260]:
                continue
            if category != p["personnel_type_name"]:
                print(f"\n  {p['personnel_type_name']}:")
                category = p["personnel_type_name"]
            print(
                f"    {oid}: {p['first_name']} {p['last_name']}, "
                f"{p['personnel_type_name']} [{p['title']}]"
            )

    def generate_newpersonnel(self, matched):
        """Generate the data for the newpersonnel.csv."""
        newpersonnel = []
        for emplid in sorted(self.emplids):
            if emplid in matched:
                continue
            p = self.emplids[emplid]
            first_name = p["first_name"]
            last_name = p["last_name"]
            personnel_type_name = p["personnel_type_name"]
            print(f" + {emplid} {first_name} {last_name} [{personnel_type_name}]")
            newpersonnel.append(p)
        self.newpersonnel = newpersonnel
        return newpersonnel

    def get_credentials(self):
        """Return Credentials formatted for update."""
        credentials = []
        for row in self.ccure.get_credentials():
            data = {
                "id": row["ObjectID"],
                "guid": row["GUID"],
                "personnel_id": row["PersonnelId"],
                "card_number": row["CardNumber"],
                "activation_datetime": row["ActivationDateTime"],
                "expiration_datetime": row["ExpirationDateTime"],
                "disabled": row["Disabled"],
                "lost": row["Lost"],
                "stolen": row["Stolen"],
            }
            credentials.append(data)
        return credentials

    def get_credentials_dict(self):
        """Return a dict of Credentials."""
        if self.credentials:
            return credentials
        credentials = {}
        for c in self.get_credentials():
            cid = c["id"]
            credentials[cid] = c
        self.credentials = credentials
        return credentials

    def get_personnel(self):
        """Return Personnal formatted for update."""
        personnel_types = self.get_personnel_types_dict()
        personnel = []

        for row in self.ccure.get_personnel():
            data = {
                "id": row["ObjectID"],
                "guid": row["GUID"],
                "first_name": row["FirstName"],
                "middle_name": row["MiddleName"],
                "last_name": row["LastName"],
                "personnel_type_id": row["PersonnelTypeID"],
                "personnel_type_name": personnel_types.get(row["PersonnelTypeID"]),
                "disabled": row["Disabled"],
                "status": row["Text1"],
                "company": row["Text2"],
                "parking": row["Text3"],
                "pid": row["Text4"],
                "emplid": row["Text5"],
                "username": row["Text6"],
                "email": row["Text7"],
                "home_institution": row["Text8"],
                "department_name": row["Text9"],
                "supervisor_name": row["Text10"],
                "text11": row["Text11"],
                "text12": row["Text12"],
                "text13": row["Text13"],
                "legal_name": row["Text14"],
                "text15": row["Text15"],
                "title": row["Text16"],
                "worker_type": row["Text17"],
                "org_unit": row["Text18"],
                "desk": row["Text19"],
                "text20": row["Text20"],
                "text21": row["Text21"],
                "text22": row["Text22"],
                "text23": row["Text23"],
                "text24": row["Text24"],
                "text25": row["Text25"],
            }
            personnel.append(data)
        return personnel

    def get_personnel_dict(self):
        personnel = {}
        for p in self.get_personnel():
            oid = p["id"]
            personnel[oid] = p
        return personnel

    def get_personnel_types(self):
        """Return Personnal Types formatted for update."""
        personnel_types = []
        for row in self.ccure.get_personnel_types():
            data = {
                "id": int(row["ObjectID"]),
                "name": row["Name"],
            }
            personnel_types.append(data)
        return personnel_types

    def get_personnel_types_dict(self):
        """Return a dict of Personnel Types."""
        if self.personnel_types:
            return self.personnel_types
        personnel_types = {}
        for t in self.get_personnel_types():
            tid = t["id"]
            personnel_types[tid] = t["name"]
        self.personnel_types = personnel_types
        return personnel_types

    def get_personnel_type_names(self):
        """Return a list of names of valid Personnel Types."""
        names = []
        for tid in self.get_personnel_types_dict():
            names.append(self.personnel_types[tid])
        return sorted(set(names))

    def organize_personnel(self, personnel):
        """Organize personall by CCURE-only and Workday."""
        ccure_people = {}
        workday_people = {}

        emplid_exceptions = []

        # organize personnel by CCURE-only or Workday
        for oid in personnel:
            p = personnel[oid]
            personnel_type = p["personnel_type_name"]
            if personnel_type in self.type_exceptions:
                ccure_people[oid] = p
                emplid = p["emplid"]
                if emplid and emplid in self.emplids:
                    emplid_exceptions.append(p)
            else:
                workday_people[oid] = p

        self.ccure_people = ccure_people
        self.workday_people = workday_people
        self.emplid_exceptions = emplid_exceptions

        return ccure_people, workday_people

    def organize_workday_personnel(self, workday_people):
        """Organize Workday Personnel into matched and unmatched."""
        matched = {}
        unmatched = []

        # organize workday_people into matches
        for oid in sorted(workday_people):
            p = workday_people[oid]
            emplid = p["emplid"]
            if emplid and emplid in self.emplids:
                if emplid not in matched:
                    matched[emplid] = p
                else:
                    print(f"\nERROR: Duplicate EMPLID in CCURE: {emplid}")
                    dup = matched[emplid]
                    print(
                        f"  * {dup['first_name']} {dup['last_name']} "
                        f"[{dup['id']}] {dup['personnel_type_name']}"
                    )
                    print(
                        f"  * {p['first_name']} {p['last_name']} "
                        f"[{p['id']}] {p['personnel_type_name']}"
                    )
            else:
                unmatched.append(p)

        return matched, unmatched

    def prepare_people(self, people):
        """Prepare People records for CCURE."""
        personnel_type_names = self.get_personnel_type_names()
        missing_personnel_types = []

        emplids = {}

        # create dicts of people by emplid and pid
        for p in people:
            emplid = p["emplid"]
            # pid = p["person_id"]
            worker_sub_type = p["worker_sub_type"]

            p["company"] = ""
            # p["disabled"] = p["terminated"]
            if "disabled" in p:
                del p["disabled"]
            # p["first_name"] = p["first_name_ascii"]
            if (len(p["home_institution"]) < 125):
                p["home_institution"][:125]
            # p["last_name"] = p["last_name_ascii"]
            # p["legal_name"] = f"{p['legal_last_name']},{p['legal_first_name']}"
            p["middle_name"] = ""
            # p["parking"] = "Yes" if p["parking"] else "No"
            p["person_id"] = ""
            p["personnel_type_name"] = worker_sub_type if worker_sub_type in personnel_type_names else "None"
            p["pid"] = ""
            # p["status"] = "Terminated" if p["terminated"] else "Active"
            # p["supervisor_name"] = p["manager_ascii"]
            p["text11"] = ""
            p["text12"] = ""
            p["text13"] = ""
            p["text15"] = ""
            p["text20"] = ""
            p["text21"] = ""
            p["text22"] = ""
            p["text23"] = ""
            p["text24"] = ""
            p["text25"] = ""

            # get activation datetime
            # start_date = p["activation_datetime"]
            # activation_datetime = "1990-01-01 00:00:01"
            # if start_date and start_date >= "1990-01-01":
            #     activation_datetime = f"{start_date} 00:00:01"
            # p["activation_datetime"] = activation_datetime

            # # get expiration datetime
            # end_date = p["security_card_end_date"]
            # expiration_datetime = "2037-12-31 00:00:01"
            # if end_date:
            #     expiration_datetime = f"{end_date} 23:59:59"
            # p["expiration_datetime"] = expiration_datetime

            # check for missing personnel types in CCURE
            if worker_sub_type not in personnel_type_names and worker_sub_type not in missing_personnel_types:
                missing_personnel_types.append(worker_sub_type)

            emplids[emplid] = p

        self.people = people
        self.emplids = emplids
        self.missing_personnel_types = missing_personnel_types

        return emplids

    def prepare_credentials(self, matched):
        """Prepare data for credentials.csv."""
        # organize people by personnel_id
        people = {}
        for emplid in matched:
            # get personnel record
            p = matched[emplid]
            guid = p["guid"]
            oid = p["id"]

            # get person record
            person = self.emplids[emplid]
            person["guid"] = guid
            people[oid] = person

        # organize cards by person
        person_cards = {}
        for oid in self.credentials:
            c = self.credentials[oid]
            pid = c["personnel_id"]
            # skip personnel that weren't matched with workday
            if pid not in people:
                continue
            if pid not in person_cards:
                person_cards[pid] = []
            person_cards[pid].append(c)

        entries = []
        for pid in person_cards:
            p = people[pid]
            cards = person_cards[pid]

            for c in cards:
                output = []
                if str(c['activation_datetime']) != p['activation_datetime']:
                    output.append(f" * activation_datetime: {str(c['activation_datetime'])} -> {str(p['activation_datetime'])}")
                if str(c['expiration_datetime']) != p['expiration_datetime']:
                    output.append(f" * expiration_datetime: {str(c['expiration_datetime'])} -> {str(p['expiration_datetime'])}")
                card = {
                    'ObjectID': c['id'],
                    'Personnel.GUID': p['guid'],
                    'Credentials.GUID': c['guid'],
                    'ActivationDateTime': p['activation_datetime'],
                    'ExpirationDateTime': p['expiration_datetime'],
                }
                if output:
                    entries.append(card)

                if output:
                    card_id = c['id']
                    emplid = p["emplid"]
                    first_name = p["first_name"]
                    last_name = p["last_name"]

                    print(f"\n{card_id} {first_name} {last_name} [{emplid}]:")
                    print("\n".join(output))

        return entries

    def prepare_newpersonnel(self, newpersonnel):
        """Prepare data for newpersonnel.csv."""
        entries = []
        for p in newpersonnel:
            entry = self.prepare_person(p)
            entries.append(entry)
        return entries

    def prepare_person(self, p):
        """Prepare a single personnel record."""
        entry = {
            "ObjectID": p.get("id"),
            "GUID": p.get("guid"),
            "FirstName": p["first_name"],
            "LastName": p["last_name"],
            "MiddleName": "",
            "LegalName": p["legal_name"],
            "PersonnelType": p["personnel_type_name"],
            "PID": p["person_id"],
            "EMPLID": p["emplid"],
            "Username": p["username"],
            "Email": p["email"],
            "AccessLevel": None,
            "HomeInstitution": p["home_institution"],
            "DepartmentName": p["department_name"],
            "SupervisorName": p["supervisor_name"],
            "Title": p["title"],
            "WorkerType": p["worker_type"],
            "OrgUnit": p["org_unit"],
            "Desk": p["desk"],
            "Parking": p["parking"],
            "Status": p["status"],
            "ActivationDateTime": p["activation_datetime"],
            "ExpirationDateTime": p["expiration_datetime"],
        }
        return entry

    def prepare_personnel(self, personnel):
        """Prepare data fro personnel.csv."""
        entries = []
        for p in personnel:
            entry = self.prepare_person(p)
            entries.append(entry)
        return entries

    def write_credentials(self, matched):
        """Write out the credentials.csv file."""
        entries = self.prepare_credentials(matched)

        # open a cvs file to write to
        csvfile = open(self.credentials_path, "w")

        # select which fields to include in the CSV and which order
        fieldnames = [
            'ObjectID',
            'Personnel.GUID',
            'Credentials.GUID',
            'ActivationDateTime',
            'ExpirationDateTime',
        ]

        # create a cvs writer to write to the file
        csvwriter = csv.DictWriter(csvfile, delimiter=",", fieldnames=fieldnames)
        csvwriter.writeheader()

        for card in entries:
            try:
                csvwriter.writerow(card)
            except Exception as err:
                print(f"ERROR Writing credential: {emplid} [{err}]")
                print(person)

        # close the csv file
        csvfile.close()
    def write_newpersonnel(self, newpersonnel):
        """Write out the newpersonnel.csv file."""
        entries = self.prepare_newpersonnel(newpersonnel)

        # open a cvs file to write to
        csvfile = open(self.newpersonnel_path, "w")

        # create a cvs writer to write to the file
        csvwriter = csv.DictWriter(csvfile, delimiter=",", fieldnames=self.personnel_fieldnames)
        csvwriter.writeheader()

        for person in entries:
            emplid = person["EMPLID"]
            try:
                csvwriter.writerow(person)
            except Exception as err:
                print(f"ERROR Writing new person: {emplid} [{err}]")
                print(person)

        # close the csv file
        csvfile.close()

    def write_personnel(self, personnel):
        """Write out the personnel.csv file."""
        entries = self.prepare_personnel(personnel)

        # open a cvs file to write to
        csvfile = open(self.personnel_path, "w")

        # create a cvs writer to write to the file
        csvwriter = csv.DictWriter(csvfile, delimiter=",", fieldnames=self.personnel_fieldnames)
        csvwriter.writeheader()

        for person in entries:
            emplid = person["EMPLID"]
            try:
                csvwriter.writerow(person)
            except Exception as err:
                print(f"ERROR Writing person: {emplid} [{err}]")
                print(person)

        # close the csv file
        csvfile.close()

    def update(self, people):
        """Update Personnel and Credentials from People."""
        # create dicts of people by emplid and pid
        emplids = self.prepare_people(people)

        # check for missing personnel types
        if self.missing_personnel_types:
            print(f"\nMissing Personnel Types [{len(self.missing_personnel_types)}]:")
            print(" * " + "\n * ".join(set(self.missing_personnel_types)))

        # get personnel from CCURE
        personnel = self.get_personnel_dict()

        # get credentials from CCURE
        credentials = self.get_credentials_dict()

        # organize personnel by CCURE-only or Workday
        ccure_people, workday_people = self.organize_personnel(personnel)
        print(f"\nWorkday People: {len(workday_people)}, CCURE People: {len(ccure_people)}")

        # check for people with personnel type exception and a valid emplid
        # self.check_emplid_exceptions()

        # organize workday_people into matches
        matched, unmatched = self.organize_workday_personnel(personnel)
        print(f"\nMatched: {len(matched)}, Unmatched: {len(unmatched)}")

        # check for people to add
        print("\nChecking for Workday People to add to CCURE...")
        personnel_to_add = self.generate_newpersonnel(matched)
        print(f"Adding {len(personnel_to_add)} Workday Personnel to CCURE.")

        # check matched people
        print(f"\nChecking {len(matched)} existing Workday Personnel for updates...")
        personnel_to_update = self.check_matched_people(matched)
        print(f"Updating {len(personnel_to_update)} Workday Personnel in CCURE.")

        # check unmatched people
        # print(f"\fChecking {len(unmatched)} unmatched Workday Personnel...")
        # self.check_unmatched_people(unmatched)

        # generate the credentials.csv
        self.write_credentials(matched)

        # generate the newpersonnel.csv
        self.write_newpersonnel(personnel_to_add)

        # generate the personnel.csv
        self.write_personnel(personnel_to_update)

        # # check CCURE-only people
        # print(f"\fChecking {len(ccure_people)} CCURE-only Personnel...")
        # category = ""
        # bademplids = []
        # for oid in sorted(
        #     ccure_people,
        #     key=lambda x: ccure_people[x]["personnel_type_name"] + str(ccure_people[x]["title"]) + str(ccure_people[x]["id"])
        # ):
        #     p = ccure_people[oid]
        #     oid = p["id"]
        #     if oid in [1000, 5000, 8260]:
        #         continue
        #     if category != p["personnel_type_name"]:
        #         print(f"\n  {p['personnel_type_name']}:")
        #         category = p["personnel_type_name"]
        #     print(
        #         f"    {oid}: {p['first_name']} {p['last_name']}, "
        #         f"{p['personnel_type_name']} [{p['title']}]"
        #     )
        #     if p["emplid"]:
        #         bademplids.append(p)

        # if bademplids:
        #     print(f"Found {len(bademplids)} CCURE-only records with an EMPLID!")
        #     for p in bademplids:
        #         print(p["emplid"], p["personnel_type_name"])