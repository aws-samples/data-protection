# Module 2: Attack Simulation

Now that you have detective and responsive controls setup, you'll be running another CloudFormation template which will simulate the actual attack you will be investigating.

**Agenda**

1. Run the second CloudFormation template – 5 min
2. Threat detection and response presentation – 25 min

## Deploy the CloudFormation template

To initiate the attack simulation you will need to run the module 2 CloudFormation template: 

!!! info "Before you deploy the CloudFormation template feel free to view it <a href="https://github.com/aws-samples/aws-scaling-threat-detection-workshop/blob/master/templates/02-attack-simulation.yml" target="_blank">repo</a href>."

Region| Deploy
------|-----
US West 2 (Oregon) | <a href="https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=ThreatDetectionWksp-Attacks&templateURL=https://s3-us-west-2.amazonaws.com/sa-security-specialist-workshops-us-west-2/threat-detect-workshop/staging/02-attack-simulation.yml" target="_blank">![Deploy Module 2 in us-west-2](./images/deploy-to-aws.png)</a>

1. Click the **Deploy to AWS** button above.  This will automatically take you to the console to run the template.  

2. The name of the stack will be automatically populated but you are free to change it, after which click **Next**, then **Next** again (leave everything on this page at the default).  

3. Finally, acknowledge that the template will create IAM roles and click **Create**

![IAM Capabilities](./images/iam-capabilities.png)

This will bring you back to the CloudFormation console. You can refresh the page to see the stack starting to create. Before moving on, make sure the stack is in a **CREATE_COMPLETE** status as shown below.

![Stack Complete](./images/02-stack-complete.png)

## Architecture overview

Below is a diagram of the setup after the module 2 CloudFormation stack is created.

![Module 2 Diagram](./images/02-diagram-module2-3.png)

!!! warning "Threat detection and response presentation"
    **AWS Sponsored Event**: If you are going through this workshop in a classroom setting then wait till the presentation is over before starting module 3 (the presentation will allow enough time to pass for the attack scenario to complete.)

    **Individual**: If you are going through this workshop outside of a classroom setting you can proceed to Module 3.  Please note it will take at least **20 minutes** after the 2nd CloudFormation template has completed before you will start seeing findings.