from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter
from app.auth.handlers import user_router
from app.auth.login_handler import login_router
import sentry_sdk
from starlette_exporter import handle_metrics
from starlette_exporter import PrometheusMiddleware

#########################
# BLOCK WITH API ROUTES #
#########################

sentry_sdk.init(
    dsn="https://cf2259c3da451766977a44f25641821e@o4506383221194752.ingest.sentry.io/4506497932722181",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

# create instance of the app
app = FastAPI()

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

# create the instance for the routes
main_api_router = APIRouter()

# # set routes to the app instance
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(main_api_router)

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8080)
