#!/bin/bash
set -e

echo "===== Testing Docker Container ====="

# Step 1: Build the image using the existing Dockerfile
echo "Building Docker image from existing Dockerfile..."
docker build -t evanchime/ebookstore:test .

# Step 2: Run tests by mounting the test directory into the container
echo "Running tests in Docker container..."
docker run --rm \
  --entrypoint "" \
  -v "$(pwd)/tests:/tests" \
  evanchime/ebookstore:test \
  python3 -m pytest /tests/

# Step 3: Verify the application starts properly
echo "Verifying application starts correctly..."
docker run --rm \
  --entrypoint "" \
  evanchime/ebookstore:test \
  python3 -c "import ebookstore; print('Application imported successfully')"

echo "===== All Docker container tests passed! ====="
exit 0