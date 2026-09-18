from urllib.parse import urlencode
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from openmrs.repository.patient_summary import PatientSummary
import re
import os
from dotenv import load_dotenv
load_dotenv()



class KenyaEMRAPI:

    def __init__(
        self,
        base_url=os.getenv("KENYAEMR_URL"),
        username=os.getenv("KENYAEMR_USERNAME"),
        password=os.getenv("KENYAEMR_PASSWORD")
    ):
        self.base_url = base_url.rstrip("/")
        print(self.base_url)

        # -------------------------------------------------
        # HTTP Session
        # -------------------------------------------------
        self.session = requests.Session()

        self.session.auth = HTTPBasicAuth(
            username,
            password
        )

        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

        # -------------------------------------------------
        # Current Patient Session
        # -------------------------------------------------
        self.patient_session = None

    # -------------------------------------------------
    # Internal GET Request
    # -------------------------------------------------
    async def _get(self, url):


        response = self.session.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return  response.json()

    # -------------------------------------------------
    # Search Patient
    # -------------------------------------------------
    async def search_patient(
            self,
            query,
            limit=10,
            include_dead=True
    ):

        # -------------------------------------------------
        # Only retrieve required patient information
        # -------------------------------------------------
        custom_fields = (
            "patientId,"
            "uuid,"
            "identifiers:(uuid,identifier,identifierType:(uuid,display),preferred),"
            "person:("
            "gender,"
            "age,"
            "birthdate,"
            "personName:(givenName,middleName,familyName),"
            "addresses:("
            "preferred,"
            "address1,"
            "address2,"
            "address4,"
            "cityVillage,"
            "countyDistrict,"
            "stateProvince,"
            "country"
            ")"
            "),"
            "attributes:(value,attributeType:(uuid,display))"
        )

        params = {
            "q": query,
            "v": f"custom:({custom_fields})",
            "includeDead": str(include_dead).lower(),
            "limit": limit,
            "totalCount": "true"
        }

        url = (
                f"{self.base_url}/ws/rest/v1/patient?"
                + urlencode(params)
        )

        data = await self._get(url)

        results = data.get("results", [])

        if not results:
            self.patient_session = None

            return {
                "success": False,
                "message": "Patient not found",
                "patient": None
            }

        # -------------------------------------------------
        # Use first patient returned
        # -------------------------------------------------
        patient = results[0]

        person = patient.get("person", {})

        # -------------------------------------------------
        # Patient name
        # -------------------------------------------------
        patient_name = self._get_patient_name(person)

        # -------------------------------------------------
        # Patient address
        # -------------------------------------------------
        patient_address = self._get_address(person)

        # -------------------------------------------------
        # Identifiers
        # -------------------------------------------------
        identifiers = []

        for item in patient.get("identifiers", []):

            if item.get("voided"):
                continue

            identifiers.append({
                "identifier": item.get("identifier"),
                "type": (
                    item
                    .get("identifierType", {})
                    .get("display")
                ),
                "preferred": item.get("preferred", False)
            })

        # -------------------------------------------------
        # Relevant patient attributes only
        # -------------------------------------------------
        relevant_attributes = {
            "Telephone contact": "phone",
            "Alternate Phone Number": "alternate_phone",
            "Next of kin name": "next_of_kin_name",
            "Next of kin relationship": "next_of_kin_relationship",
            "Next of kin contact": "next_of_kin_contact"
        }

        patient_details = {
            "phone": None,
            "alternate_phone": None,
            "next_of_kin_name": None,
            "next_of_kin_relationship": None,
            "next_of_kin_contact": None
        }

        for attribute in patient.get("attributes", []):

            attribute_type = (
                attribute
                .get("attributeType", {})
                .get("display")
            )

            key = relevant_attributes.get(attribute_type)

            if key:
                patient_details[key] = attribute.get("value")

        # -------------------------------------------------
        # Create clean patient session
        # -------------------------------------------------
        self.patient_session = {

            "patient_id": patient.get("patientId"),

            "patient_uuid": patient.get("uuid"),

            "patient_name": patient_name,

            "age": person.get("age"),

            "sex": person.get("gender"),

            "dob": person.get("birthdate"),

            "identifiers": identifiers,

            "address": patient_address,

            "phone": patient_details["phone"],

            "alternate_phone": (
                patient_details["alternate_phone"]
            ),

            "next_of_kin": {
                "name": patient_details[
                    "next_of_kin_name"
                ],

                "relationship": patient_details[
                    "next_of_kin_relationship"
                ],

                "contact": patient_details[
                    "next_of_kin_contact"
                ]
            },

            "summary": None
        }

        return self.patient_session

    # -------------------------------------------------
    # Patient Name Helper
    # -------------------------------------------------
    @staticmethod
    def _get_patient_name(person):

        person_name = person.get("personName")

        if not person_name:
            return None

        if isinstance(person_name, list):
            if not person_name:
                return None
            person_name = person_name[0]

        if not isinstance(person_name, dict):
            return str(person_name)

        names = [
            person_name.get("givenName"),
            person_name.get("middleName"),
            person_name.get("familyName")
        ]

        return " ".join(
            str(name).strip()
            for name in names
            if name
        )

    @staticmethod
    def _get_address(person):

        addresses = person.get("addresses", [])

        if not addresses:
            return None

        # Prefer preferred address
        address = next(
            (
                item
                for item in addresses
                if item.get("preferred")
            ),
            addresses[0]
        )

        return {
            "address1": address.get("address1"),
            "address2": address.get("address2"),
            "village": address.get("address4"),
            "city": address.get("cityVillage"),
            "county": address.get("countyDistrict"),
            "sub_county": address.get("stateProvince"),
            "country": address.get("country")
        }

    # -------------------------------------------------
    # Get Current Patient Session
    # -------------------------------------------------
    def get_patient_session(self):

        print("SESSION")

        return self.patient_session

    # -------------------------------------------------
    # Clear Patient Session
    # -------------------------------------------------
    def clear_patient_session(self):

        self.patient_session = None

        return {
            "success": True,
            "message": "Patient session cleared"
        }

    # -------------------------------------------------
    # Patient Summary
    # -------------------------------------------------

    from datetime import datetime

    from datetime import datetime

    async def patient_summary(
            self,
            patient_uuid=None,
            refresh=False
    ):

        # -------------------------------------------------
        # Get patient UUID from session
        # -------------------------------------------------
        if patient_uuid is None:

            if not self.patient_session:
                raise ValueError(
                    "No patient session available"
                )

            patient_uuid = self.patient_session[
                "patient_uuid"
            ]

        # -------------------------------------------------
        # Return cached summary
        # -------------------------------------------------
        if (
                not refresh
                and self.patient_session
                and self.patient_session.get(
            "patient_uuid"
        ) == patient_uuid
                and self.patient_session.get(
            "summary"
        ) is not None
        ):
            return self.patient_session[
                "summary"
            ]

        # -------------------------------------------------
        # API URL
        # -------------------------------------------------
        url = (
            f"{self.base_url}"
            f"/ws/rest/v1/kenyaemr/patientSummary"
            f"?patientUuid={patient_uuid}"
        )

        # -------------------------------------------------
        # Get summary
        # -------------------------------------------------
        data = await self._get(url)

        if not isinstance(
                data,
                (dict, list)
        ):
            return data

        # -------------------------------------------------
        # Parse dates
        # -------------------------------------------------
        def parse_date(value):

            if not value:
                return None

            if isinstance(value, datetime):
                return value

            value = str(value).strip()

            formats = [
                "%d/%m/%Y",
                "%d-%m-%Y",
                "%Y-%m-%d",
                "%d %b %Y",
                "%d %B %Y",
                "%Y/%m/%d",
                "%d/%m/%Y %H:%M:%S",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S.%f%z",
            ]

            for fmt in formats:

                try:
                    return datetime.strptime(
                        value,
                        fmt
                    )

                except (
                        ValueError,
                        TypeError
                ):
                    continue

            try:
                return datetime.fromisoformat(
                    value.replace(
                        "Z",
                        "+00:00"
                    )
                )

            except (
                    ValueError,
                    TypeError
            ):
                return None

        # -------------------------------------------------
        # Get date from a record
        # -------------------------------------------------
        def get_record_date(record):

            if not isinstance(record, dict):
                return None

            date_fields = [
                "vlDate",
                "cd4CountDate",
                "date",
                "resultDate",
                "sampleDate",
                "visitDate",
                "encounterDate",
                "encounterDatetime",
                "obsDatetime",
                "orderDate",
                "startDate",
                "dateStarted",
                "dateCreated",
                "createdDate",
                "appointmentDate",
                "nextAppointmentDate",
            ]

            # Known date fields first
            for field in date_fields:

                value = record.get(field)

                parsed = parse_date(value)

                if parsed:
                    return parsed

            # Fallback: any field containing "date"
            for key, value in record.items():

                key_lower = str(key).lower()

                if (
                        "date" in key_lower
                        or "datetime" in key_lower
                ):

                    parsed = parse_date(value)

                    if parsed:
                        return parsed

            return None

        # -------------------------------------------------
        # Recursively keep all fields.
        #
        # Only lists containing dated dictionaries are
        # shortened to the latest two.
        #
        # Lists of strings, numbers, medications, etc.
        # remain unchanged.
        # -------------------------------------------------
        def process_value(value):

            # ---------------------------------------------
            # Dictionary
            # ---------------------------------------------
            if isinstance(value, dict):
                return {
                    key: process_value(item)
                    for key, item in value.items()
                }

            # ---------------------------------------------
            # List
            # ---------------------------------------------
            if isinstance(value, list):

                # Process children first
                processed = [
                    process_value(item)
                    for item in value
                ]

                # 0 - 2 items need no trimming
                if len(processed) <= 2:
                    return processed

                # -----------------------------------------
                # IMPORTANT:
                # Do not touch lists containing strings,
                # numbers, None, etc.
                # -----------------------------------------
                if not all(
                        isinstance(item, dict)
                        for item in processed
                ):
                    return processed

                dated_records = []

                for item in processed:

                    record_date = get_record_date(
                        item
                    )

                    # If even one record has no date,
                    # preserve the complete collection.
                    if record_date is None:
                        return processed

                    dated_records.append(
                        (
                            record_date,
                            item
                        )
                    )

                # -----------------------------------------
                # Newest first
                # -----------------------------------------
                dated_records.sort(
                    key=lambda x: x[0],
                    reverse=True
                )

                # -----------------------------------------
                # Latest two complete records
                # -----------------------------------------
                return [
                    item
                    for _, item
                    in dated_records[:2]
                ]

            # ---------------------------------------------
            # String / number / bool / None
            # ---------------------------------------------
            return value

        # -------------------------------------------------
        # Process entire API payload
        # -------------------------------------------------
        patient_summary = process_value(
            data
        )

        # -------------------------------------------------
        # Save summary in patient session
        # -------------------------------------------------
        if self.patient_session:
            self.patient_session[
                "summary"
            ] = patient_summary

        return patient_summary

        return data

    # -------------------------------------------------
    # Encounter History
    # -------------------------------------------------

    async def encounter_history(
            self,
            patient_uuid=None
    ):
        """
        Retrieve cleaned patient encounter history.

        Returns:
        - encounter date
        - encounter type
        - location
        - provider

        Removes UUIDs, links and other OpenMRS metadata.
        """

        if patient_uuid is None:

            if not self.patient_session:
                raise ValueError(
                    "No patient session available"
                )

            patient_uuid = self.patient_session[
                "patient_uuid"
            ]

        custom_view = (
            "encounterDatetime,"
            "encounterType:(display),"
            "location:(display),"
            "encounterProviders:("
            "provider:("
            "person:(display)"
            ")"
            ")"
        )

        params = {
            "patient": patient_uuid,
            "v": f"custom:({custom_view})"
        }

        url = (
                f"{self.base_url}"
                f"/ws/rest/v1/encounter?"
                + urlencode(params)
        )

        data = await self._get(url)

        encounters = []

        for encounter in data.get(
                "results",
                []
        ):

            encounter_datetime = encounter.get(
                "encounterDatetime"
            )

            if encounter_datetime:
                encounter_date = datetime.strptime(
                    encounter_datetime[:19],
                    "%Y-%m-%dT%H:%M:%S"
                ).strftime("%d %b %Y")
            else:
                encounter_date = None

            encounter_type = (
                    encounter.get(
                        "encounterType"
                    ) or {}
            ).get("display")

            location = (
                    encounter.get(
                        "location"
                    ) or {}
            ).get("display")

            providers = []

            for item in encounter.get(
                    "encounterProviders",
                    []
            ):

                provider = item.get(
                    "provider"
                ) or {}

                person = provider.get(
                    "person"
                ) or {}

                provider_name = person.get(
                    "display"
                )

                if provider_name:
                    providers.append(
                        provider_name
                    )

            encounters.append({
                "date": encounter_date,
                "encounter": encounter_type,
                "location": location,
                "provider": (
                    ", ".join(providers)
                    if providers
                    else None
                )
            })

        # Most recent encounters first
        encounters.sort(
            key=lambda x: (
                datetime.strptime(
                    x["date"],
                    "%d %b %Y"
                )
                if x["date"]
                else datetime.min
            ),
            reverse=True
        )

        return encounters

    # -------------------------------------------------
    # Drug Orders
    # -------------------------------------------------
    from datetime import datetime
    from urllib.parse import urlencode

    async def drug_orders(
            self,
            patient_uuid=None,
            care_setting="6f0c9a92-6f24-11e3-af88-005056821db0",
            order_type="131168f4-15f5-102d-96e4-000c29c2a5d7"
    ):

        if patient_uuid is None:

            if not self.patient_session:
                raise ValueError(
                    "No patient session available"
                )

            patient_uuid = self.patient_session[
                "patient_uuid"
            ]

        # Only request fields that are actually useful
        custom_view = (
            "uuid,"
            "orderNumber,"
            "action,"
            "dateActivated,"
            "dateStopped,"
            "autoExpireDate,"
            "orderReasonNonCoded,"
            "urgency,"
            "instructions,"
            "fulfillerStatus,"
            "drug:(display),"
            "dose,"
            "doseUnits:(display),"
            "frequency:(display),"
            "asNeeded,"
            "asNeededCondition,"
            "quantity,"
            "quantityUnits:(display),"
            "numRefills,"
            "dosingInstructions,"
            "duration,"
            "durationUnits:(display),"
            "route:(display),"
            "brandName,"
            "orderer:(person:(display))"
        )

        params = {
            "patient": patient_uuid,
            "careSetting": care_setting,
            "orderTypes": order_type,
            "v": f"custom:({custom_view})",
            "excludeDiscontinueOrders": "true"
        }

        url = (
                f"{self.base_url}"
                f"/ws/rest/v1/order?"
                + urlencode(params)
        )

        data = await self._get(url)

        drug_orders = []

        for order in data.get("results", []):

            date_activated = order.get("dateActivated")

            if date_activated:
                date_ordered = datetime.strptime(
                    date_activated[:19],
                    "%Y-%m-%dT%H:%M:%S"
                ).strftime("%d %b %Y")
            else:
                date_ordered = None

            drug = order.get("drug") or {}
            dose_units = order.get("doseUnits") or {}
            frequency = order.get("frequency") or {}
            quantity_units = order.get("quantityUnits") or {}
            duration_units = order.get("durationUnits") or {}
            route = order.get("route") or {}

            orderer = order.get("orderer") or {}
            person = orderer.get("person") or {}

            cleaned_order = {
                "date": date_ordered,
                "drug": drug.get("display"),
                "dose": order.get("dose"),
                "dose_unit": dose_units.get("display"),
                "frequency": frequency.get("display"),
                "route": route.get("display"),
                "quantity": order.get("quantity"),
                "quantity_unit": quantity_units.get(
                    "display"
                ),
                "duration": order.get("duration"),
                "duration_unit": duration_units.get(
                    "display"
                ),
                "refills": order.get("numRefills"),
                "as_needed": order.get("asNeeded"),
                "as_needed_condition": order.get(
                    "asNeededCondition"
                ),
                "instructions": (
                        order.get("dosingInstructions")
                        or order.get("instructions")
                ),
                "reason": order.get(
                    "orderReasonNonCoded"
                ),
                "status": order.get(
                    "fulfillerStatus"
                ),
                "prescriber": person.get(
                    "display"
                ),

                # Keep internally for sorting
                "_dateActivated": date_activated
            }

            drug_orders.append(cleaned_order)

        # Most recent first
        drug_orders.sort(
            key=lambda x: x.get("_dateActivated") or "",
            reverse=True
        )

        # Limit to latest 4
        drug_orders = drug_orders[:4]

        # Remove internal sorting field
        for order in drug_orders:
            order.pop("_dateActivated", None)

        return drug_orders

    # -------------------------------------------------
    # Risk Score
    # -------------------------------------------------
    async def  risk_score(self, patient_uuid=None):

        if patient_uuid is None:

            if not self.patient_session:
                raise ValueError(
                    "No patient session available"
                )

            patient_uuid = (
                self.patient_session[
                    "patient_uuid"
                ]
            )

        url = (
            f"{self.base_url}"
            f"/ws/rest/v1/keml/patientiitscore"
            f"?patientUuid={patient_uuid}"
        )

        return await self._get(url)

    # -------------------------------------------------
    # Encounter History
    # -------------------------------------------------


    # -------------------------------------------------
    # Historical Program Enrollment
    # -------------------------------------------------
    async def patient_historical_enrollment(
            self,
            patient_uuid=None
    ):
        """
        Retrieve the patient's historical KenyaEMR
        program enrollment information.
        """

        if patient_uuid is None:

            if not self.patient_session:
                raise ValueError(
                    "No patient session available"
                )

            patient_uuid = (
                self.patient_session[
                    "patient_uuid"
                ]
            )

        params = {
            "patientUuid": patient_uuid
        }

        url = (
                f"{self.base_url}"
                f"/ws/rest/v1/kenyaemr/"
                f"patientHistoricalEnrollment?"
                + urlencode(params)
        )

        return await self._get(url)

    # -------------------------------------------------
    # Eligible Programs
    # -------------------------------------------------
    async def eligible_programs(
            self,
            patient_uuid=None
    ):
        """
        Retrieve programs for which the patient
        is currently eligible.
        """

        if patient_uuid is None:

            if not self.patient_session:
                raise ValueError(
                    "No patient session available"
                )

            patient_uuid = (
                self.patient_session[
                    "patient_uuid"
                ]
            )

        params = {
            "patientUuid": patient_uuid
        }

        url = (
                f"{self.base_url}"
                f"/ws/rest/v1/kenyaemr/eligiblePrograms?"
                + urlencode(params)
        )

        return await self._get(url)

    # -------------------------------------------------
    # Program Enrollments
    # -------------------------------------------------
    async def program_enrollments(
            self,
            patient_uuid=None
    ):
        """
        Retrieve the patient's program enrollment history,
        including enrollment dates, completion dates,
        locations and program states.
        """

        if patient_uuid is None:

            if not self.patient_session:
                raise ValueError(
                    "No patient session available"
                )

            patient_uuid = (
                self.patient_session[
                    "patient_uuid"
                ]
            )

        custom_view = (
            "uuid,"
            "display,"
            "program,"
            "dateEnrolled,"
            "dateCompleted,"
            "location:(uuid,display),"
            "states:("
            "startDate,"
            "endDate,"
            "voided,"
            "state:("
            "uuid,"
            "concept:(display)"
            ")"
            ")"
        )

        params = {
            "patient": patient_uuid,
            "v": f"custom:({custom_view})"
        }

        url = (
                f"{self.base_url}"
                f"/ws/rest/v1/programenrollment?"
                + urlencode(params)
        )

        return await self._get(url)

    # -------------------------------------------------
    # Current Program Details
    # -------------------------------------------------
    async def current_program_details(
            self,
            patient_uuid=None
    ):
        """
        Retrieve the patient's current KenyaEMR
        program details.
        """

        if patient_uuid is None:

            if not self.patient_session:
                raise ValueError(
                    "No patient session available"
                )

            patient_uuid = (
                self.patient_session[
                    "patient_uuid"
                ]
            )

        params = {
            "patientUuid": patient_uuid
        }

        url = (
                f"{self.base_url}"
                f"/ws/rest/v1/kenyaemr/"
                f"currentProgramDetails?"
                + urlencode(params)
        )

        return await self._get(url)

    # -------------------------------------------------
    # Last Regimen Encounter
    # -------------------------------------------------
    async def last_regimen_encounter(
            self,
            patient_uuid=None,
            category="ARV"
    ):
        """
        Retrieve the patient's latest regimen encounter.

        Default category is ARV.
        """

        if patient_uuid is None:

            if not self.patient_session:
                raise ValueError(
                    "No patient session available"
                )

            patient_uuid = (
                self.patient_session[
                    "patient_uuid"
                ]
            )

        params = {
            "patientUuid": patient_uuid,
            "category": category
        }

        url = (
                f"{self.base_url}"
                f"/ws/rest/v1/kenyaemr/"
                f"lastRegimenEncounter?"
                + urlencode(params)
        )

        return await self._get(url)

    # -------------------------------------------------
    # Patient Visits
    # -------------------------------------------------
    async def visits(
            self,
            patient_uuid=None,
            include_inactive=True,
            view="default"
    ):
        """
        Retrieve patient visit history and return only:
        - Visit date
        - Encounter/visit names

        Visits without encounters are ignored.
        """

        if patient_uuid is None:

            if not self.patient_session:
                raise ValueError(
                    "No patient session available"
                )

            patient_uuid = self.patient_session[
                "patient_uuid"
            ]

        params = {
            "patient": patient_uuid,
            "v": view,
            "includeInactive": str(
                include_inactive
            ).lower()
        }

        url = (
                f"{self.base_url}"
                f"/ws/rest/v1/visit?"
                + urlencode(params)
        )

        data = await self._get(url)

        visits = []

        for visit in data.get("results", []):

            encounters = visit.get("encounters", [])

            # Ignore visits with no encounters
            if not encounters:
                continue

            # Format visit date
            start_datetime = visit.get("startDatetime")

            if start_datetime:
                visit_date = datetime.strptime(
                    start_datetime[:19],
                    "%Y-%m-%dT%H:%M:%S"
                ).strftime("%d %b %Y")
            else:
                visit_date = None

            encounter_names = []

            for encounter in encounters:

                name = encounter.get("display", "")

                # Remove date at end:
                # "HIV Consultation 07/05/2024"
                # becomes
                # "HIV Consultation"
                name = re.sub(
                    r"\s+\d{2}/\d{2}/\d{4}$",
                    "",
                    name
                ).strip()

                if name:
                    encounter_names.append(name)

            if not encounter_names:
                continue

            visits.append({
                "date": visit_date,
                "visits": encounter_names
            })

        return visits[:2]

    # -------------------------------------------------
    # Drug Orders dispensing history
    # -------------------------------------------------
    from datetime import datetime
    from urllib.parse import urlencode

    async def drug_orders_dispensing_history(
            self,
            patient_uuid=None,
            care_setting=(
                    "6f0c9a92-6f24-11e3-af88-005056821db0"
            ),
            order_type=(
                    "131168f4-15f5-102d-96e4-000c29c2a5d7"
            ),
            exclude_discontinue_orders=True
    ):
        """
        Retrieve the 4 most recent medication orders.

        Returns clinically relevant details only:
        drug, dose, frequency, route, quantity,
        duration, refills, instructions, reason,
        status and prescriber.
        """

        if patient_uuid is None:

            if not self.patient_session:
                raise ValueError(
                    "No patient session available"
                )

            patient_uuid = self.patient_session[
                "patient_uuid"
            ]

        custom_view = (
            "orderNumber,"
            "action,"
            "dateActivated,"
            "dateStopped,"
            "autoExpireDate,"
            "orderReasonNonCoded,"
            "urgency,"
            "instructions,"
            "fulfillerStatus,"
            "drug:(display),"
            "dose,"
            "doseUnits:(display),"
            "frequency:(display),"
            "asNeeded,"
            "asNeededCondition,"
            "quantity,"
            "quantityUnits:(display),"
            "numRefills,"
            "dosingInstructions,"
            "duration,"
            "durationUnits:(display),"
            "route:(display),"
            "brandName,"
            "orderer:(person:(display))"
        )

        params = {
            "patient": patient_uuid,
            "careSetting": care_setting,
            "orderTypes": order_type,
            "v": f"custom:({custom_view})",
            "excludeDiscontinueOrders": str(
                exclude_discontinue_orders
            ).lower()
        }

        url = (
                f"{self.base_url}"
                f"/ws/rest/v1/order?"
                + urlencode(params)
        )

        data = await self._get(url)

        results = []

        for order in data.get("results", []):

            date_activated = order.get(
                "dateActivated"
            )

            if date_activated:
                date_ordered = datetime.strptime(
                    date_activated[:19],
                    "%Y-%m-%dT%H:%M:%S"
                ).strftime("%d %b %Y")
            else:
                date_ordered = None

            drug = order.get("drug") or {}
            dose_units = order.get(
                "doseUnits"
            ) or {}
            frequency = order.get(
                "frequency"
            ) or {}
            quantity_units = order.get(
                "quantityUnits"
            ) or {}
            duration_units = order.get(
                "durationUnits"
            ) or {}
            route = order.get(
                "route"
            ) or {}

            orderer = order.get(
                "orderer"
            ) or {}

            person = orderer.get(
                "person"
            ) or {}

            results.append({
                "date": date_ordered,

                "drug": drug.get(
                    "display"
                ),

                "dose": order.get(
                    "dose"
                ),

                "dose_unit": dose_units.get(
                    "display"
                ),

                "frequency": frequency.get(
                    "display"
                ),

                "route": route.get(
                    "display"
                ),

                "quantity": order.get(
                    "quantity"
                ),

                "quantity_unit": quantity_units.get(
                    "display"
                ),

                "duration": order.get(
                    "duration"
                ),

                "duration_unit": duration_units.get(
                    "display"
                ),

                "refills": order.get(
                    "numRefills"
                ),

                "instructions": (
                        order.get(
                            "dosingInstructions"
                        )
                        or order.get(
                    "instructions"
                )
                ),

                "as_needed": order.get(
                    "asNeeded"
                ),

                "as_needed_condition": order.get(
                    "asNeededCondition"
                ),

                "reason": order.get(
                    "orderReasonNonCoded"
                ),

                "status": order.get(
                    "fulfillerStatus"
                ),

                "prescriber": person.get(
                    "display"
                ),

                "_dateActivated": date_activated
            })

        # Sort newest first
        results.sort(
            key=lambda x: (
                    x.get("_dateActivated") or ""
            ),
            reverse=True
        )

        # Keep only 4 most recent
        results = results[:4]

        # Remove internal sorting field
        for order in results:
            order.pop(
                "_dateActivated",
                None
            )

        return results

    # -------------------------------------------------
    # Observation Tree
    # -------------------------------------------------
    async def viral_load_results_history(
            self,
            patient_uuid=None,
            concept=(
                    "856AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
            )
    ):
        """
        Retrieve observations for the patient
        for a specific OpenMRS concept.
        """

        if patient_uuid is None:

            if not self.patient_session:
                raise ValueError(
                    "No patient session available"
                )

            patient_uuid = (
                self.patient_session[
                    "patient_uuid"
                ]
            )

        params = {
            "patient": patient_uuid,
            "concept": concept
        }

        url = (
                f"{self.base_url}"
                f"/ws/rest/v1/obstree?"
                + urlencode(params)
        )

        return await self._get(url)

    # -------------------------------------------------
    # FHIR Encounters With Medication Requests
    # -------------------------------------------------
    async def medication_request_encounters(
            self,
            patient_search_term=None,
            status="active",
            date_from=None,
            offset=0,
            count=10
    ):
        """
        Retrieve FHIR encounters containing medication
        requests.

        patient_search_term may be a patient identifier
        or patient name.
        """
        patient_identifier = ""

        if patient_search_term is None:

            if not self.patient_session:
                raise ValueError(
                    "No patient session available"
                )

            patient_search_term = (
                self.patient_session[
                    "identifiers"
                ]
            )
            identifier = [
                item["identifier"]
                for item in patient_search_term
                if item["identifier_type"] in ["Unique Patient Number","OpenMRS ID"]
            ]
            patient_identifier = identifier[0]


        params = {
            "_query":
                "encountersWithMedicationRequests",
            "patientSearchTerm":
                patient_identifier,
            "status":
                status,
            "_summary":
                "data",
            "_getpagesoffset":
                offset,
            "_count":
                count
        }

        if date_from is not None:
            params["date"] = date_from

        url = (
                f"{self.base_url}"
                f"/ws/fhir2/R4/Encounter?"
                + urlencode(params)
        )

        return await self._get(url)


    async def patient_hiv_hts_testing_details(
            self,
            patient_uuid=None
    ):
        """
        Retrieve relevant HIV testing and linkage information
        from HTS encounters for the current patient.

        Non-HTS / non-relevant observations are ignored.
        """

        # ---------------------------------------------------------
        # 1. Get patient UUID from the current patient session
        # ---------------------------------------------------------
        if patient_uuid is None:

            if not self.patient_session:
                raise ValueError(
                    "No patient session available"
                )

            patient_uuid = (
                self.patient_session[
                    "patient_uuid"
                ]
            )

        # ---------------------------------------------------------
        # 2. HTS encounter type
        # ---------------------------------------------------------
        HTS_ENCOUNTER_TYPE = (
            "9c0a7a57-62ff-4f75-babe-5835b0e921b7"
        )

        # ---------------------------------------------------------
        # 3. Only keep relevant HIV testing / linkage fields
        # ---------------------------------------------------------
        HTS_FIELDS = {

            # HIV testing
            "Result of HIV test":
                "hiv_result",

            "HIV test performed":
                "test_performed",

            "Received HIV test result":
                "received_result",

            "HIV testing services strategy":
                "testing_strategy",

            "Provider type":
                "provider_type",

            "Patient tested as":
                "testing_type",

            "point of HIV testing":
                "testing_point",

            "Setting of the last HIV test":
                "last_test_setting",

            "Patient had HIV self test":
                "self_tested",

            # Referral / enrolment
            "Reasons for Referral":
                "referral_reason",

            "Method of enrollment":
                "enrollment_method",

            "Person enrolled in program":
                "enrolled_in_program",

            "Referred for preventive services":
                "referred_for_prevention",

            # TB
            "Tuberculosis disease status":
                "tb_status",

            # Facility / linkage
            "Health facility name":
                "facility",

            "Facility of HIV Care":
                "hiv_care_facility",

            "Date enrolled in HIV care":
                "hiv_care_enrollment_date",

            "Antiretroviral treatment start date":
                "art_start_date",

            "Comprehensive care center number":
                "ccc_number",

            # Important clinical / linkage note
            "General examination (text)":
                "clinical_note",
        }

        # ---------------------------------------------------------
        # 4. OpenMRS custom representation
        # ---------------------------------------------------------
        representation = (
            "custom:("
            "uuid,"
            "encounterDatetime,"
            "encounterType,"
            "location:(uuid,name),"
            "patient:(uuid,display),"
            "encounterProviders:("
            "uuid,"
            "provider:(uuid,name)"
            "),"
            "obs:("
            "uuid,"
            "obsDatetime,"
            "voided,"
            "groupMembers,"
            "concept:(uuid,name:(uuid,name)),"
            "value:("
            "uuid,"
            "name:(uuid,name),"
            "names:(uuid,conceptNameType,name)"
            ")"
            "),"
            "form:(uuid,name)"
            ")"
        )

        params = {
            "encounterType": HTS_ENCOUNTER_TYPE,
            "patient": patient_uuid,
            "v": representation,
            "limit": 100
        }

        url = (
                f"{self.base_url}"
                f"/ws/rest/v1/encounter?"
                + urlencode(
            params,
            safe="(),:"
        )
        )

        response = await self._get(url)

        if not isinstance(response, dict):
            return {
                "patient_uuid": patient_uuid,
                "encounters": []
            }

        encounters = response.get(
            "results",
            []
        )

        # ---------------------------------------------------------
        # Helper: get observation concept name
        # ---------------------------------------------------------
        def get_concept_name(obs):

            concept = (
                    obs.get("concept")
                    or {}
            )

            # groupMembers normally use "display"
            if concept.get("display"):
                return concept["display"]

            name = concept.get("name")

            if isinstance(name, dict):
                return (
                        name.get("name")
                        or name.get("display")
                )

            if isinstance(name, str):
                return name

            return None

        # ---------------------------------------------------------
        # Helper: simplify OpenMRS values
        # ---------------------------------------------------------
        def get_value(value):

            if value is None:
                return None

            # Normal primitive values
            if isinstance(
                    value,
                    (
                            str,
                            int,
                            float,
                            bool
                    )
            ):
                return value

            # Coded OpenMRS concept
            if isinstance(value, dict):

                if value.get("display") is not None:
                    return value["display"]

                name = value.get("name")

                if isinstance(name, dict):
                    return (
                            name.get("name")
                            or name.get("display")
                    )

                if isinstance(name, str):
                    return name

                return value.get("uuid")

            return str(value)

        # ---------------------------------------------------------
        # Helper: HIV test kit/result construct
        # ---------------------------------------------------------
        def extract_test_group(obs):

            members = (
                    obs.get("groupMembers")
                    or []
            )

            test = {}

            for member in members:

                if member.get("voided"):
                    continue

                label = get_concept_name(
                    member
                )

                value = get_value(
                    member.get("value")
                )

                if not label or value is None:
                    continue

                label_lower = label.lower()

                if "test kit lot number" in label_lower:

                    test[
                        "lot_number"
                    ] = value

                elif "hiv test kit used" in label_lower:

                    test[
                        "kit"
                    ] = value

                elif "expiration date" in label_lower:

                    test[
                        "expiry_date"
                    ] = value

                # KenyaEMR uses several different concepts
                # for Test 1 / Test 2 / Test 3 results.
                elif (
                        "result" in label_lower
                        or "pcr" in label_lower
                        or "rapid test" in label_lower
                ):

                    test[
                        "result_type"
                    ] = label

                    test[
                        "result"
                    ] = value

            if test:
                return test

            return None

        # ---------------------------------------------------------
        # 5. Filter the HTS encounters
        # ---------------------------------------------------------
        filtered_encounters = []

        for encounter in encounters:

            providers = (
                    encounter.get(
                        "encounterProviders"
                    )
                    or []
            )

            provider_name = None

            if providers:
                provider_name = (
                    providers[0]
                    .get(
                        "provider",
                        {}
                    )
                    .get("name")
                )

            record = {

                "encounter_uuid":
                    encounter.get("uuid"),

                "encounter_datetime":
                    encounter.get(
                        "encounterDatetime"
                    ),

                "form":
                    (
                            encounter.get("form")
                            or {}
                    ).get("name"),

                "location":
                    (
                            encounter.get("location")
                            or {}
                    ).get("name"),

                "provider":
                    provider_name,
            }

            tests = []

            # -----------------------------------------------------
            # Process observations
            # -----------------------------------------------------
            for obs in (
                    encounter.get("obs")
                    or []
            ):

                # Ignore deleted / voided observations
                if obs.get("voided"):
                    continue

                concept_name = (
                    get_concept_name(
                        obs
                    )
                )

                if not concept_name:
                    continue

                # ---------------------------------------------
                # Standard HIV fields
                # ---------------------------------------------
                if concept_name in HTS_FIELDS:

                    field_name = (
                        HTS_FIELDS[
                            concept_name
                        ]
                    )

                    record[
                        field_name
                    ] = get_value(
                        obs.get("value")
                    )

                # ---------------------------------------------
                # HIV test kits/results
                # ---------------------------------------------
                elif (
                        concept_name
                        == "Test laboratory number construct"
                ):

                    test = (
                        extract_test_group(
                            obs
                        )
                    )

                    if test:
                        tests.append(
                            test
                        )

            if tests:
                record[
                    "tests"
                ] = tests

            # -----------------------------------------------------
            # Only return encounters having useful HTS information
            # -----------------------------------------------------
            metadata_fields = {
                "encounter_uuid",
                "encounter_datetime",
                "form",
                "location",
                "provider",
            }

            useful_fields = (
                    set(record.keys())
                    - metadata_fields
            )

            if useful_fields:
                filtered_encounters.append(
                    record
                )

        # Latest encounter first
        filtered_encounters.sort(
            key=lambda x: (
                    x.get(
                        "encounter_datetime"
                    )
                    or ""
            ),
            reverse=True
        )

        return {
            "patient_uuid": patient_uuid,
            "encounters": filtered_encounters
        }


    async def patient_treatment_hiv_defaulter_tracing(
            self,
            patient_uuid=None
    ):
        """

        Retrieve relevant HIV treatment defaulter tracing history
        from CCC Defaulter Tracing encounters.

        Irrelevant observations are ignored.

        """

        # ---------------------------------------------------------
        # Get patient UUID from current session
        # ---------------------------------------------------------
        if patient_uuid is None:

            if not self.patient_session:
                raise ValueError(
                    "No patient session available"
                )

            patient_uuid = (
                self.patient_session[
                    "patient_uuid"
                ]
            )

        # ---------------------------------------------------------
        # CCC Defaulter Tracing encounter type
        # ---------------------------------------------------------
        encounter_type = (
            "1495edf8-2df2-11e9-b210-d663bd873d93"
        )

        # ---------------------------------------------------------
        # Only relevant HIV treatment / tracing fields
        # ---------------------------------------------------------
        TRACING_FIELDS = {

            "Procedure outcome":
                "procedure_outcome",

            "Procedure comment":
                "procedure_comment",

            "Treatment sequence number":
                "treatment_sequence_number",

            "Test status":
                "tracing_status",

            "Date of last patient visit":
                "last_patient_visit",

            "Mode of client tracing":
                "tracing_mode",

            "Reason for failed contact tracing":
                "failed_tracing_reason",

            "REASON(S) FOR NOT RECEIVING CARE AT HOSPITAL":
                "reason_not_receiving_care",

            "Reason for discontinuing service (text)":
                "discontinuation_reason",

            "Treatment start date":
                "treatment_start_date",
        }

        # ---------------------------------------------------------
        # Custom OpenMRS representation
        # ---------------------------------------------------------
        representation = (
            "custom:("
            "uuid,"
            "encounterDatetime,"
            "encounterType,"
            "location:(uuid,name),"
            "patient:(uuid,display),"
            "encounterProviders:("
                "uuid,"
                "provider:(uuid,name)"
            "),"
            "obs:("
                "uuid,"
                "obsDatetime,"
                "voided,"
                "groupMembers,"
                "concept:(uuid,name:(uuid,name)),"
                "value:("
                    "uuid,"
                    "name:(uuid,name),"
                    "names:(uuid,conceptNameType,name)"
                ")"
            "),"
            "form:(uuid,name)"
            ")"
        )

        params = {
            "encounterType": encounter_type,
            "patient": patient_uuid,
            "v": representation,
            "limit": 200,
        }

        url = (
            f"{self.base_url}"
            f"/ws/rest/v1/encounter?"
            + urlencode(params)
        )

        response = await self._get(url)

        if not isinstance(response, dict):
            return {
                "patient_uuid": patient_uuid,
                "tracing_history": []
            }

        encounters = response.get(
            "results",
            []
        )

        # ---------------------------------------------------------
        # Convert OpenMRS coded values to readable values
        # ---------------------------------------------------------
        def get_value(value):

            if value is None:
                return None

            # String, date, number, boolean
            if isinstance(
                value,
                (
                    str,
                    int,
                    float,
                    bool
                )
            ):
                return value

            # OpenMRS coded concept
            if isinstance(value, dict):

                name = value.get("name")

                if isinstance(name, dict):

                    readable_name = (
                        name.get("name")
                        or name.get("display")
                    )

                    if readable_name:
                        return readable_name

                if isinstance(name, str):
                    return name

                if value.get("display"):
                    return value.get(
                        "display"
                    )

                return value.get(
                    "uuid"
                )

            return str(value)

        # ---------------------------------------------------------
        # Get observation concept name
        # ---------------------------------------------------------
        def get_concept_name(obs):

            concept = (
                obs.get("concept")
                or {}
            )

            concept_name = (
                concept.get("name")
                or {}
            )

            if isinstance(
                concept_name,
                dict
            ):
                return (
                    concept_name.get("name")
                    or concept_name.get(
                        "display"
                    )
                )

            if isinstance(
                concept_name,
                str
            ):
                return concept_name

            return concept.get(
                "display"
            )

        tracing_history = []

        # ---------------------------------------------------------
        # Process each tracing encounter
        # ---------------------------------------------------------
        for encounter in encounters:

            providers = (
                encounter.get(
                    "encounterProviders"
                )
                or []
            )

            provider_name = None

            if providers:

                provider = (
                    providers[0]
                    .get(
                        "provider"
                    )
                    or {}
                )

                provider_name = (
                    provider.get(
                        "name"
                    )
                )

            patient = (
                encounter.get(
                    "patient"
                )
                or {}
            )

            location = (
                encounter.get(
                    "location"
                )
                or {}
            )

            form = (
                encounter.get(
                    "form"
                )
                or {}
            )

            record = {

                "encounter_uuid":
                    encounter.get(
                        "uuid"
                    ),

                "encounter_datetime":
                    encounter.get(
                        "encounterDatetime"
                    ),

                "patient_uuid":
                    patient.get(
                        "uuid"
                    ),

                "patient":
                    patient.get(
                        "display"
                    ),

                "location":
                    location.get(
                        "name"
                    ),

                "provider":
                    provider_name,

                "form":
                    form.get(
                        "name"
                    ),
            }

            # -----------------------------------------------------
            # Filter observations
            # -----------------------------------------------------
            for obs in (
                encounter.get("obs")
                or []
            ):

                # Ignore deleted observations
                if obs.get(
                    "voided"
                ):
                    continue

                concept_name = (
                    get_concept_name(
                        obs
                    )
                )

                if not concept_name:
                    continue

                # Ignore everything not relevant
                if concept_name not in TRACING_FIELDS:
                    continue

                field_name = (
                    TRACING_FIELDS[
                        concept_name
                    ]
                )

                value = get_value(
                    obs.get(
                        "value"
                    )
                )

                if value is not None:

                    record[
                        field_name
                    ] = value

            # -----------------------------------------------------
            # Only include encounter if it contains tracing data
            # -----------------------------------------------------
            metadata_fields = {
                "encounter_uuid",
                "encounter_datetime",
                "patient_uuid",
                "patient",
                "location",
                "provider",
                "form",
            }

            tracing_fields_found = (
                set(record.keys())
                - metadata_fields
            )

            if tracing_fields_found:

                tracing_history.append(
                    record
                )

        # ---------------------------------------------------------
        # Latest tracing encounter first
        # ---------------------------------------------------------
        tracing_history.sort(
            key=lambda item: (
                item.get(
                    "encounter_datetime"
                )
                or ""
            ),
            reverse=True
        )

        return tracing_history







