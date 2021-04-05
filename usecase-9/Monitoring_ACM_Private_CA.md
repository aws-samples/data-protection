## Security Monitoring:
![alt text](img/architecture.png)

In this section we will look at how to monitor privileged actions as you build your certificate management infrastructure. We will study two scenerios. The creation of a CA Certificate and mass revocation of end entity certificates. 

#### 13. [Scenario 1]: Monitoring with Security Hub
Creating a CA Certificate is a privileged action that should only be taken by authorized personnel within the CA Hierarchy Management team. For this reason we want to monitor the creation of any CA Certificate within our hierarchy. 

To do this we will check the findings within Security Hub: [View results](https://view.highspot.com/viewer/5e9f63cbc714332ad7cba2f6).

#### 14. [Scenario 2]: Monitor Mass Revocation
This scenario shows a developer revoking many end-entity certificates within a short period of time. We want to monitor and notify the security team if this type of privileged action takes place in order to investigate.

#### 15. Create/Revoke End-Entity Certificates
First we will act as the Developer by creating and then revoking many certificates at once: [Mass revocation](https://view.highspot.com/viewer/5da634e266bbaa2860b471a7)

#### 16. Quiz time. Open this link in a new browser tab : [Quiz](https://amazonmr.au1.qualtrics.com/jfe/form/SV_3mHHKwvVlxQ0v1X)

#### 17. Monitor revocation of certificates
We will navigate to Security Hub in order to monitor revocation of certificates: [View results](https://view.highspot.com/viewer/5ef51b34a2e3a9211e98c434)
