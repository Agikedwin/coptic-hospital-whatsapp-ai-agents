# Coptic AI Agent

**AI-Powered Family Planning and HIV Care & Treatment Support via WhatsApp and Telegram**

The **Coptic AI Agent** is a conversational healthcare application developed to support **patients and healthcare service providers**, including doctors, clinical officers, nurses, counsellors, pharmacists and programme teams. It makes approved family planning (FP) and HIV prevention, care and treatment information easier to access through **WhatsApp and Telegram**, while enabling authorized users to retrieve relevant clinical information from **OpenMRS** through controlled application tools.

Built with **Python and FastAPI**, the platform combines large language models (LLMs), agent orchestration, retrieval-augmented generation (RAG), secure identity and session controls, and integration with existing healthcare systems. The two messaging platforms serve as communication channels; clinical workflows and access controls remain centralized in the backend.

## What the Application Does

The Coptic AI Agent provides two distinct, role-based experiences through **WhatsApp and Telegram**: confidential self-service for patients and rapid, authorized clinical information retrieval for healthcare providers. Its primary focus is **family planning and HIV prevention, care and treatment**.

### For patients

- **Secure access to medical and treatment information:** After identity verification and appropriate authorization, patients can ask about selected information in their own medical record, including appointments, prescribed treatment, medication instructions, and relevant HIV care or family planning follow-up details. Only information approved for patient disclosure is returned.
- **Book and manage appointments:** Request, book or reschedule clinic appointments through integrated scheduling workflows, where those functions are enabled, with confirmation of the appointment details.
- **Receive diagnostic and laboratory reports:** Securely request and receive clinician-approved diagnostic reports and permitted laboratory results when available in the connected clinical system. The AI **does not independently diagnose** conditions or generate official diagnostic reports.
- **Family planning support:** Get understandable information on contraceptive options, side effects, method continuation or switching, and when to seek a clinician's assessment.
- **HIV prevention and treatment support:** Access approved information on HIV testing, PrEP, PEP, ART adherence, viral-load monitoring and follow-up care, with referral or urgent escalation when appropriate.
- **Reminders and navigation:** Receive approved appointment or medication reminders and guidance on available services, clinic locations and referrals.

### For healthcare service providers

- **Rapid retrieval of patient medical records:** Authorized doctors, clinical officers, nurses, counsellors and other service providers can promptly search and retrieve relevant OpenMRS data to support care delivery, subject to their assigned roles and permissions.
- **Patient history and treatment review:** Access appropriately scoped encounter summaries, HIV programme enrolment, ART regimens, prescribed medications, laboratory and viral-load results, family planning history and upcoming appointments.
- **Clinical workflow support:** Locate information needed for consultations, follow-up, referrals and continuity of care without manually navigating multiple record screens, where the corresponding integrations are available.
- **Evidence-based reference:** Search approved HIV and family planning guidelines and facility protocols to support clinical counselling and decision-making; urgent or complex cases remain with qualified clinicians.

**Privacy and clinical boundaries:** Patient and provider permissions are separate. A WhatsApp number or Telegram account alone is not proof of patient identity or clinical authorization. Access to medical records, appointment booking and reports depends on the relevant backend integration, consent, identity verification and release permissions. The application assists care; it does not replace clinical judgment.

## Technical Architecture

```text
Patients and healthcare providers
          │
          ├── Telegram Bot API
          └── WhatsApp Cloud API
                    │
             HTTPS Webhooks
                    │
             Python / FastAPI
                    │
       Identity • Consent • Authorization
                    │
           Redis Sessions / OTP
                    │
          Coptic AI Agent Runtime
         LangChain + LangGraph
                    │
       ┌────────────┼────────────┐
       │            │            │
  LLM Providers   RAG Layer   Controlled Tools
       │            │            │
       │     Sentence-Transformers  OpenMRS APIs
       │        + ChromaDB       Referrals / Follow-up
       │            │            │
       └────────────┼────────────┘
                    │
       Safety and Response Validation
                    │
          Telegram / WhatsApp
```

The agent interprets a request, determines whether approved knowledge or clinical data is needed, invokes only permitted tools, and returns a response appropriate to the user's role and channel. Sensitive requests require identity verification, authorization and, where appropriate, consent before any protected information is disclosed.

## Technology Stack and Implementation

| Technology | Role in the application |
|---|---|
| **Python** | Primary language for backend services, agent functions, integrations and asynchronous message handling. |
| **FastAPI** | Hosts WhatsApp and Telegram webhooks, routes messages, validates requests and exposes protected application services. |
| **Telegram Bot API** | Receives incoming messages and delivers replies; supports contact-sharing authentication and typing indicators. |
| **WhatsApp Cloud API** | Receives webhook events and sends responses through Meta's messaging infrastructure; follows channel-specific message and template rules. |
| **LangChain** | Provides abstractions for LLM providers, prompts, retrievers and tool calling, allowing the agent to connect language models with clinical workflows. |
| **LangGraph** | Supports stateful, multi-step agent workflows such as routing, authorization checks, retrieval, tool execution, safety review and escalation. |
| **Sentence-Transformers** | Generates embeddings from approved clinical documents and queries to support semantic knowledge retrieval. |
| **ChromaDB** | Stores and searches vector embeddings for RAG, returning relevant passages from approved clinical guidance. |
| **Redis** | Stores temporary OTP records, verification-attempt counters, authenticated sessions and short-lived conversation state with expiry controls. |
| **OpenMRS** | Source of truth for patient clinical records; accessed only through scoped, authenticated application tools and APIs. |
| **MySQL / PostgreSQL** | Optional relational persistence for configuration, workflow records, audit metadata and application state—not a substitute for OpenMRS. |
| **LLM integrations** | Configurable AI inference through supported hosted providers or local models such as Ollama, subject to deployment and data-governance requirements. |
| **Docker / Docker Compose** | Optional packaging and deployment of the backend and supporting services. |
| **Pytest** | Automated testing of webhooks, security boundaries, agent behaviour, retrieval and clinical workflows. |

### Agent orchestration: LangChain and LangGraph

**LangChain** connects configured LLMs to prompts, retrieval components and narrowly defined tool interfaces. **LangGraph** models multi-step interactions that need explicit state and branching. For example, a medication-related question can pass through identity and access checks, a relevant OpenMRS lookup, guideline retrieval, response validation and human escalation when necessary. The model **does not receive unrestricted database access**; the backend enforces what tools may be called and what data may be returned.

### Clinical knowledge: Sentence-Transformers, ChromaDB and RAG

RAG grounds health-education responses in a curated knowledge collection rather than relying solely on the model's pretrained knowledge. Approved materials may include Kenya Ministry of Health and NASCOP guidance, WHO guidance, Coptic facility standard operating procedures, and clinician-reviewed FP and HIV education resources.

Documents are prepared and divided into searchable passages. **Sentence-Transformers** converts passages into vector embeddings, which **ChromaDB** indexes for semantic retrieval. For each relevant question, the retriever supplies matching source passages to the agent. Source provenance, document version and review date should be maintained so outdated or unapproved guidance can be excluded. Retrieved text is reference material, **not** an instruction source authorized to override security or clinical rules.

### Messaging: Telegram and WhatsApp

**Telegram** and **WhatsApp** use separate webhook adapters but share the same agent runtime. The adapters normalize incoming events, identify the channel and sender, route messages through security checks, and format responses for the correct platform. Asynchronous processing helps keep webhook handling responsive. Telegram supports typing-status feedback; WhatsApp feedback features are used only where supported by the configured API and messaging flow. Repeated or duplicate webhook events should be handled idempotently to prevent duplicate replies or actions.

### Authentication and state: Redis

The Telegram workflow includes **contact sharing, six-digit OTP verification and Redis-backed sessions**. Redis stores temporary authentication data with time-to-live limits and can track failed attempts. After successful verification, an authenticated session is reused until expiry, preventing unnecessary repeated login prompts. WhatsApp identity and access controls must be implemented and validated independently; a phone number alone is insufficient evidence of entitlement to clinical data. Conversation state is scoped by user and channel to avoid cross-user information leakage.

### Clinical integration: OpenMRS

**OpenMRS** remains the authoritative clinical record. Tools exposed by the FastAPI backend may support patient search, encounter review, programme enrolment, ART medication review, laboratory or viral-load information, and appointment lookup—**only when implemented and authorized**. Each tool should validate scope, minimize returned fields, handle errors securely and record appropriate audit metadata. Clinical write operations require additional review, permissions and confirmation safeguards.

## Clinical Safety and Data Protection

Because the platform works in healthcare, responses are subject to explicit clinical and privacy boundaries:

- **Role-based access and verified identity** before patient-specific records are disclosed.
- **Consent and minimum-necessary data access**, with masking of identifiers where appropriate.
- **HTTPS and webhook validation**, including channel-specific authenticity checks.
- **Secret management** outside source control; OTP secrets, API tokens and credentials must not appear in logs or responses.
- **Clinical grounding** in approved, versioned guidance, with clear limits on uncertain or incomplete information.
- **Human escalation** for emergencies, recent HIV exposure requiring urgent PEP assessment, significant adverse effects, safeguarding concerns or requests needing physical examination.
- **Auditability and testing** for tool calls, authorization decisions, retrieval quality, response safety and session isolation.

The AI Agent is a **clinical support and navigation tool**, not an autonomous diagnosing or prescribing system. Clinical decisions remain with qualified healthcare professionals.

## Configuration and Deployment

The application is intended to run as a secured **FastAPI** service with reachable HTTPS webhook endpoints, configured Telegram and WhatsApp application credentials, a Redis service, access-controlled OpenMRS integration and approved AI/RAG components. Use environment variables or a secret manager for configuration. Development environments may use a secure tunnel; production requires stable HTTPS endpoints, monitoring, backups, access restrictions and tested incident-response procedures.

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install project dependencies
pip install -r requirements.txt

# Run the API locally (adjust the module path if needed)
uvicorn app.main:app --reload

# Run automated tests
pytest -q
```

The commands assume the corresponding project files and dependencies exist; adapt them to the actual repository layout. Never commit `.env` files or live credentials. Before production use, verify webhook signatures, OTP and session expiration, OpenMRS permissions, RAG source approval, and escalation routes for **both** channels.

## Project Scope

The Coptic AI Agent is designed primarily for **family planning and HIV prevention, care and treatment**, serving both patients and authorized service providers through a shared, extensible backend. Other clinical modules may be incorporated later using the same controlled tool, RAG, identity and safety architecture.

**Core principle:** WhatsApp and Telegram deliver conversations; **FastAPI, LangChain, LangGraph, RAG and controlled OpenMRS integrations** provide the application intelligence—under explicit clinical and data-protection safeguards.
