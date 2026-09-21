provider "kubernetes" {
  # Supply a kubeconfig or host+token at apply time. Nothing is applied in this PoV
  # unless terraform apply is genuinely executed against a cluster.
  config_path    = var.kubeconfig_path == "" ? null : var.kubeconfig_path
  config_context = var.kubeconfig_context == "" ? null : var.kubeconfig_context
  host           = var.kubernetes_host == "" ? null : var.kubernetes_host
  token          = var.kubernetes_token == "" ? null : var.kubernetes_token
  insecure       = var.kubernetes_insecure
}
