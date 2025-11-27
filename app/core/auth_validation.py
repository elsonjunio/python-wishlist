from fastapi import Depends, HTTPException, Request


def require_user(request: Request):
    if not request.state.current_user:
        raise HTTPException(status_code=401, detail='Authentication required')
    return request.state.current_user


def require_role(*allowed_roles):
    def wrapper(user=Depends(require_user)):
        if user['role'] not in allowed_roles:
            raise HTTPException(status_code=403, detail='Forbidden')
        return user

    return wrapper
