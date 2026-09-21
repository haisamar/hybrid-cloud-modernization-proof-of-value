# Terraform — platform prerequisites

This stack declares **environment** objects for an OpenShift-compatible
cluster. It does **not** duplicate the application Deployment, Service, or
Route. Those remain in `deploy/openshift/`.

Resources:

- namespace + labels
- platform ConfigMap
- ResourceQuota and LimitRange
- service account

## Commands

If Terraform is installed:

```bash
terraform fmt -check
terraform init -backend=false
terraform validate
```

`terraform plan` / `terraform apply` require a real kubeconfig or API
credentials. They were **not** executed unless `docs/implementation-status.md`
records otherwise. Never invent plan/apply output.

GitHub Actions workflow **validate #2** on commit `518e3d0` ran
`terraform fmt -check`, `terraform init -backend=false`, and
`terraform validate`. That is **TESTED IN CI**. It is not `terraform plan`
or `terraform apply`. See `docs/implementation-status.md`.
