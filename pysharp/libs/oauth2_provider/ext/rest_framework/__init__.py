# flake8: noqa
from .authentication import OAuth2Authentication
from .permissions import TokenHasScope, TokenHasReadWriteScope, TokenHasResourceScope
from .permissions import IsAuthenticatedOrTokenHasScope
