import csv
import time
import logging
from datetime import datetime
from functools import wraps
import os
import asyncio

logger = logging.getLogger(__name__)

# 你之前写的 _extract_usage 保持不变
def _extract_usage(result):
    if isinstance(result, dict):
        usage = result.get("usage", {})
        return {
            "model": result.get("model", ""),
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
        }
    elif hasattr(result, "usage"):
        usage = result.usage
        return {
            "model": getattr(result, "model", ""),
            "prompt_tokens": getattr(usage, "prompt_tokens", 0),
            "completion_tokens": getattr(usage, "completion_tokens", 0),
            "total_tokens": getattr(usage, "total_tokens", 0),
        }
    else:
        return {
            "model": "",
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

# 更严谨的 _write_csv（替换掉你原来的 write_csv）
def _write_csv(csv_path, row):
    headers = [
        'timestamp', 'model', 'prompt_tokens', 'completion_tokens',
        'total_tokens', 'elapsed_ms', 'success', 'error'
    ]
    need_header = True
    if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
        with open(csv_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        expected_header = ",".join(headers)
        if first_line == expected_header:
            need_header = False

    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if need_header:
            writer.writerow(headers)
        writer.writerow(row)


# 同步版 cost_logger 装饰器
def cost_logger(csv_path):
    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = None
                error = ""
                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as e:
                    error = str(e)
                    raise
                finally:
                    elapsed_ms = (time.perf_counter() - start) * 1000
                    success = not error
                    extracted = _extract_usage(result) if result else {
                        'model': '', 'prompt_tokens': 0,
                        'completion_tokens': 0, 'total_tokens': 0
                    }
                    row = [
                        datetime.now().isoformat(),
                        extracted['model'],
                        extracted['prompt_tokens'],
                        extracted['completion_tokens'],
                        extracted['total_tokens'],
                        f"{elapsed_ms:.2f}",
                        success,
                        error
                    ]
                    _write_csv(csv_path, row)
            return async_wrapper
        else:
            # 你原来的同步 wrapper
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = None
                error = ""
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    error = str(e)
                    raise
                finally:
                    elapsed_ms = (time.perf_counter() - start) * 1000
                    success = not error
                    extracted = _extract_usage(result) if result else {
                        'model': '', 'prompt_tokens': 0,
                        'completion_tokens': 0, 'total_tokens': 0
                    }
                    row = [
                        datetime.now().isoformat(),
                        extracted['model'],
                        extracted['prompt_tokens'],
                        extracted['completion_tokens'],
                        extracted['total_tokens'],
                        f"{elapsed_ms:.2f}",
                        success,
                        error
                    ]
                    _write_csv(csv_path, row)
            return wrapper
    return decorator

