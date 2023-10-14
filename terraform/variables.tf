variable "project" {
  description = "linux-distro-popularity "
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