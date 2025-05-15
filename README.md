# pvc-extract
![ci workflow](https://github.com/Surote/pvc-extract/actions/workflows/ci.yaml/badge.svg)

## Why
- this project mainly for quely result from `compliance-operator` in `OpenShift Container Platform 4` in `HTML` format.

**Vibe coding**

<img width="391" alt="Screenshot 2568-04-24 at 21 37 21" src="https://github.com/user-attachments/assets/e4f35479-a85c-4b9a-bb5d-71202b147c7c" />

<img width="732" alt="Screenshot 2568-04-24 at 21 37 27" src="https://github.com/user-attachments/assets/a04a45ef-2522-4e93-b43c-d4f8ce281cab" />

## Usage for Compliance 

- Use `deployment_compliance_get_result_example` to deploy in the `openshift-compliance` namespace.
- Apply the `route` and `service`.
- Access the application using the `URL`, which can be found by running `oc get route -n openshift-compliance`.

## Usage for Other Purposes, Such as Checking Files in a PVC

- You must have a claimable `PVC`.
- Use `deployment_other_purpose.yaml`:
    - Replace `replace-me-pvc-name` with the name of your PVC.
    - Replace `replace-me-with-password-or-delete-me` with your password or remove it if not needed.
- Apply the `route` and `service`.
- Access the application using the `URL`, which can be found by running `oc get route -n <your namespace>`.