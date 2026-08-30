class LLMError(Exception):
    pass

class LLMAPIError(LLMError):
    pass

class LLMRetryExhausted(LLMError):
    pass