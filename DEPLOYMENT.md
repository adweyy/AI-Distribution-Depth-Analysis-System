# Shalina Distribution Intelligence — Deployment Guide

This guide explains how to go from running the app locally to having it live on
Azure, accessible to the entire Shalina commercial team.

---

## Step 1 — Find Your Fabric SQL Endpoint

This is the most important step. The SQL endpoint gives the app a direct,
fast connection to your Fabric warehouse instead of going through Power BI APIs.

1. Go to [app.fabric.microsoft.com](https://app.fabric.microsoft.com)
2. Open your workspace (the one that holds the Nigeria and Angola tables)
3. Click on the **Warehouse** item (or Lakehouse with SQL endpoint)
4. Click the **⚙ Settings** icon in the top-right
5. Find the field labelled **"SQL connection string"** — it looks like:
   ```
   abc123xyz.datawarehouse.fabric.microsoft.com
   ```
6. Copy that value and add it to your `.env`:
   ```
   FABRIC_SQL_ENDPOINT=abc123xyz.datawarehouse.fabric.microsoft.com
   FABRIC_SQL_DATABASE=YourWarehouseName
   ```
7. Also ask your IT / data team to grant the service principal
   (`FABRIC_CLIENT_ID` in your `.env`) the **db_datareader** role on the warehouse.

---

## Step 2 — Test Locally

Make sure the app runs locally first:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Check the banner at the top of the dashboard:
- 🟢 **"Connected to Microsoft Fabric SQL Analytics Endpoint"** — perfect, SQL is working
- 🟡 **"Hybrid"** — one country is live, the other is on CSV
- 🟡 **"CSV Fallback"** — Fabric unreachable, check your credentials

---

## Step 3 — Set Up Azure Resources (one-time, ask IT)

### 3a. Create Azure Container Registry (ACR)

```bash
az group create --name shalina-rg --location eastus
az acr create --resource-group shalina-rg --name shalinaacr --sku Basic
az acr update --name shalinaacr --admin-enabled true
```

### 3b. Create Azure App Service

```bash
az appservice plan create \
  --name shalina-plan \
  --resource-group shalina-rg \
  --sku B2 \
  --is-linux

az webapp create \
  --resource-group shalina-rg \
  --plan shalina-plan \
  --name shalina-whitespace \
  --deployment-container-image-name shalinaacr.azurecr.io/shalina-whitespace:latest
```

### 3c. Create Azure AD Service Principal for GitHub Actions

```bash
az ad sp create-for-rbac \
  --name "shalina-github-actions" \
  --role contributor \
  --scopes /subscriptions/<YOUR_SUBSCRIPTION_ID>/resourceGroups/shalina-rg \
  --sdk-auth
```

Copy the entire JSON output — you'll need it in Step 4.

---

## Step 4 — Add GitHub Secrets

Go to your GitHub repo → **Settings → Secrets and variables → Actions → New secret**

Add each of these:

| Secret Name | Where to find it |
|---|---|
| `AZURE_CREDENTIALS` | JSON output from Step 3c |
| `REGISTRY_LOGIN_SERVER` | `shalinaacr.azurecr.io` |
| `REGISTRY_USERNAME` | ACR → Access Keys → Username |
| `REGISTRY_PASSWORD` | ACR → Access Keys → Password |
| `AZURE_WEBAPP_NAME` | `shalina-whitespace` |
| `FABRIC_TENANT_ID` | From your `.env` |
| `FABRIC_CLIENT_ID` | From your `.env` |
| `FABRIC_CLIENT_SECRET` | From your `.env` |
| `FABRIC_SQL_ENDPOINT` | From Step 1 |
| `FABRIC_SQL_DATABASE` | From Step 1 |
| `FABRIC_WORKSPACE_ID` | From your `.env` |
| `FABRIC_DATASET_ID` | From your `.env` |
| `FABRIC_USERNAME` | From your `.env` |
| `FABRIC_PASSWORD` | From your `.env` |

---

## Step 5 — Deploy

Push to the `main` branch:

```bash
git add .
git commit -m "feat: add SQL endpoint, Docker, CI/CD"
git push origin main
```

GitHub Actions will automatically:
1. Build the Docker image (with ODBC Driver 18 included)
2. Push it to your Azure Container Registry
3. Deploy it to Azure App Service
4. Inject all secrets as environment variables

Your app will be live at:
```
https://shalina-whitespace.azurewebsites.net
```

---

## Step 6 — Restrict Access to Shalina Staff (Recommended)

By default the app is publicly accessible. To restrict it to Shalina employees:

1. Azure Portal → your App Service → **Authentication**
2. Click **Add identity provider**
3. Choose **Microsoft** → select your Shalina Azure AD tenant
4. Set "Unauthenticated requests" to **HTTP 401** or **Redirect to login**

Now only users with a `@shalina.com` account can access the app.

---

## Write-Back: Saving Predictions to Fabric

Once deployed, the app can write churn predictions and whitespace scores
back into your Fabric warehouse. Call these functions from your code:

```python
from fabric_connector import write_churn_predictions, write_whitespace_scores

# After training the churn model:
result = write_churn_predictions(scored_df)
print(result)  # {'success': True, 'rows_written': 21879, 'error': None}

# After loading outlet data:
result = write_whitespace_scores(df_all)
print(result)  # {'success': True, 'rows_written': 39155, 'error': None}
```

The tables `ChurnPredictions` and `WhitespaceScores` are created automatically
in your Fabric warehouse on first write. They can then be used in Power BI
reports that the commercial team already uses.

---

## Troubleshooting

**App shows "CSV Fallback" after deployment**
→ Check that all `FABRIC_*` secrets are set correctly in App Service → Configuration → Application settings.

**SQL connection error: "Cannot open server... firewall"**
→ Ask IT to add the App Service outbound IPs to the Fabric workspace network rules.
   (Azure Portal → App Service → Networking → Outbound addresses)

**"ODBC Driver 18 not found" error**
→ This only happens if running locally without the driver installed.
   Download it from: https://aka.ms/downloadmsodbcsql
   On the deployed container it is pre-installed.

**401 Unauthorized from Power BI API**
→ The service principal needs to be added to the Power BI workspace.
   Power BI Service → Workspace → Settings → Access → add the app by Client ID.
