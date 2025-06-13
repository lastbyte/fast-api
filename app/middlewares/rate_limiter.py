import time
from typing import Awaitable, Callable
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class RateLimiterMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: FastAPI, max_requests: int = 100, time_window:int = 100) -> None:
        super().__init__(app)
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = {}

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:

        ip_address = request.client.host
        current_time = time.time()

        self.register_visit(ip_address=ip_address, current_time=current_time)
        is_valid_request = self.validate_limits(ip_address=ip_address)

        if not is_valid_request:
            return JSONResponse(status_code=429, content={"error"  :"Rate limit exceeded"})

        return await call_next(request)
    
    def register_visit(self, ip_address :str, current_time : float) :

        if ip_address not in self.requests:
            self.requests[ip_address] = []
        
        self.requests[ip_address].append(current_time)
        self.requests[ip_address].sort()

        self.requests[ip_address] = [
            request_time 
            for request_time in self.requests[ip_address]
            if request_time > current_time - self.time_window
        ]

    def validate_limits(self, ip_address: str):
        if ip_address not in self.requests:
            return True
        
        requests = self.requests[ip_address]

        if len(requests) < self.max_requests:
            return True
        
        return False