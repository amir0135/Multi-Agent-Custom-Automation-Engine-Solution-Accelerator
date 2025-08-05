#!/bin/bash
# Script to set up Azure Developer CLI environment variables
# This script recreates your environment settings without storing sensitive data in Git

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "Azure CLI is not installed. Please install it first."
    exit 1
fi

# Check if Azure Developer CLI is installed
if ! command -v azd &> /dev/null; then
    echo "Azure Developer CLI is not installed. Please install it first."
    exit 1
fi

# Check if logged in to Azure
az account show &> /dev/null
if [ $? -ne 0 ]; then
    echo "Not logged in to Azure. Please run 'az login' first."
    exit 1
fi

# Environment Name
ENV_NAME="production"
echo "Creating AZD environment: $ENV_NAME"
azd env new -n $ENV_NAME --no-prompt

# Set environment variables
echo "Setting environment variables..."
azd env set AZURE_ENV_NAME "$ENV_NAME"
azd env set AZURE_LOCATION "swedencentral"
azd env set AZURE_RESOURCE_GROUP "rg-multi-agent-test-automation"
azd env set AZURE_SUBSCRIPTION_ID "a3b64ac1-4ca3-4f9c-9465-f5a9abfbfb38"
azd env set AZURE_ENV_OPENAI_LOCATION "norwayeast"
azd env set AZURE_ENV_MODEL_NAME "gpt-4o"
azd env set AZURE_ENV_MODEL_VERSION "2024-08-06"
azd env set AZURE_ENV_MODEL_DEPLOYMENT_TYPE "GlobalStandard"
azd env set AZURE_ENV_MODEL_CAPACITY "100"
azd env set AZURE_ENV_IMAGE_TAG "latest"
azd env set AZURE_ENV_ENABLE_TELEMETRY "true"
azd env set useWafAlignedArchitecture "false"

# Set the existing Foundry Project ID (your existing deployed AI model)
azd env set AZURE_ENV_FOUNDRY_PROJECT_ID "/subscriptions/a3b64ac1-4ca3-4f9c-9465-f5a9abfbfb38/resourceGroups/rg-multi-agent-test-automation/providers/Microsoft.CognitiveServices/accounts/aisa-macae-2sjcytrhsmbr/projects/aifp-macae-2sjcytrhsmbr"

echo "Environment setup complete! Your AZD environment '$ENV_NAME' is now configured."
echo "To use it, run: azd env select $ENV_NAME"
echo ""
echo "To verify your environment settings, run: azd env get-values"
