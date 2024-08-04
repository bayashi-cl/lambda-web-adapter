#!/bin/bash

PATH="/opt/python/bin:$LAMBDA_TASK_ROOT/bin:$PATH" PYTHONPATH="/opt/python/lib/python3.12/site-packages:$LAMBDA_RUNTIME_DIR:$PYTHONPATH" \
    exec python -m fastapi run
