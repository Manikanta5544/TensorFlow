class AppError(Exception):
    code: str = "APP_ERROR"
    http_status: int = 400

    def __init__(self, message: str, code: str | None = None):
        self.message = message
        if code:
            self.code = code
        super().__init__(message)


class NotFoundError(AppError):
    code = "NOT_FOUND"
    http_status = 404


class ConflictError(AppError):
    code = "CONFLICT"
    http_status = 409


class ValidationAppError(AppError):
    code = "VALIDATION_ERROR"
    http_status = 422


class UnauthorizedError(AppError):
    code = "UNAUTHORIZED"
    http_status = 401


class ForbiddenError(AppError):
    code = "FORBIDDEN"
    http_status = 403


class RateLimitedError(AppError):
    code = "RATE_LIMITED"
    http_status = 429
