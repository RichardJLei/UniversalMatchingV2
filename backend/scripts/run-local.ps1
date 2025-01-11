# PowerShell script for running locally
$env:FLASK_ENV = "development"

# Build the image
docker build -t myapp:local --build-arg FLASK_ENV=development .

# Run with all necessary environment variables and mounted credentials
docker run -p 8080:8080 `
    -v "${PWD}/config/universalmatching-firebase-credentialv2.json:/secrets/firebase-credentials.json:ro" `
    --env-file .env `
    -e FLASK_ENV=development `
    myapp:local 