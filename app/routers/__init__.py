from app.routers.counties import router as counties_router
from app.routers.education_levels import router as education_levels_router
from app.routers.marital_statuses import router as marital_statuses_router
from app.routers.discontinuation_reasons import router as discontinuation_reasons_router
from app.routers.fp_methods import router as fp_methods_router
from app.routers.database_metadata import router as database_metadata_router
from app.routers.subcounties import router as subcounties_router
from app.routers.chats import router as chats_router
from app.routers.facilities import router as facilities_router
from app.routers.clients import router as clients_router
from app.routers.encounters import router as encounters_router
from app.routers.counselling_sessions import router as counselling_sessions_router
from app.routers.reproductive_history import router as reproductive_history_router
from app.routers.fp_method_advantages import router as fp_method_advantages_router
from app.routers.fp_method_cautions import router as fp_method_cautions_router
from app.routers.fp_method_side_effects import router as fp_method_side_effects_router
from app.routers.fp_method_use_instructions import router as fp_method_use_instructions_router
from app.routers.fp_usage_episodes import router as fp_usage_episodes_router
from app.routers.fp_dispensing import router as fp_dispensing_router
from app.routers.followups import router as followups_router
from app.routers.side_effect_reports import router as side_effect_reports_router
from app.routers.clinical import router as clinical_router
from whatsapp.webhook import router as webhook_router

all_routers = [
    chats_router,
    counties_router,
    education_levels_router,
    marital_statuses_router,
    discontinuation_reasons_router,
    fp_methods_router,
    database_metadata_router,
    subcounties_router,
    facilities_router,
    clients_router,
    encounters_router,
    counselling_sessions_router,
    reproductive_history_router,
    fp_method_advantages_router,
    fp_method_cautions_router,
    fp_method_side_effects_router,
    fp_method_use_instructions_router,
    fp_usage_episodes_router,
    fp_dispensing_router,
    followups_router,
    side_effect_reports_router,
    clinical_router,
    webhook_router
]
