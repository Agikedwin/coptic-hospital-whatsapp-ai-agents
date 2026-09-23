# Hospital WhatsApp AI Agent

## FastAPI + OpenMRS + WhatsApp Cloud API + RAG

A hospital-wide conversational AI platform that allows patients, healthcare workers, counsellors and other authorized users to interact with hospital services through **WhatsApp**.

The system uses:

* **WhatsApp Cloud API** as the primary conversation interface
* **Python + FastAPI** as the application and integration backend
* **OpenMRS** as the main clinical system of record
* An **AI agent / LLM** for conversation understanding, reasoning and tool selection
* **RAG — Retrieval-Augmented Generation** for answers grounded in approved clinical and operational documents
* Controlled **OpenMRS and hospital tools** for retrieving or recording authorized information
* Structured **conversation state and memory**
* Clinical **safety rules and guardrails**
* **Human escalation** when automated support is insufficient or inappropriate
* Optional supporting databases such as MySQL/PostgreSQL for agent state, audit logs, referrals, messaging state and other application-level data

The project is **not limited to Family Planning**.

Family Planning is one supported clinical domain within a broader hospital-wide architecture.

---

# 1. Core Architecture

The user interacts with the system through an ordinary WhatsApp conversation.

Behind the scenes:

```text
USER
  │
  │ WhatsApp Message
  ▼
WHATSAPP CLOUD API
  │
  │ Webhook
  ▼
FASTAPI BACKEND
  │
  ▼
IDENTITY / CONSENT / SESSION LAYER
  │
  ▼
AI AGENT
  │
  ├── LLM reasoning
  ├── Instructions and guardrails
  ├── Intent classification
  ├── Conversation state
  ├── Memory
  ├── Tool selection
  └── Safety validation
       │
       ├───────────────┬────────────────┬────────────────┐
       ▼               ▼                ▼                ▼
    OpenMRS           RAG          Hospital Tools    External APIs
       │               │                │
       │               │                ├── Facility directory
       │               │                ├── Referral service
       │               │                ├── Appointments
       │               │                ├── Follow-up
       │               │                └── Human escalation
       │               │
       ▼               ▼
Patient Clinical    Approved Clinical
Information        Knowledge
       │               │
       └───────┬───────┘
               ▼
        RESPONSE VALIDATION
               │
               ▼
        FASTAPI BACKEND
               │
               ▼
       WHATSAPP CLOUD API
               │
               ▼
              USER
```

WhatsApp is therefore only the **conversation channel**.

The actual application intelligence runs on the hospital backend.

---

# 2. System Purpose

The objective of the platform is to provide a controlled conversational interface between users and hospital services.

The AI agent may:

* Answer approved health-information questions
* Retrieve authorized patient information from OpenMRS
* Retrieve appointment information
* Support clinic navigation
* Provide health education
* Support Family Planning counselling
* Support HIV prevention information including PrEP and PEP
* Support ART-related service navigation
* Support adherence and treatment-literacy workflows
* Retrieve relevant historical patient information when permitted
* Provide laboratory-service guidance
* Support pharmacy and refill workflows
* Support maternal and child health information
* Provide referral guidance
* Record or initiate referrals
* Schedule or record follow-up
* Identify potential clinical red flags
* Escalate a user to an appropriate healthcare worker
* Support structured follow-up questionnaires
* Send approved reminders where permitted
* Support other hospital programmes through additional controlled tools

The system should not allow the LLM to directly manipulate hospital systems without going through defined, validated tools.

---

# 3. OpenMRS as the Clinical Backend

**OpenMRS is the primary clinical system of record.**

Patient clinical information should normally be retrieved from or written to OpenMRS through controlled application services.

Examples include:

```text
Patient search
Patient demographics
Patient summary
Encounter history
Program enrolment
Program status
Appointments
Clinical observations
Medication information
Historical enrolment
Laboratory information
Referral information
```

The AI model should **not receive unrestricted database access**.

Instead, the agent calls approved FastAPI tools.

Example:

```text
User:
"When is my next appointment?"

        ↓

AI Agent identifies intent:
appointment_lookup

        ↓

FastAPI tool:
get_patient_next_appointment()

        ↓

OpenMRS

        ↓

Structured result

        ↓

Agent produces user-friendly response

        ↓

WhatsApp
```

---

# 4. OpenMRS Tool Layer

OpenMRS operations should be exposed internally as controlled tools.

Examples:

```python
search_patient()
get_patient_summary()
get_patient_encounters()
get_current_program()
get_program_enrollment()
get_patient_appointments()
get_patient_medications()
get_recent_lab_results()
get_referral_status()
```

Each tool should:

1. Accept only required parameters.
2. Verify authentication and authorization.
3. Validate the patient's identity where necessary.
4. Return structured information.
5. Limit information to what is required for the current task.
6. Log relevant access.
7. Handle OpenMRS errors safely.
8. Avoid exposing raw OpenMRS responses directly to WhatsApp users.

---

# 5. WhatsApp Cloud API

WhatsApp Cloud API is the principal patient-facing communication channel.

The FastAPI application exposes a webhook that receives incoming WhatsApp events.

Typical flow:

```text
WhatsApp User
      ↓
Meta WhatsApp Cloud API
      ↓
POST /webhooks/whatsapp
      ↓
Validate webhook
      ↓
Extract sender identifier
      ↓
Resolve internal user/session
      ↓
Process message
      ↓
Run AI agent
      ↓
Validate response
      ↓
Send through WhatsApp Cloud API
```

A WhatsApp phone number should be treated as a **message-delivery identifier**, not as the complete patient identity.

Where access to personal clinical data is required, the application should perform the appropriate patient verification, authorization and consent checks.

---

# 6. AI Agent

The AI component should behave as an **agent**, rather than as a simple chatbot.

A simple chatbot normally follows:

```text
Question
   ↓
LLM
   ↓
Answer
```

This project follows:

```text
User message
      ↓
Understand intent
      ↓
Determine context
      ↓
Determine whether patient information is required
      ↓
Choose appropriate tool
      ↓
Retrieve information
      ↓
Retrieve approved clinical guidance if required
      ↓
Evaluate result
      ↓
Apply safety rules
      ↓
Respond / Refer / Escalate / Follow up
```

The agent may therefore:

* Answer
* Retrieve
* Search
* Refer
* Record
* Schedule
* Escalate
* Request additional information
* Trigger approved workflow actions

---

# 7. RAG — Approved Clinical Knowledge

Clinical responses should not depend only on the LLM's general knowledge.

The project should maintain a curated and version-controlled **RAG knowledge base**.

Approved documents may include:

* Kenya Ministry of Health guidelines
* NASCOP HIV prevention and treatment guidance
* Kenya Family Planning guidelines
* WHO clinical guidance
* Coptic Mission Hospital SOPs
* Pharmacy SOPs
* Laboratory SOPs
* HIV programme SOPs
* PrEP and PEP guidance
* ART treatment guidance
* Viral-load protocols
* STI guidance
* Maternal and child health protocols
* Adolescent health protocols
* Safeguarding protocols
* Referral pathways
* Facility directories
* Frequently asked questions approved by clinicians
* Patient education materials

Typical workflow:

```text
WhatsApp Question
       ↓
Intent Classification
       ↓
Clinical Information Required?
       ↓
Retrieve Approved Documents
       ↓
Return Relevant Sections
       ↓
Agent Reasons Over Retrieved Evidence
       ↓
Clinical Safety Validation
       ↓
WhatsApp Response
```

Documents loaded into the clinical RAG environment should be:

* Approved
* Version controlled
* Traceable to their source
* Dated
* Reviewed when guidance changes

---

# 8. Hospital-Wide Clinical Domains

The architecture should support multiple hospital programmes rather than creating a separate AI application for each service.

Possible domains include:

### HIV Services

* HIV testing information
* HIV prevention
* PrEP
* PEP
* ART treatment support
* Viral-load education
* Adherence support
* Treatment literacy
* Appointment reminders
* Differentiated service-delivery information
* Referral and linkage
* Retention support

### Family Planning

* Contraceptive-method information
* Eligibility counselling
* Side-effect information
* Method continuation
* Method switching
* Follow-up
* Referral
* Facility availability

### Maternal and Child Health

* ANC information
* PNC information
* PMTCT support
* Immunization information
* Danger-sign education
* Clinic navigation

### Pharmacy

* Refill information
* Medication instructions
* Pharmacy appointment information
* Adherence reminders
* Referral to pharmacy staff
* Medication-related escalation

### Laboratory

* Sample-related information
* Test availability
* Result workflow information
* Laboratory appointments
* Appropriate retrieval of authorized results

### General Outpatient Services

* Clinic information
* Appointment assistance
* Referral
* Health education
* Facility navigation

Additional services can be added by creating new tools and approved knowledge collections without changing the overall WhatsApp architecture.

---

# 9. Example: PrEP Interaction

Example:

```text
User:
"Can I qualify for PrEP?"
```

The agent may:

1. Identify the request as an HIV-prevention / PrEP question.
2. Retrieve the approved current NASCOP/WHO PrEP guidance.
3. Ask only the clinically relevant questions required.
4. Determine whether there may have been an HIV exposure within the previous 72 hours.
5. If appropriate, distinguish a potential PEP pathway from routine PrEP.
6. Provide approved information.
7. Recommend HIV testing or clinical assessment where required.
8. Provide a facility/referral option.
9. Escalate to a healthcare worker where clinical assessment is required.

The agent should not independently diagnose the patient or make unsafe treatment decisions.

---

# 10. Example: Family Planning Interaction

```text
User:
"I started taking pills and now I am bleeding. Is this normal?"
```

Possible workflow:

```text
MESSAGE
   ↓
CLASSIFY SITUATION
   ↓
Identify contraceptive method
   ↓
Retrieve approved FP guidance
   ↓
Check relevant history/state
   ↓
Assess safety/red-flag rules
   │
   ├───────────────────┐
   ▼                   ▼
Routine issue      Possible red flag
   │                   │
   ▼                   ▼
RAG guidance      Safety protocol
   │                   │
   ▼                   ▼
Respond           Human escalation
```

---

# 11. Memory and Conversation State

The application should maintain structured state so that users do not have to repeat information unnecessarily.

Example:

```text
User:
"I am interested in implants."

Later:
"What side effects does it have?"

Later:
"Where can I get one?"
```

The system should understand that **"it"** and **"one"** refer to the contraceptive implant.

Possible application state:

| Data element                | Purpose                                                          |
| --------------------------- | ---------------------------------------------------------------- |
| Internal user ID            | Stable identity inside the application                           |
| WhatsApp number             | Message-delivery identifier                                      |
| OpenMRS patient UUID        | Links a verified user with the clinical record where appropriate |
| Conversation state          | Current conversation context                                     |
| Recent conversation summary | Supports follow-up questions                                     |
| Current topic               | FP, HIV, pharmacy, laboratory, etc.                              |
| Consent state               | Records required consent decisions                               |
| Referral state              | Tracks referrals                                                 |
| Follow-up state             | Tracks planned follow-up                                         |
| Escalation state            | Tracks human-provider involvement                                |

Clinical information should remain in the appropriate clinical system wherever possible.

---

# 12. Supporting Application Database

This project may use MySQL, PostgreSQL or another application database.

However, this database is **not intended to replace OpenMRS as the hospital clinical record**.

It may store application-level information such as:

```text
users
whatsapp_sessions
conversation_state
conversation_summaries
agent_events
tool_calls
referrals
followups
escalations
message_status
consent_records
audit_events
rag_documents
rag_document_versions
rag_retrieval_logs
```

Any duplication of clinical information should be minimized.

---

# 13. Human Escalation

The system must support escalation to a human provider.

Examples include:

* Medical emergencies
* Possible serious adverse events
* Clinical red flags
* Suspected acute HIV infection
* Possible recent HIV exposure requiring urgent PEP assessment
* Complex medication questions
* Symptoms requiring examination
* Mental-health emergencies
* Safeguarding concerns
* Gender-based violence or sexual violence
* Cases where the system lacks sufficient information
* User requests to speak to a human provider

Example:

```text
AI Agent
   ↓
Safety condition detected
   ↓
request_human_provider()
   ↓
Create escalation record
   ↓
Notify designated provider/work queue
   ↓
Send appropriate WhatsApp response
```

---

# 14. Agent Tools

Initial controlled tools may include:

```python
tools = [
    # Clinical knowledge
    search_clinical_guidelines,

    # OpenMRS
    search_patient,
    get_patient_summary,
    get_patient_encounters,
    get_current_program,
    get_patient_appointments,
    get_patient_medications,
    get_recent_lab_results,

    # Hospital operations
    find_nearest_facility,
    check_clinic_hours,
    check_service_availability,

    # Referrals
    create_referral,
    get_referral_status,

    # Human support
    request_human_provider,

    # State
    retrieve_relevant_history,

    # Follow-up
    schedule_follow_up,
]
```

Begin with a small number of well-tested tools and expand gradually.

---

# 15. Recommended Project Structure

```text
hospital_whatsapp_ai/
│
├── app/
│   ├── main.py
│   ├── settings.py
│   ├── dependencies.py
│   │
│   ├── api/
│   │   ├── health.py
│   │   ├── whatsapp.py
│   │   └── internal.py
│   │
│   ├── whatsapp/
│   │   ├── webhook.py
│   │   ├── parser.py
│   │   ├── sender.py
│   │   ├── templates.py
│   │   └── security.py
│   │
│   ├── agent/
│   │   ├── agent.py
│   │   ├── instructions.py
│   │   ├── context.py
│   │   ├── memory.py
│   │   ├── safety.py
│   │   └── tools.py
│   │
│   ├── openmrs/
│   │   ├── client.py
│   │   ├── auth.py
│   │   ├── patients.py
│   │   ├── encounters.py
│   │   ├── programs.py
│   │   ├── appointments.py
│   │   └── medications.py
│   │
│   ├── rag/
│   │   ├── loader.py
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   └── vector_store.py
│   │
│   ├── services/
│   │   ├── referrals.py
│   │   ├── followups.py
│   │   ├── facilities.py
│   │   ├── escalation.py
│   │   └── consent.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   └── security/
│       ├── privacy.py
│       ├── authorization.py
│       └── audit.py
│
├── knowledge_base/
│   ├── national_guidelines/
│   ├── who_guidelines/
│   ├── hospital_sops/
│   └── approved_faqs/
│
├── scripts/
│   ├── build_vector_db.py
│   └── initialize_database.py
│
├── tests/
│   ├── test_whatsapp.py
│   ├── test_openmrs.py
│   ├── test_agent.py
│   ├── test_rag.py
│   ├── test_safety.py
│   └── test_tools.py
│
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

The precise folder structure may be adjusted as the implementation evolves.

---

# 16. Environment Configuration

Copy the environment template:

```bash
cp .env.example .env
```

Example configuration:

```dotenv
# --------------------------------------------------
# APPLICATION
# --------------------------------------------------

APP_NAME=Hospital WhatsApp AI Agent
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000

# --------------------------------------------------
# OPENMRS
# --------------------------------------------------

OPENMRS_BASE_URL=https://your-openmrs-server/openmrs
OPENMRS_USERNAME=your_service_account
OPENMRS_PASSWORD=your_secure_password

# --------------------------------------------------
# WHATSAPP CLOUD API
# --------------------------------------------------

WHATSAPP_API_VERSION=your_meta_api_version
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_ACCESS_TOKEN=your_access_token
WHATSAPP_VERIFY_TOKEN=your_verify_token
WHATSAPP_APP_SECRET=your_app_secret

# --------------------------------------------------
# AI
# --------------------------------------------------

OPENAI_API_KEY=your_api_key
OPENAI_MODEL=your_configured_model

# --------------------------------------------------
# RAG / VECTOR DATABASE
# --------------------------------------------------

VECTOR_DB_PATH=./vector_db

# --------------------------------------------------
# APPLICATION DATABASE
# --------------------------------------------------

DATABASE_URL=mysql+pymysql://user:password@127.0.0.1/hospital_ai

# --------------------------------------------------
# SECURITY
# --------------------------------------------------

SECRET_KEY=replace_with_secure_secret
```

Never commit `.env` or production credentials to source control.

---

# 17. Installation

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 18. Build the Clinical Knowledge Base

After placing approved documents in the configured knowledge directories:

```bash
python scripts/build_vector_db.py
```

If the existing script is located at project root:

```bash
python build_vector_db.py
```

The RAG index should be rebuilt when approved source documents are added, replaced or retired.

---

# 19. Start FastAPI

```bash
uvicorn app.main:app --reload
```

Production deployments should not use `--reload`.

Useful local URLs:

* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`
* Health: `http://127.0.0.1:8000/health`

---

# 20. Expose Development Webhook

For development only, a secure public tunnel can be used:

```bash
ngrok http 8000
```

Example webhook:

```text
https://your-ngrok-domain.ngrok-free.app/webhooks/whatsapp
```

Configure this URL in the Meta WhatsApp application.

Production systems should use a stable HTTPS domain rather than a temporary development tunnel.

---

# 21. WhatsApp Webhook

Recommended endpoints:

```http
GET  /webhooks/whatsapp
POST /webhooks/whatsapp
```

### GET

Used by Meta to verify the webhook.

### POST

Receives:

* Incoming messages
* Interactive message responses
* Delivery status updates
* Read status updates
* Other subscribed WhatsApp events

The application should validate incoming webhook requests before processing them.

---

# 22. Basic Backend Flow

Conceptually:

```python
user_message = whatsapp_message

internal_user = resolve_internal_user(
    whatsapp_number=sender_number
)

agent_response = agent.run(
    user_id=internal_user.id,
    message=user_message
)

send_to_whatsapp(
    recipient=sender_number,
    message=agent_response
)
```

In the real application, `agent.run()` represents considerably more than one LLM call.

It may:

```text
Retrieve conversation state
        ↓
Classify the user's request
        ↓
Determine authorization requirements
        ↓
Retrieve approved knowledge
        ↓
Call OpenMRS
        ↓
Call hospital tools
        ↓
Evaluate results
        ↓
Run safety checks
        ↓
Determine whether escalation is required
        ↓
Generate response
```

---

# 23. Example OpenMRS Patient Flow

```text
User:
"Show me my next appointment."

        ↓

Resolve WhatsApp session
        ↓

Patient identity already verified?
        │
   ┌────┴────┐
   │         │
  NO        YES
   │         │
   ▼         ▼
Verify     Continue
Identity
   │
   └────┬────┘
        ▼
Retrieve OpenMRS patient UUID
        ↓
Call appointment tool
        ↓
OpenMRS
        ↓
Return structured result
        ↓
Apply privacy rules
        ↓
Generate patient-friendly response
        ↓
WhatsApp
```

---

# 24. API Endpoints

Application routes should generally be grouped under:

```text
/api/v1
```

Examples:

```http
GET  /health

GET  /webhooks/whatsapp
POST /webhooks/whatsapp

GET  /api/v1/patients/search
GET  /api/v1/patients/{uuid}/summary
GET  /api/v1/patients/{uuid}/appointments
GET  /api/v1/patients/{uuid}/encounters
GET  /api/v1/patients/{uuid}/programs

POST /api/v1/referrals
GET  /api/v1/referrals/{id}

POST /api/v1/followups

POST /api/v1/escalations

POST /api/v1/agent/chat
```

Internal endpoints containing clinical information should be appropriately authenticated and should not automatically be exposed publicly.

---

# 25. WhatsApp Business Configuration

Meta Developer resources:

### WhatsApp Business settings

https://developers.facebook.com/apps/961273237022140/use_cases/customize/wa-settings/?use_case_enum=WHATSAPP_BUSINESS_MESSAGING&product_route=whatsapp-business&business_id=1608810040642467&selected_tab=wa-settings

### WhatsApp Development Console

https://developers.facebook.com/apps/961273237022140/use_cases/customize/wa-dev-console/?use_case_enum=WHATSAPP_BUSINESS_MESSAGING&product_route=whatsapp-business&business_id=1608810040642467&selected_tab=wa-dev-console

### WhatsApp API Testing

https://developers.facebook.com/apps/1104039355981930/whatsapp-business/api-testing-v2/?business_id=2273437143196944

Access to these pages depends on the Meta account permissions assigned to the relevant application and business account.

---

# 26. WhatsApp Messaging Rules

Design separately for:

### User-Initiated Conversations

The patient sends a message and the system responds through the WhatsApp Business Platform according to the applicable messaging rules.

### Proactive Messages

Examples include:

* Follow-up reminders
* Appointments
* Medication reminders
* Referral reminders
* Adherence follow-up
* FP continuation follow-up
* PrEP continuation follow-up
* Patient surveys

Proactive messages must comply with current WhatsApp Business Platform requirements, including approved templates where required.

Do not hard-code WhatsApp policy assumptions that may later change.

---

# 27. Security and Privacy

Because this platform may process health information, security must be designed into every layer.

At minimum:

* Use HTTPS
* Validate WhatsApp webhook requests
* Keep secrets outside source code
* Use secure service accounts for OpenMRS
* Apply least-privilege access
* Verify identity before exposing patient-specific information
* Maintain consent where required
* Log clinical-data access appropriately
* Avoid unnecessary storage of health information
* Encrypt sensitive stored information
* Protect backups
* Restrict administrative interfaces
* Separate production and development environments
* Never expose internal stack traces to WhatsApp users
* Never place API keys or passwords inside messages
* Minimize data sent to AI models
* Avoid placing unnecessary patient identifiers in prompts
* Apply retention and deletion policies
* Maintain audit trails for sensitive actions

---

# 28. Clinical Safety

The platform should distinguish between:

```text
INFORMATION
     ↓
GENERAL GUIDANCE
     ↓
PATIENT-SPECIFIC INFORMATION
     ↓
CLINICAL ASSESSMENT REQUIRED
     ↓
URGENT / EMERGENCY ESCALATION
```

Clinical answers should be grounded in approved RAG documents whenever relevant.

The system should contain explicit rules covering:

* Emergencies
* Red flags
* Medication safety
* Possible adverse events
* Possible acute HIV infection
* PEP urgency
* Pregnancy-related danger signs
* Severe symptoms
* Safeguarding
* Sexual violence
* Self-harm or crisis situations
* Requests requiring physical examination
* Situations requiring laboratory or clinical assessment

The AI agent should not replace a clinician.

---

# 29. Data Minimization

Only retrieve the information needed to complete the current task.

For example:

If the user asks:

```text
"When is my next appointment?"
```

the agent normally does not require:

```text
Complete clinical history
Complete medication history
All laboratory results
All diagnoses
Every OpenMRS encounter
```

Instead it should retrieve only the minimum information necessary to answer the question safely.

---

# 30. Logging and Observability

Recommended observability includes:

* Request ID
* Internal user ID
* Conversation/session ID
* Intent
* Tools called
* Tool outcome
* OpenMRS response status
* RAG sources retrieved
* Safety decisions
* Escalation events
* WhatsApp send status
* Error category
* Processing duration

Sensitive clinical values should not automatically be placed in application logs.

---

# 31. Testing

Run:

```bash
pytest -q
```

Recommended tests include:

```text
WhatsApp webhook verification
WhatsApp signature validation
Message parsing
Internal user resolution
OpenMRS authentication
OpenMRS patient search
OpenMRS timeout handling
Agent intent classification
Tool selection
RAG retrieval
Clinical source grounding
Red-flag detection
Human escalation
Consent checks
Authorization
Prompt-injection resistance
Sensitive-information leakage
Follow-up workflow
Referral creation
Multi-user session separation
```

---

# 32. Docker

The system may be started using:

```bash
docker compose up --build
```

The Docker environment may contain:

```text
FastAPI application
Application database
Vector database / RAG services
Supporting workers
```

OpenMRS may remain an external hospital service rather than being recreated inside this application's Docker environment.

---

# 33. Development Principles

### 1. OpenMRS remains the clinical source of truth

Do not create parallel patient records inside the AI application unnecessarily.

### 2. WhatsApp is an interface

Do not place business logic inside WhatsApp-specific code.

### 3. FastAPI performs orchestration

FastAPI connects:

```text
WhatsApp
OpenMRS
AI
RAG
Hospital tools
Application state
```

### 4. The LLM does not receive unrestricted system access

Every action must pass through a controlled tool.

### 5. RAG grounds clinical information

Use approved and version-controlled guidance.

### 6. Patient identity and WhatsApp identity are not automatically the same thing

Verification is required before sensitive patient information is disclosed.

### 7. Human providers remain part of the workflow

The system must know when to escalate.

### 8. Start with one reliable agent

Avoid unnecessary multi-agent complexity during the initial implementation.

---

# 34. Development Roadmap

## Phase 1 — Core WhatsApp Agent

Implement:

* WhatsApp Cloud API webhook
* FastAPI
* One AI agent
* Basic conversation state
* RAG
* Selected OpenMRS read tools
* Safety rules
* Human escalation

## Phase 2 — Structured Hospital Workflows

Add:

* Referrals
* Follow-up
* Appointment workflows
* Facility directory
* Service availability
* Stronger audit logging
* Evaluation and observability
* Selected OpenMRS write operations

## Phase 3 — Workflow Orchestration

Introduce a workflow engine such as LangGraph only if explicit state machines or more complex branching become necessary.

## Phase 4 — Specialised Capabilities

Introduce specialised agents only where separation provides a clear clinical, operational or safety benefit.

Potential areas include:

```text
HIV / ART
Family Planning
Maternal and Child Health
Pharmacy
Laboratory
Appointments
Referrals
Patient support
```

These specialised components should continue to operate within common hospital-wide security, safety, RAG and OpenMRS integration rules.

## Phase 5 — Additional Channels

The same backend intelligence may later support:

* SMS
* USSD
* Web chat
* Mobile applications
* Voice

The clinical logic should remain independent of the communication channel.

---

# 35. Key Design Principle

```text
WHATSAPP
    =
CONVERSATION INTERFACE

FASTAPI
    =
APPLICATION + INTEGRATION + AGENT RUNTIME

OPENMRS
    =
CLINICAL SYSTEM OF RECORD

LLM
    =
LANGUAGE UNDERSTANDING + REASONING

TOOLS
    =
CONTROLLED ACTIONS

RAG
    =
APPROVED CLINICAL KNOWLEDGE

APPLICATION DATABASE
    =
STATE + WORKFLOW + AUDIT SUPPORT

HUMAN PROVIDER
    =
CLINICAL ESCALATION AND OVERSIGHT
```

The system should therefore never be described simply as a **Family Planning FastAPI + MySQL API**.

A more accurate description is:

> **A hospital-wide WhatsApp AI agent platform built with FastAPI, integrated with OpenMRS as the clinical backend, grounded through approved clinical RAG sources, and capable of securely using controlled tools for patient support, information retrieval, referrals, follow-up and human escalation.**

---

# 36. Reference Documentation

### Meta

WhatsApp Business Platform:

https://developers.facebook.com/docs/whatsapp/

WhatsApp Cloud API:

https://developers.facebook.com/docs/whatsapp/cloud-api/

### OpenAI

Responses API:

https://platform.openai.com/docs/api-reference/responses

Agents SDK:

https://openai.github.io/openai-agents-python/

### OpenMRS

Use the OpenMRS REST API and implementation-specific endpoints configured for the hospital environment.

---

# 37. Important Clinical Note

This application is intended to **support healthcare delivery, patient education, navigation, follow-up and controlled access to hospital services**.

It must not be treated as an autonomous replacement for trained healthcare professionals.

Before clinical functionality is deployed in production:

* Clinical content must be approved
* RAG documents must be validated
* Safety rules must be tested
* OpenMRS permissions must be reviewed
* Patient-identity workflows must be verified
* Privacy and data-protection controls must be implemented
* Referral pathways must be functional
* Human escalation must be tested
* WhatsApp messaging workflows must comply with the rules in force
* Clinical and technical monitoring must be enabled


