<template>
  <div class="app">

    <!-- HEADER -->
    <header class="topbar">

      <div>
        <h1>Terraform Generator</h1>
        <p>
          Multi-Cloud Infrastructure as Code Builder
        </p>
      </div>

      <button
        class="primary-btn"
        @click="generateTerraform"
      >
        Generate Terraform
      </button>

    </header>

    <!-- MAIN -->
    <main class="main-layout">

      <!-- LEFT PANEL -->
      <section class="card sidebar">

        <div class="section-title">
          <h2>Cloud Provider</h2>
          <span>Select Platform</span>
        </div>

        <!-- PROVIDERS -->

        <div class="provider-grid">

          <button
            v-for="item in providers"
            :key="item"
            :class="[
              'provider-btn',
              provider === item ? 'active' : ''
            ]"
            @click="selectProvider(item)"
          >
            {{ item }}
          </button>

        </div>

        <!-- CATEGORY -->

        <div class="form-group">

          <label>Category</label>

          <select
            v-model="category"
            @change="updateServices"
          >

            <option
              v-for="item in categories"
              :key="item"
            >
              {{ item }}
            </option>

          </select>

        </div>

        <!-- SERVICE -->

        <div class="form-group">

          <label>Service</label>

          <select
            v-model="service"
            @change="loadDefaults"
          >

            <option
              v-for="item in services"
              :key="item"
            >
              {{ item }}
            </option>

          </select>

        </div>

      </section>

      <!-- CENTER PANEL -->

      <section class="card config-panel">

        <div class="section-title">

          <div>
            <h2>Configuration</h2>
            <span>
              Security Best Practice Defaults
            </span>
          </div>

          <div class="service-badge">
            {{ service }}
          </div>

        </div>

        <div
          class="config-item"
          v-for="(value, key) in config"
          :key="key"
        >

          <label>
            {{ formatLabel(key) }}
          </label>

          <input v-model="config[key]" />

        </div>

      </section>

      <!-- RIGHT PANEL -->

      <section class="card output-panel">

        <div class="section-title">

          <div>
            <h2>Terraform Output</h2>
            <span>
              Generated Terraform Script
            </span>
          </div>

          <div class="actions">

            <button @click="selectAll">
              Select All
            </button>

            <button @click="copyCode">
              Copy
            </button>

          </div>

        </div>

        <textarea
          ref="terraformBox"
          v-model="terraformCode"
        ></textarea>

      </section>

    </main>

  </div>
</template>

<script setup>
import {
  ref,
  reactive,
  onMounted
} from 'vue'

/* PROVIDERS */

const providers = [
  'AWS',
  'Azure',
  'GCP'
]

/* CATEGORIES */

const categories = [
  'Compute',
  'Storage',
  'Networking',
  'Kubernetes',
  'Security',
  'Database',
  'Monitoring',
  'DevOps',
  'AI/ML'
]

/* STATE */

const provider = ref('AWS')
const category = ref('Compute')
const service = ref('EC2')

const services = ref([])

const terraformCode = ref('')

const terraformBox = ref(null)

const config = reactive({})

/* SERVICES */

const serviceMap = {

  AWS: {

    Compute: [
      'EC2',
      'Lambda',
      'ECS',
      'Batch',
      'Lightsail'
    ],

    Storage: [
      'S3',
      'EFS',
      'EBS',
      'FSx'
    ],

    Networking: [
      'VPC',
      'Route53',
      'CloudFront',
      'API Gateway'
    ],

    Kubernetes: [
      'EKS',
      'ECR'
    ],

    Security: [
      'IAM',
      'KMS',
      'Secrets Manager',
      'WAF'
    ],

    Database: [
      'RDS',
      'DynamoDB',
      'Aurora',
      'Redshift'
    ],

    Monitoring: [
      'CloudWatch',
      'CloudTrail'
    ],

    DevOps: [
      'CodePipeline',
      'CodeBuild',
      'CloudFormation'
    ],

    'AI/ML': [
      'SageMaker',
      'Bedrock'
    ]
  },

  Azure: {

    Compute: [
      'Virtual Machine',
      'Functions',
      'App Service'
    ],

    Storage: [
      'Blob Storage',
      'Disk Storage'
    ],

    Networking: [
      'Virtual Network',
      'Load Balancer'
    ],

    Kubernetes: [
      'AKS'
    ],

    Security: [
      'Key Vault',
      'Defender'
    ],

    Database: [
      'Azure SQL',
      'Cosmos DB'
    ],

    Monitoring: [
      'Azure Monitor'
    ],

    DevOps: [
      'Azure DevOps'
    ],

    'AI/ML': [
      'Azure OpenAI'
    ]
  },

  GCP: {

    Compute: [
      'Compute Engine',
      'Cloud Run',
      'Cloud Functions'
    ],

    Storage: [
      'Cloud Storage',
      'Persistent Disk'
    ],

    Networking: [
      'VPC',
      'Cloud CDN'
    ],

    Kubernetes: [
      'GKE'
    ],

    Security: [
      'Cloud IAM',
      'Secret Manager'
    ],

    Database: [
      'Cloud SQL',
      'Firestore'
    ],

    Monitoring: [
      'Cloud Monitoring'
    ],

    DevOps: [
      'Cloud Build'
    ],

    'AI/ML': [
      'Vertex AI',
      'Gemini API'
    ]
  }
}

/* DEFAULT CONFIGS */

const defaults = {

  EC2: {
    instance_name: 'production-ec2',
    ami: 'ami-123456',
    instance_type: 't3.micro',
    region: 'us-east-1',

    enable_monitoring: 'true',
    encrypted_root_volume: 'true',
    metadata_v2_required: 'true',
    ebs_optimized: 'true',

    public_ip: 'false',

    security_group_name: 'secure-ec2-sg',

    allowed_ssh_cidr: '10.0.0.0/24',

    backup_enabled: 'true',

    environment: 'production'
  },

  Lambda: {
    function_name: 'secure-lambda',
    runtime: 'nodejs18.x',
    timeout: '30',
    memory_size: '512',

    tracing_enabled: 'true',

    dead_letter_queue: 'true',

    reserved_concurrency: '5'
  },

  S3: {
    bucket_name: 'secure-bucket',
    region: 'us-east-1',

    encryption_enabled: 'true',

    block_public_access: 'true',

    versioning_enabled: 'true',

    kms_encryption: 'true',

    access_logging: 'true'
  },

  VPC: {
    vpc_name: 'production-vpc',
    cidr_block: '10.0.0.0/16',

    enable_dns_support: 'true',

    enable_dns_hostnames: 'true',

    nat_gateway_enabled: 'true',

    flow_logs_enabled: 'true'
  },

  RDS: {
    db_name: 'appdb',
    engine: 'mysql',
    engine_version: '8.0',

    instance_class: 'db.t3.micro',

    storage_encrypted: 'true',

    multi_az: 'true',

    backup_retention_days: '7',

    deletion_protection: 'true',

    publicly_accessible: 'false'
  },

  EKS: {
    cluster_name: 'secure-eks-cluster',

    kubernetes_version: '1.29',

    node_type: 't3.medium',

    node_count: '2',

    endpoint_private_access: 'true',

    secrets_encryption: 'true'
  },

  'Virtual Machine': {
    vm_name: 'secure-vm',

    size: 'Standard_B2s',

    location: 'East US',

    os_disk_encryption: 'true',

    boot_diagnostics: 'true',

    enable_monitoring: 'true',

    public_ip_enabled: 'false',

    backup_enabled: 'true'
  },

  'Azure SQL': {
    server_name: 'secure-sql-server',

    db_name: 'appdb',

    transparent_data_encryption: 'true',

    geo_backup_enabled: 'true',

    threat_detection: 'true',

    public_network_access: 'false'
  },

  AKS: {
    cluster_name: 'secure-aks-cluster',

    kubernetes_version: '1.29',

    node_count: '2',

    private_cluster_enabled: 'true',

    azure_policy_enabled: 'true'
  },

  'Compute Engine': {
    vm_name: 'secure-gcp-instance',

    machine_type: 'e2-medium',

    zone: 'us-central1-a',

    shielded_vm: 'true',

    secure_boot: 'true',

    integrity_monitoring: 'true',

    public_ip_enabled: 'false'
  },

  GKE: {
    cluster_name: 'secure-gke-cluster',

    node_count: '2',

    private_nodes: 'true',

    workload_identity: 'true',

    network_policy: 'true'
  },

  'Cloud SQL': {
    db_instance: 'secure-cloudsql',

    database_version: 'MYSQL_8_0',

    backup_enabled: 'true',

    binary_logging: 'true',

    deletion_protection: 'true'
  },

  SageMaker: {
    notebook_name: 'secure-ml-notebook',

    instance_type: 'ml.t3.medium',

    encryption_enabled: 'true',

    network_isolation: 'true'
  },

  'Azure OpenAI': {
    service_name: 'enterprise-openai',

    sku: 'S0',

    private_endpoint: 'true',

    diagnostics_enabled: 'true'
  },

  'Vertex AI': {
    endpoint_name: 'secure-vertex-ai',

    encryption_enabled: 'true',

    private_endpoint: 'true'
  }
}

/* PROVIDER */

function selectProvider(item) {

  provider.value = item

  updateServices()
}

/* UPDATE SERVICES */

function updateServices() {

  services.value =
    serviceMap[provider.value][category.value]

  service.value = services.value[0]

  loadDefaults()
}

/* LOAD DEFAULTS */

function loadDefaults() {

  Object.keys(config).forEach(
    key => delete config[key]
  )

  const data =
    defaults[service.value] || {
      name: 'demo-resource'
    }

  Object.entries(data).forEach(
    ([key, value]) => {
      config[key] = value
    }
  )

  generateTerraform()
}

/* GENERATE TERRAFORM */

function generateTerraform() {

  let terraformFields = ''

  Object.entries(config).forEach(
    ([key, value]) => {

      terraformFields += `
  ${key} = "${value}"`
    }
  )

  terraformCode.value = `
# ====================================
# Terraform Generated Resource
# ====================================

terraform {
  required_version = ">= 1.5.0"
}

provider "${provider.value.toLowerCase()}" {

}

resource "${provider.value.toLowerCase()}_${service.value.toLowerCase().replaceAll(' ', '_')}" "main" {
${terraformFields}
}
`.trim()
}

/* COPY */

function copyCode() {

  navigator.clipboard.writeText(
    terraformCode.value
  )

  alert('Terraform copied!')
}

/* SELECT */

function selectAll() {
  terraformBox.value.select()
}

/* LABEL */

function formatLabel(text) {

  return text
    .replaceAll('_', ' ')
}

/* INIT */

onMounted(() => {
  updateServices()
})
</script>

<style scoped>

/* RESET */

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* APP */

.app {
  min-height: 100vh;
  width: 100%;
  background: #f5f7fb;
  padding: 20px;
  font-family: Inter, sans-serif;
  color: #1e293b;

  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

/* HEADER */

.topbar {
  width: 100%;

  display: flex;
  justify-content: space-between;
  align-items: center;

  margin-bottom: 20px;
  gap: 20px;
  flex-wrap: wrap;
}

.topbar h1 {
  font-size: 34px;
  font-weight: 700;
}

.topbar p {
  margin-top: 6px;
  color: #64748b;
}

/* MAIN */

.main-layout {

  width: 100%;

  display: grid;

  grid-template-columns:
    260px
    340px
    minmax(950px, 1fr);

  gap: 20px;

  min-height: calc(100vh - 120px);

  align-items: start;
}

/* CARD */

.card {
  background: white;

  border-radius: 24px;

  padding: 24px;

  border: 1px solid #e2e8f0;

  box-shadow:
    0 10px 30px rgba(15, 23, 42, 0.04);
}

/* TITLES */

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;

  gap: 12px;

  margin-bottom: 24px;
}

.section-title h2 {
  font-size: 22px;
  font-weight: 700;
}

.section-title span {
  color: #64748b;
  font-size: 14px;
}

/* PROVIDERS */

.provider-grid {
  display: grid;

  grid-template-columns: repeat(3, 1fr);

  gap: 10px;
}

.provider-btn {

  border: none;

  padding: 14px;

  border-radius: 14px;

  background: #eef2ff;

  color: #475569;

  font-weight: 600;

  cursor: pointer;

  transition: 0.2s;
}

.provider-btn:hover {
  transform: translateY(-2px);
}

.provider-btn.active {
  background: #6366f1;
  color: white;
}

/* FORM */

.form-group {
  margin-top: 22px;
}

.form-group label,
.config-item label {

  display: block;

  margin-bottom: 10px;

  font-weight: 600;

  color: #475569;

  text-transform: capitalize;
}

select,
input {

  width: 100%;

  padding: 14px;

  border-radius: 14px;

  border: 1px solid #dbeafe;

  background: #f8fafc;

  outline: none;

  font-size: 14px;
}

select:focus,
input:focus {

  border-color: #6366f1;

  background: white;
}

/* CONFIG */

.config-item {
  margin-bottom: 18px;
}

.service-badge {

  background: #eef2ff;

  color: #4338ca;

  padding: 8px 14px;

  border-radius: 999px;

  font-size: 13px;

  font-weight: 600;
}

/* BUTTONS */

.actions {
  display: flex;
  gap: 10px;
}

.actions button,
.primary-btn {

  border: none;

  padding: 12px 18px;

  border-radius: 14px;

  background: #6366f1;

  color: white;

  cursor: pointer;

  font-weight: 600;

  transition: 0.2s;
}

.actions button:hover,
.primary-btn:hover {

  background: #4f46e5;
}

/* OUTPUT */

.output-panel {

  display: flex;

  flex-direction: column;

  width: 100%;

  min-width: 950px;
}

textarea {

  flex: 1;

  width: 100%;

  min-height: 82vh;

  border: none;

  resize: none;

  border-radius: 18px;

  padding: 24px;

  background: #f8fafc;

  color: #0f172a;

  font-size: 14px;

  line-height: 1.8;

  font-family:
    Consolas,
    Monaco,
    monospace;

  border: 1px solid #e2e8f0;

  overflow: auto;

  white-space: pre;

  tab-size: 2;
}

/* RESPONSIVE */

@media (max-width: 1400px) {

  .main-layout {

    grid-template-columns:
      240px
      320px
      1fr;
  }

  .output-panel {
    min-width: unset;
  }
}

@media (max-width: 1100px) {

  .main-layout {
    grid-template-columns: 1fr;
  }

  textarea {
    min-height: 500px;
  }
}

@media (max-width: 768px) {

  .app {
    padding: 14px;
  }

  .topbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .topbar h1 {
    font-size: 28px;
  }

  .provider-grid {
    grid-template-columns: 1fr;
  }

  .section-title {
    flex-direction: column;
    align-items: flex-start;
  }

  .actions {
    width: 100%;
  }

  .actions button {
    flex: 1;
  }
}

</style>