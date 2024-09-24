import functools
import io
from fastapi import Response
import yaml

# @webServer.get("/")
# def read_root():
#     return {"status": "ok"}

# @webServer.get('/openapi.yaml', include_in_schema=False)
# @functools.lru_cache()
# def read_openapi_yaml() -> Response:
#     openapi_json= webServer.openapi()
#     yaml_s = io.StringIO()
#     yaml.dump(openapi_json, yaml_s)
#     return Response(yaml_s.getvalue(), media_type='text/yaml')
