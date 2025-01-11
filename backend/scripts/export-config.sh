#!/bin/bash
gcloud run deploy myapp \
  --image=gcr.io/project-id/myapp \
  --mount-secrets=/secrets/firebase-credentials.json=firebase-credentials:latest \
  --set-env-vars-file=.env.production 