import json


def get_param(request, key, default=None):
    """Get a parameter from JSON body (if sent) or from form POST data.

    Keeps endpoints compatible with both application/json requests and
    traditional form submissions.
    """
    # cached parsed body
    if getattr(request, "_cached_json_body", None) is not None:
        body = request._cached_json_body
    else:
        body = None
        if request.content_type and "application/json" in request.content_type:
            try:
                body = json.loads(request.body.decode() or "{}")
            except Exception:
                body = None
        request._cached_json_body = body

    if body is not None:
        return body.get(key, default)

    return request.POST.get(key, default)
