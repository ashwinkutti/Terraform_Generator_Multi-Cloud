from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import subprocess
import json

app = FastAPI(
    title="Terraform Generator API",
    version="1.0.0"
)

# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================
# CACHE
# =========================================

terraform_cache = None

# =========================================
# LOAD TERRAFORM SCHEMA
# =========================================

def load_schema():

    global terraform_cache

    # CACHE
    if terraform_cache:
        return terraform_cache

    result = subprocess.run(
        "terraform providers schema -json",
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        shell=True
    )

   
    # TERRAFORM ERROR
    if result.stderr:
        return {
            "terraform_error": result.stderr
        }

    # EMPTY OUTPUT
    if not result.stdout:
        return {
            "error": "Terraform returned empty output"
        }

    try:

        terraform_cache = json.loads(
            result.stdout
        )

        return terraform_cache

    except Exception as e:

        return {
            "parse_error": str(e)
        }

# =========================================
# ROOT
# =========================================

@app.get("/")
def home():

    return {
        "status": "running",
        "message": "Terraform Generator API"
    }

# =========================================
# FULL SCHEMA
# =========================================

@app.get("/schema")
def schema():

    return load_schema()

# =========================================
# PROVIDERS
# =========================================

@app.get("/providers")
def providers():

    data = load_schema()

    if "provider_schemas" not in data:
        return data

    return list(
        data["provider_schemas"].keys()
    )

# =========================================
# AWS RESOURCES
# =========================================

@app.get("/resources/aws")
def aws_resources():

    data = load_schema()

    aws = data["provider_schemas"].get(
        "registry.terraform.io/hashicorp/aws"
    )

    if not aws:
        return {
            "error": "AWS provider not found"
        }

    return list(
        aws["resource_schemas"].keys()
    )

# =========================================
# AZURE RESOURCES
# =========================================

@app.get("/resources/azure")
def azure_resources():

    data = load_schema()

    azure = data["provider_schemas"].get(
        "registry.terraform.io/hashicorp/azurerm"
    )

    if not azure:
        return {
            "error": "Azure provider not found"
        }

    return list(
        azure["resource_schemas"].keys()
    )

# =========================================
# GCP RESOURCES
# =========================================

@app.get("/resources/gcp")
def gcp_resources():

    data = load_schema()

    gcp = data["provider_schemas"].get(
        "registry.terraform.io/hashicorp/google"
    )

    if not gcp:
        return {
            "error": "GCP provider not found"
        }

    return list(
        gcp["resource_schemas"].keys()
    )

# =========================================
# AWS RESOURCE SCHEMA
# =========================================

@app.get("/resource/aws/{resource_name}")
def aws_resource(resource_name: str):

    data = load_schema()

    aws = data["provider_schemas"].get(
        "registry.terraform.io/hashicorp/aws"
    )

    if not aws:
        return {
            "error": "AWS provider not found"
        }

    return aws["resource_schemas"].get(
        resource_name,
        {
            "error": f"{resource_name} not found"
        }
    )

# =========================================
# AZURE RESOURCE SCHEMA
# =========================================

@app.get("/resource/azure/{resource_name}")
def azure_resource(resource_name: str):

    data = load_schema()

    azure = data["provider_schemas"].get(
        "registry.terraform.io/hashicorp/azurerm"
    )

    if not azure:
        return {
            "error": "Azure provider not found"
        }

    return azure["resource_schemas"].get(
        resource_name,
        {
            "error": f"{resource_name} not found"
        }
    )

# =========================================
# GCP RESOURCE SCHEMA
# =========================================

@app.get("/resource/gcp/{resource_name}")
def gcp_resource(resource_name: str):

    data = load_schema()

    gcp = data["provider_schemas"].get(
        "registry.terraform.io/hashicorp/google"
    )

    if not gcp:
        return {
            "error": "GCP provider not found"
        }

    return gcp["resource_schemas"].get(
        resource_name,
        {
            "error": f"{resource_name} not found"
        }
    )

# =========================================
# SEARCH RESOURCES
# =========================================

@app.get("/search/{provider}/{keyword}")
def search_resources(
    provider: str,
    keyword: str
):

    data = load_schema()

    provider_map = {

        "aws":
        "registry.terraform.io/hashicorp/aws",

        "azure":
        "registry.terraform.io/hashicorp/azurerm",

        "gcp":
        "registry.terraform.io/hashicorp/google"
    }

    provider_key = provider_map.get(provider)

    if not provider_key:
        return {
            "error": "Invalid provider"
        }

    resources = data["provider_schemas"][
        provider_key
    ]["resource_schemas"]

    results = []

    for resource in resources.keys():

        if keyword.lower() in resource.lower():
            results.append(resource)

    return results