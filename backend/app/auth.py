import os
from fastapi import Request, HTTPException
from clerk_backend_api import authenticate_request, AuthenticateRequestOptions

def require_user(request: Request) -> str:
    state = authenticate_request(
        request,
        AuthenticateRequestOptions(
            secret_key=os.environ["CLERK_SECRET_KEY"],
            authorized_parties=["http://localhost:3000"],
            accepts_token=["session_token"],
        ),
    )
    if not state.is_signed_in:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return state.payload["sub"]