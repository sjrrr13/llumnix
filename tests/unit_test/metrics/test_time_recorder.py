# Copyright (c) 2024, Alibaba Group;
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio

import pytest
from llumnix.metrics.metrics_types import Summary, Registery


@pytest.mark.parametrize("sleep_time", [0.001, 0.01, 0.1, 1])
async def test_time_recorder(sleep_time: int):
    register = Registery()
    summary = Summary(name="unit_test_summary", registry=register,metrics_sampling_interval=1)

    async def worker(sleep_time):
        with summary.observe_time():
            await asyncio.sleep(sleep_time)

    tasks = [worker(sleep_time=sleep_time) for i in range(100)]
    await asyncio.gather(*tasks)
    metrics = summary.collect()
    for metric in metrics:
        if metric.name == "unit_test_summary_mean":
            assert metric.value < sleep_time*1000 + 2
