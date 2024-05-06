#!/bin/bash

PROJECT_ROOT=`dirname "$0"|realpath`

SSH_PUBLIC_KEY="ssh-rsa /OGu3VpWyGhUGOjvtCpjea4XNlgYzBAJUrQ/mHyC5VBnJo5PlM7zn/z27ohsbDOrgdXsw69VxjbqghbVI+iEmF6SFeKJxKbgc54XrO/1SyJZdN77nft8/TpMIRQ4wI87FC1P7uuYyqj59j0NrtkjJQetwH12coyGKH6A6IFgpLSZ1IvzR//tNOCuoJiYyvAO9OrsR9e7jJ8+ClXNFiahSX7bFWrv/kc3/T0nQtC5DALb4NJXSCYEiQPGPny8taAa5mfLbGw76373rtTtZ0WMEQShUyofUZ+E3X/EBW4i31l5JMOnVR6P7rTMJHxfM959q00+isUwWJWeeHo1MZt+1JgR8bKMoDy16/nIUqwBx7Dgf1k+ktKS9cFBPjSwlpZ0VH1PXG0xrDgFzhdOguZdmfg/05LsrWYvSRMM05EnSfwza1BUUI44nC7YyIXWAy+mnDMEbF2fLQ9plH0oAig/+n3VkkD9V8C/ErSwL57Zwq83j81dNBE="


exec \
docker run -it --rm \
-p 20022:22 \
-p 23000:3000 \
-p 28000:8000 \
-v "${PROJECT_ROOT}":/workspace \
-v "${PROJECT_ROOT}/vscode-server:/root/.vscode-server/" \
-v "${PROJECT_ROOT}/docker-poetry-cache:/root/.cache/pypoetry" \
-w /workspace \
-e "SSH_PUBLIC_KEY=${SSH_PUBLIC_KEY}" \
dagsterdbt:latest
