variable "namespace" {
  type        = string
  description = "Platform namespace for the Order Intake PoV."
  default     = "order-intake-pov"
}

variable "kubeconfig_path" {
  type        = string
  description = "Optional kubeconfig path. Leave empty when using host+token."
  default     = ""
}

variable "kubeconfig_context" {
  type        = string
  description = "Optional kubeconfig context."
  default     = ""
}

variable "kubernetes_host" {
  type        = string
  description = "Optional Kubernetes API host."
  default     = ""
}

variable "kubernetes_token" {
  type        = string
  description = "Optional bearer token. Do not commit real tokens."
  default     = ""
  sensitive   = true
}

variable "kubernetes_insecure" {
  type        = bool
  description = "Skip TLS verify. Default false."
  default     = false
}

variable "quota_cpu" {
  type        = string
  description = "Namespace CPU quota."
  default     = "2"
}

variable "quota_memory" {
  type        = string
  description = "Namespace memory quota."
  default     = "4Gi"
}

variable "platform_labels" {
  type        = map(string)
  description = "Labels applied to the namespace."
  default = {
    "app.kubernetes.io/part-of" = "hybrid-cloud-modernization-pov"
    "purpose"                   = "proof-of-value"
  }
}
