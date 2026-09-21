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

Initial workstation implementation recorded Terraform as **IMPLEMENTED**
and runtime validation as **NOT EXECUTED** when the `terraform` binary was
absent. A later successful GitHub Actions run may update that status only
after the workflow is actually observed.
