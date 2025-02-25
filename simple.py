from starlette.requests import Request
import time

import ray
from ray import serve

@serve.deployment(num_replicas=2, ray_actor_options={"num_cpus": 0.2, "num_gpus": 0})
class RayApi:
    async def __call__(self, http_request: Request) -> str:
        start_time = time.time()
        csv_loc: str = await http_request.json()
        ds = ray.data.read_csv(csv_loc)
        ds.write_parquet(csv_loc.replace(".csv", ".parquet"))
        mem_bytes = ds.size_bytes()
        mem_gb = mem_bytes / (1024 ** 3)  # Convert bytes to GB
        execution_time = time.time() - start_time
        return f"The file {csv_loc} of size {mem_gb:.2f} GB has been converted to parquet in {execution_time:.2f} seconds"

app = RayApi.bind()