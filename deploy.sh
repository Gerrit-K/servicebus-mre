set -eou pipefail

# required to set: QUEUE_NAME, CONNECTION_STRING, IMAGE

export NAMESPACE=servicebus-mre
export APP_NAME=servicebus-mre
export CONNECTION_STRING_BASE64=$(base64 -w0 <<<"${CONNECTION_STRING:?}")

kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

envsubst < manifests/secret.yaml | kubectl -n "$NAMESPACE" apply -f -
MODE=consumer envsubst < manifests/deployment.yaml | kubectl -n "$NAMESPACE" apply -f -
MODE=producer envsubst < manifests/deployment.yaml | kubectl -n "$NAMESPACE" apply -f -
