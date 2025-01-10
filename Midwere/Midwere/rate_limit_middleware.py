import time
from django.http import JsonResponse
from django.core.cache import cache

class RateLimitMiddleware:
    Rate_limit = 100
    Time_window = 300
    Blocked_status_code = 429

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = RateLimitMiddleware.get_client_ip(request)
        cache_key = f"Rate_limit_{ip_address}"
        request_data = cache.get(cache_key, ([], 0))
        request_timestamps, block_until = request_data
        current_time = time.time()

        if block_until > current_time:
            return JsonResponse({"error": "Too many requests. pls try again later."}, status=self.Blocked_status_code)

        request_timestamps = [ts for ts in request_timestamps if ts > current_time - self.Time_window]
        if len(request_timestamps) >= self.Rate_limit:
            block_until = current_time + self.Time_window
            cache.set(cache_key, (request_timestamps, block_until), timeout=self.Time_window)
            return JsonResponse({"error": "Too many requests. pls try again later."}, status=self.Blocked_status_code)

        request_timestamps.append(current_time)
        cache.set(cache_key, (request_timestamps, 0), timeout=self.Time_window)

        response = self.get_response(request)
        remaining_requests = self.Rate_limit - len(request_timestamps)
        response.headers["X-RateLimit-Limit"] = self.Rate_limit
        response.headers["X-RateLimit-Remaining"] = remaining_requests

        return response

    @staticmethod
    def get_client_ip(request):

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
