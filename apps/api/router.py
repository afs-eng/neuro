from ninja import NinjaAPI

from apps.accounts.api.router import router as accounts_router
from apps.patients.api.router import router as patients_router 

api = NinjaAPI(
    title="Laudos AI API",
    version="1.0.0",
    docs_url="/docs",
)

api.add_router("/accounts/", accounts_router)
api.add_router("/patients/", patients_router)