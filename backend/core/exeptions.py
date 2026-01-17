from fastapi import HTTPException, status


class UnauthorizedExc(HTTPException):
    def __init__(
        self,
        status_code: status = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Не верная почта или пароль",
        headers: str | None = None,
    ):
        super().__init__(status_code, detail, headers)


class InvalidTokenExc(HTTPException):
    def __init__(
        self,
        status_code: status = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Не верный токен",
        headers: str | None = None,
    ):
        super().__init__(status_code, detail, headers)


class ExpireTokenExc(HTTPException):
    def __init__(
        self,
        status_code: status = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Токен истек",
        headers: str | None = None,
    ):
        super().__init__(status_code, detail, headers)

class PasswordExc(HTTPException):
    def __init__(
        self,
        status_code: status = status.HTTP_400_BAD_REQUEST,
        detail: str = "Пароли не совпадают",
        headers: str | None = None,
    ):
        super().__init__(status_code, detail, headers)