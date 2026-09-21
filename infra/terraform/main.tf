resource "kubernetes_namespace_v1" "order_intake" {
  metadata {
    name   = var.namespace
    labels = var.platform_labels
  }
}

resource "kubernetes_config_map_v1" "platform" {
  metadata {
    name      = "order-intake-platform"
    namespace = kubernetes_namespace_v1.order_intake.metadata[0].name
    labels    = var.platform_labels
  }

  data = {
    PLATFORM                 = "openshift-compatible"
    PERSISTENCE_MODE         = "sqlite-pov"
    REPLICAS_POLICY          = "1"
    DATABASE_MODERNIZATION   = "out-of-scope"
  }
}

resource "kubernetes_resource_quota_v1" "namespace_quota" {
  metadata {
    name      = "order-intake-quota"
    namespace = kubernetes_namespace_v1.order_intake.metadata[0].name
  }

  spec {
    hard = {
      "requests.cpu"    = var.quota_cpu
      "requests.memory" = var.quota_memory
      "limits.cpu"      = var.quota_cpu
      "limits.memory"   = var.quota_memory
      pods              = "4"
    }
  }
}

resource "kubernetes_limit_range_v1" "defaults" {
  metadata {
    name      = "order-intake-limits"
    namespace = kubernetes_namespace_v1.order_intake.metadata[0].name
  }

  spec {
    limit {
      type = "Container"
      default = {
        cpu    = "250m"
        memory = "256Mi"
      }
      default_request = {
        cpu    = "50m"
        memory = "128Mi"
      }
    }
  }
}

resource "kubernetes_service_account_v1" "order_intake" {
  metadata {
    name      = "order-intake"
    namespace = kubernetes_namespace_v1.order_intake.metadata[0].name
    labels    = var.platform_labels
  }
}
