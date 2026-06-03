# Cosmic-Navigator-AI-Agent 🌌

## Clone the Repository 

1.In the terminal,clone the repository:
```bash
git clone "https://github.com/KushalGupta-07/Cosmic-Navigator-AI-Agent.git"
```

## Set your project

1.In the terminal, set your project with this command:
```bash
gcloud config set project [PROJECT_ID]
```
Example: gcloud config set project lab-project-id-example

2. In the terminal, enable the APIs:
```bash
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  aiplatform.googleapis.com \
  compute.googleapis.com
```

When this finishes running, you should see an output like the following:
```bash
Operation "operations/acat.p2-[GUID]" finished successfully.
```

3. In the terminal, run the following command to open the zoo_guide_agent directory in the Cloud Shell Editor explorer:
```bash
cloudshell open-workspace ~/cosmic_navigator_agent
```

## Install requirements

1. In the terminal, create and activate a virtual environment using uv. This ensures your project dependencies don't conflict with the system Python.
```bash
uv venv
source .venv/bin/activate
```

2. Install the required packages into your virtual environment in the terminal.
```bash
uv pip install -r requirements.txt
```

## Set up environment variables

1. Use the following command in the terminal to update the .env file.
```bash
# 1. Set the variables in your terminal first
PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
SA_NAME=cosmic-signal-service

# 2. Create the .env file using those variables
cat <<EOF > .env
PROJECT_ID=$PROJECT_ID
PROJECT_NUMBER=$PROJECT_NUMBER
SA_NAME=$SA_NAME
SERVICE_ACCOUNT=${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com
MODEL="gemini-2.5-flash"
EOF
```

## Set up IAM permissions
With your local code ready, the next step is to set up the identity your agent will use in the cloud.

1. In the terminal, load the variables into your shell session.
```bash
source .env
```
Note: If your Cloud Shell session refreshes or you open a new terminal tab, you may need to run source .env again to reload these variables.

2. Create a dedicated service account for your Cloud Run service so that it has its own specific permission. Paste the following into the terminal:
```bash
gcloud iam service-accounts create ${SA_NAME} \
    --display-name="Service Account for cosmic signal "
```
3. Grant the service account the Vertex AI User role, which gives it permission to call Google's models.
```bash
# Grant the "Vertex AI User" role to your service account
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/aiplatform.user"
```

##  Deploy the agent using the ADK CLI

1. Run the following command in the terminal to deploy your agent.
```bash
# Run the deployment command
uvx --from google-adk==1.14.0 \
adk deploy cloud_run \
  --project=$PROJECT_ID \
  --region=europe-west1 \
  --service_name=cosmic-navigator-agent \
  --with_ui \
  . \
  -- \
  --labels=cosmos=ai-agent \
  --service-account=$SERVICE_ACCOUNT
```

The uvx command allows you to run command line tools published as Python packages without requiring a global installation of those tools.
Note: This deploy command below will take a few minutes to finish running.

2. If you are prompted with the following:

Deploying from source requires an Artifact Registry Docker repository to store built containers. A repository named [cloud-run-source-deploy] in region 
[europe-west1] will be created.
```bash
Do you want to continue (Y/n)?
```
If so, Type Y and hit ENTER.

3. If you are prompted with the following:
```bash
Allow unauthenticated invocations to [your-service-name] (y/N)?.
```
Type y and hit ENTER. This allows unauthenticated invocations for this lab for easy testing.

4. Now your URL is something look like this copy the URL and paste it into the web browser.
```bash
https://cosmic-navigator-agent-691424996495.europe-west1.run.app/
```
