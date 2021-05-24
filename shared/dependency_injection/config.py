from api_gateway.application import (
    authenticate,
    create_competition,
    register_user,
)

INJECTED_MODULES = [authenticate, create_competition, register_user]
