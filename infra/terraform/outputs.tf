output "namespace" {
  value       = kubernetes_namespace_v1.order_intake.metadata[0].name
  description = "Provisioned namespace name."
}

output "quota_name" {
  value       = kubernetes_resource_quota_v1.namespace_quota.metadata[0].name
  description = "ResourceQuota name."
}

output "service_account" {
  value       = kubernetes_service_account_v1.order_intake.metadata[0].name
  description = "Workload service account name."
}
