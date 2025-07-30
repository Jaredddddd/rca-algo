

# How to develop

Use git submodule to add algorithms into this repository. 


e.g., `git submodule add git@github.com:CUHK-SE-Group/ts-anomaly-detector.git algorithms/detector`

# How to configure algo

There should be a `Dockerfile`, `entrypoint.sh`, `info.toml` in the algorithm folder.

```toml
name = "simplerca"

[env_vars]
your_env_key1="your_env_value"
your_env_key2="your_env_value"
```

The `build_algo.py` will read the env key to store it in the database. When running the algo in the future, RCABench will check the environment variables.

# How to build


```bash
# build all the algorithms
make build
```


# How to test algo in remote

Submit a algo execution to the remote server and run it. Env is used to control the environment variables (runtime behavior) for the algorithm execution. 

```bash
nn@debian ~/w/rca-algo-contrib (main)> uv run run_algo.py submit-execution --help
                                                                                                                             
 Usage: run_algo.py submit-execution [OPTIONS]                                                                               
                                                                                                                             
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --algorithm  -a      TEXT  [default: None] [required]                                                                  │
│ *  --dataset    -d      TEXT  [default: None] [required]                                                                  │
│    --env                TEXT  [default: None]                                                                             │
│    --help                     Show this message and exit.                                                                 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```



```bash
uv run run_algo.py submit-execution -a random -d ts2-ts-route-plan-service-request-abort-l264j8
```

<details>
<summary>Click to view output</summary>

```
2025-07-21 18:12:54.261 | DEBUG    | typer.main:wrapper:699 - enter submit_execution    
{'algorithms': ['random'],
 'datasets': ['ts2-ts-route-plan-service-request-abort-l264j8'],
 'envs': None}
{
    "group_id": "a7e5d7e7-6146-43a9-9fd2-e64595af1b0a",
    "traces": [
        {
            "head_task_id": "19ea1b46-ccee-4283-bdc2-8bf7865ce05f",
            "index": 0,
            "trace_id": "d5c387f4-74fd-4fe6-be3c-38d369a2a995",
            "additional_properties": {}
        }
    ],
    "additional_properties": {}
}
2025-07-21 18:12:54.269 | DEBUG    | typer.main:wrapper:699 - exit  submit_execution     duration=0.007197s
{'algorithms': ['random'],
 'datasets': ['ts2-ts-route-plan-service-request-abort-l264j8'],
 'envs': None}
```

</details>

After the execution is submitted, you can check the status of the execution using the trace ID, which is a list of events that occurred during the execution. You can use the `trace` command to stream the trace events.


```bash
nn@debian ~/w/rca-algo-contrib (main)> uv run run_algo.py trace d5c387f4-74fd-4fe6-be3c-38d369a2a995
```

<details>
<summary>Click to view output</summary>

```bash
[2025-07-21 18:21:30] [INFO] [trace:98] - Connecting to /api/v1/traces/d5c387f4-74fd-4fe6-be3c-38d369a2a995/stream with Last-Event-ID: 0
2025-07-21 18:21:30.319 | INFO     | __main__:trace:20 - {
  "task_id": "19ea1b46-ccee-4283-bdc2-8bf7865ce05f",
  "task_type": "RunAlgorithm",
  "event_name": "task.started",
  "payload": "{\"task_id\":\"19ea1b46-ccee-4283-bdc2-8bf7865ce05f\",\"type\":\"RunAlgorithm\",\"immediate\":true,\"execute_time\":0,\"restart_num\":0,\"retry_policy\":{\"max_attempts\":0,\"backoff_sec\":0},\"payload\":{\"algorithm\":{\"image\":\"\",\"name\":\"random\",\"tag\":\"\"},\"dataset\":\"ts2-ts-route-plan-service-request-abort-l264j8\",\"env_vars\":{}},\"status\":\"Pending\",\"trace_id\":\"d5c387f4-74fd-4fe6-be3c-38d369a2a995\",\"group_id\":\"a7e5d7e7-6146-43a9-9fd2-e64595af1b0a\",\"trace_carrier\":{\"traceparent\":\"00-90782d9e7e16556d52f56fd3f56f1604-68b5b4fe7c829407-01\"},\"group_carrier\":{\"traceparent\":\"00-90782d9e7e16556d52f56fd3f56f1604-8bd40cbaab478b34-01\"}}"
}
2025-07-21 18:21:30.320 | INFO     | __main__:trace:20 - {
  "task_id": "19ea1b46-ccee-4283-bdc2-8bf7865ce05f",
  "task_type": "RunAlgorithm",
  "event_name": "task.status.update",
  "payload": "{\"status\":\"Running\",\"msg\":\"running algorithm for task 19ea1b46-ccee-4283-bdc2-8bf7865ce05f\"}"
}
2025-07-21 18:21:30.320 | INFO     | __main__:trace:20 - {
  "task_id": "19ea1b46-ccee-4283-bdc2-8bf7865ce05f",
  "task_type": "RunAlgorithm",
  "event_name": "algorithm.run.succeed",
  "payload": "{\"algorithm\":{\"name\":\"random\",\"image\":\"\",\"tag\":\"\"},\"dataset\":\"ts2-ts-route-plan-service-request-abort-l264j8\",\"execution_id\":1789,\"timestamp\":\"20250721_101300\"}"
}
2025-07-21 18:21:30.320 | INFO     | __main__:trace:20 - {
  "task_id": "19ea1b46-ccee-4283-bdc2-8bf7865ce05f",
  "task_type": "RunAlgorithm",
  "event_name": "task.status.update",
  "payload": "{\"status\":\"Completed\",\"msg\":\"Task 19ea1b46-ccee-4283-bdc2-8bf7865ce05f completed\"}"
}
2025-07-21 18:21:30.320 | INFO     | __main__:trace:20 - {
  "task_id": "226a2c5a-317c-497a-bf52-062af643be20",
  "task_type": "CollectResult",
  "event_name": "task.started",
  "payload": "{\"task_id\":\"226a2c5a-317c-497a-bf52-062af643be20\",\"type\":\"CollectResult\",\"immediate\":true,\"execute_time\":0,\"restart_num\":0,\"retry_policy\":{\"max_attempts\":0,\"backoff_sec\":0},\"payload\":{\"algorithm\":{\"image\":\"\",\"name\":\"random\",\"tag\":\"\"},\"dataset\":\"ts2-ts-route-plan-service-request-abort-l264j8\",\"execution_id\":1789,\"timestamp\":\"20250721_101300\"},\"status\":\"Pending\",\"trace_id\":\"d5c387f4-74fd-4fe6-be3c-38d369a2a995\",\"group_id\":\"a7e5d7e7-6146-43a9-9fd2-e64595af1b0a\",\"trace_carrier\":{\"traceparent\":\"00-90782d9e7e16556d52f56fd3f56f1604-68b5b4fe7c829407-01\"}}"
}
2025-07-21 18:21:30.320 | INFO     | __main__:trace:20 - {
  "task_id": "226a2c5a-317c-497a-bf52-062af643be20",
  "task_type": "CollectResult",
  "event_name": "algorithm.collect_result",
  "payload": "[{\"id\":9910,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-notification-service\",\"rank\":1,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9911,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-train-food-service\",\"rank\":2,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9912,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-payment-service\",\"rank\":3,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9913,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-price-service\",\"rank\":4,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9914,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-station-food-service\",\"rank\":5,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9915,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-station-service\",\"rank\":6,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9916,\"execution_id\":1789,\"level\":\"service\",\"result\":\"loadgenerator-service\",\"rank\":7,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9917,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-route-service\",\"rank\":8,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9918,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-order-other-service\",\"rank\":9,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9919,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-basic-service\",\"rank\":10,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9920,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-user-service\",\"rank\":11,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9921,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-consign-price-service\",\"rank\":12,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9922,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-security-service\",\"rank\":13,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9923,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-config-service\",\"rank\":14,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9924,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-route-plan-service\",\"rank\":15,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9925,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-assurance-service\",\"rank\":16,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9926,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-order-service\",\"rank\":17,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9927,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-delivery-service\",\"rank\":18,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9928,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-food-service\",\"rank\":19,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9929,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-travel2-service\",\"rank\":20,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9930,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-travel-plan-service\",\"rank\":21,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9931,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-travel-service\",\"rank\":22,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9932,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-verification-code-service\",\"rank\":23,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9933,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-preserve-service\",\"rank\":24,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9934,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-auth-service\",\"rank\":25,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9935,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-contacts-service\",\"rank\":26,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9936,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-inside-payment-service\",\"rank\":27,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9937,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-ui-dashboard\",\"rank\":28,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9938,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-consign-service\",\"rank\":29,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9939,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-train-service\",\"rank\":30,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"},{\"id\":9940,\"execution_id\":1789,\"level\":\"service\",\"result\":\"ts-seat-service\",\"rank\":31,\"confidence\":0,\"created_at\":\"2025-07-21T10:13:18.758503688Z\",\"updated_at\":\"2025-07-21T10:13:18.758503688Z\"}]"
}
2025-07-21 18:21:30.320 | INFO     | __main__:trace:20 - {
  "task_id": "226a2c5a-317c-497a-bf52-062af643be20",
  "task_type": "CollectResult",
  "event_name": "task.status.update",
  "payload": "{\"status\":\"Completed\",\"msg\":\"Task 226a2c5a-317c-497a-bf52-062af643be20 completed\"}"
}
[2025-07-21 18:21:30] [INFO] [trace:126] - Received end event, closing connection
[2025-07-21 18:21:30] [INFO] [trace:148] - Connection closed
```

