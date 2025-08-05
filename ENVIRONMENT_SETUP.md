# Environment Setup Instructions

This document provides instructions for setting up the Multi-Agent Custom Automation Engine environment.

## Prerequisites

1. Install Azure CLI: [https://docs.microsoft.com/en-us/cli/azure/install-azure-cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
2. Install Azure Developer CLI (AZD): [https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd)

## Setup Instructions

### Option 1: Automated Setup (Recommended)

Run the provided setup script:

```bash
./setup-azd-env.sh
```

### Option 2: Manual Setup

1. Log in to Azure:
   ```bash
   az login
   ```

2. Create a new AZD environment:
   ```bash
   azd env new -n production --no-prompt
   ```

3. Set the required environment variables:
   ```bash
   # Set resource group and location
   azd env set AZURE_ENV_NAME "production"
   azd env set AZURE_LOCATION "swedencentral"
   azd env set AZURE_RESOURCE_GROUP "rg-multi-agent-test-automation"
   azd env set AZURE_SUBSCRIPTION_ID "a3b64ac1-4ca3-4f9c-9465-f5a9abfbfb38"
   
   # Set OpenAI/AI model settings
   azd env set AZURE_ENV_OPENAI_LOCATION "norwayeast"
   azd env set AZURE_ENV_MODEL_NAME "gpt-4o"
   azd env set AZURE_ENV_MODEL_VERSION "2024-08-06"
   azd env set AZURE_ENV_MODEL_DEPLOYMENT_TYPE "GlobalStandard"
   azd env set AZURE_ENV_MODEL_CAPACITY "100"
   
   # Set other required settings
   azd env set AZURE_ENV_IMAGE_TAG "latest"
   azd env set AZURE_ENV_ENABLE_TELEMETRY "true"
   azd env set useWafAlignedArchitecture "false"
   
   # Set the existing Foundry Project ID (your existing deployed AI model)
   azd env set AZURE_ENV_FOUNDRY_PROJECT_ID "/subscriptions/a3b64ac1-4ca3-4f9c-9465-f5a9abfbfb38/resourceGroups/rg-multi-agent-test-automation/providers/Microsoft.CognitiveServices/accounts/aisa-macae-2sjcytrhsmbr/projects/aifp-macae-2sjcytrhsmbr"
   ```

## Deployment

After setting up the environment, deploy the application:

```bash
azd up --no-prompt
```

## Accessing the Application

- Frontend Website: https://app-macae-2qy43ab2ht7s.azurewebsites.net
- Backend API: https://ca-macae-2qy43ab2ht7s.purplesea-20a58ae5.swedencentral.azurecontainerapps.io

## Troubleshooting

If you encounter issues:

1. Verify your Azure login status: `az account show`
2. Check your environment variables: `azd env get-values`
3. Ensure the resource group exists: `az group show -n rg-multi-agent-test-automation`
