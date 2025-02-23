from starlette.requests import Request

import ray
from ray import serve

@serve.deployment(num_replicas=2, ray_actor_options={"num_cpus": 0.2, "num_gpus": 0})
class RayApi:
    async def __call__(self, http_request: Request) -> str:
        csv_loc: str = await http_request.json()
        ds = ray.data.read_csv(csv_loc)
        ds.write_parquet(csv_loc.replace(".csv", ".parquet"))
        return f"The file {csv_loc} has been converted to parquet"

app = RayApi.bind()