variable "project" {
  description = "linux-distro-popularity"
  type        = string
}

variable "region" {
  description = "Your project region"
  default     = "us-west1"
  type        = string
}

variable "zone" {
  description = "Your project zone"
  default     = "us-west1-a"
  type        = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "ldp-bq"
}

# variable "vm_image" {
#   description = "Image for your VM"
#   default     = "ubuntu-os-cloud/ubuntu-2004-lts"
#   type        = string
# }

variable "network" {
  description = "Network for your instance/cluster"
  default     = "default"
  type        = string
}

variable "stg_bq_dataset" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "ldp_stg"
  type        = string
}

variable "prod_bq_dataset" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "ldp_prod"
  type        = string
}

variable "bucket" {
  description = "The name of your bucket. This should be unique across GCP"
  type        = string
}