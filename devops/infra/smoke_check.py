"""Smoke test for the MLflow server.
Run AFTER `docker compose -f compose.dev.yml up -d --build`:
    pip install mlflow
    python smoke_test.py
It logs a fake run and uploads a small file as an artifact through the server."""
import pathlib, tempfile
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("smoke-test")

with tempfile.TemporaryDirectory() as d:
    f = pathlib.Path(d) / "hello-model.txt"
    f.write_text("pretend this is a model file")
    with mlflow.start_run(run_name="smoke") as run:
        mlflow.log_param("model", "demo")
        mlflow.log_metric("accuracy", 0.99)
        mlflow.log_artifact(str(f))
        print("OK: run", run.info.run_id)
print("Open http://localhost:5000 -> experiment 'smoke-test' -> the run -> Artifacts.")
