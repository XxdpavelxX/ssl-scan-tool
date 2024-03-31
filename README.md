# SSL Scan Tool

This is a simple SSL scan tool that performs a scan of a specified website using the SSL Labs API and generates a report with relevant security information. https://github.com/ssllabs/ssllabs-scan/blob/stable/ssllabs-api-docs.md

## Requirements

- Python 3.6 or higher
- Docker (optional)

## Usage

### Locally

Clone this repository:
git clone https://github.com/XxdpavelxX/ssl-scan-tool.git

Navigate to the project directory:
cd ssl-scan-tool

Install the required Python dependencies:
pip install -r requirements.txt

Run the Python script:
python ssl_scan.py

The SSL scan results will be printed to the console, and a log file named `logs/securityReport.log` will be generated in the project directory.

### With Docker

Clone this repository:
git clone https://github.com/XxdpavelxX/ssl-scan-tool.git

Navigate to the project directory:
cd ssl-scan-tool

Build the Docker image:
docker build -t ssl-scan .

Run a Docker container based on the built image:
docker run ssl-scan

The SSL scan results will be printed to the console, and a log file named `logs/securityReport.log` will be generated in the container.

## Output

The SSL scan results are printed to the console and also saved to a log file named `logs/securityReport.log`. You can find this log file in the project directory after running the script. If you run from Docker, the report wile will stay in the container.

## Explanation of Output
**Scan Start Time (scan_start)**: This value represents the timestamp when the SSL scan started. It's formatted as a string in the format %Y-%m-%d_%H-%M-%S.

**Scan Completion Time (scan_complete)**: This value represents the timestamp when the SSL scan completed. Similar to scan_start, it's formatted as a string in the format %Y-%m-%d %H:%M:%S.

**Overall Grade (overall_grade)**: This value indicates the overall grade assigned to the scanned website based on its SSL configuration. Grades typically range from 'A+' (highest) to 'F' (lowest) and are assigned based on various security criteria evaluated by the SSL Labs API.

**Status (status)**: This value represents the status of the SSL scan. It can be either 'IN_PROGRESS' if the scan is still ongoing, or 'READY' if the scan has been completed.

**Protocol Support (protocol_support)**: This value provides information about the supported protocols by the scanned website. It typically includes details such as supported SSL/TLS versions and cipher suites.

**Certificate (certificate)**: This value contains information about the SSL certificate used by the scanned website, including details such as the issuer and subject.

**Names (names)**: This value represents the common names associated with the SSL certificate of the scanned website.

**Alternative Names (alt_names)**: This value contains alternative names (subject alternative names) associated with the SSL certificate of the scanned website.

**Secure Renegotiation (secure_renegotiation)**: This value indicates whether secure renegotiation is supported by the scanned website.

**HSTS (hsts)**: This value indicates whether HTTP Strict Transport Security (HSTS) is enabled for the scanned website.

**Protocol Details (protocol_details)**: This value provides detailed information about the SSL/TLS protocols supported by the scanned website, including configuration details and vulnerabilities.

**Heartbleed Vulnerability (heartbleed_vulnerability)**: This value indicates whether the Heartbleed vulnerability is present in the scanned website's SSL configuration.

**Poodle Vulnerability (poodle_vulnerability)**: This value indicates whether the POODLE vulnerability is present in the scanned website's SSL configuration.

**Freak Vulnerability (freak_vulnerability)**: This value indicates whether the FREAK vulnerability is present in the scanned website's SSL configuration.

**OpenSSL CCS Injection Test (openSslCcs_test_results)**: This value represents the results of the OpenSSL CCS Injection test, indicating whether the scanned website is vulnerable to the OpenSSL CCS Injection vulnerability.

**OpenSSLLuckyMinus20 Test (openSslLucky_test_results)**: This value represents the results of the OpenSSL LuckyMinus20 test, indicating whether the scanned website is vulnerable to the LuckyMinus20 vulnerability.

**Poodle TLS Test (poodle_test_results)**: This value represents the results of the POODLE TLS test, indicating whether the scanned website is vulnerable to the POODLE TLS vulnerability.

These return values provide comprehensive information about the SSL scan results for the scanned website, including security grades, protocol support, certificate details, and vulnerability assessments.


## Questions and Answers
### 1. How would you scale this script and run it with resiliency to e.g. handle 1000s of domains?
Scaling the script to handle thousands of domains and ensuring resiliency can be achieved through several approaches.
Below are some steps to take.
1) I would first start by modifying the script in ssl_scan.py so that the target url for scanning is 
not hard coded to be https://www.elliottmgmt.com/. And instead have it be passed as a parameter (ie via the python click library)
to the function. This way users can run the tool on other domains as well. 
2) Then I would break down the task of scanning thousands of domains into smaller chunks and distribute them across multiple worker instances. Each worker instance can handle a subset of domains concurrently. Having multiple workers would also increase the availability of the service, we can also distribute these workers across multiple AZs and regions.
3) To help with this I may implement a Queueing system, for example with AWS SQS. To manage the list of domains to be scanned. When a worker is available, it can fetch a domain from the queue, perform the scan, and report the results back.
4) I would also add autoscaling groups if running on AWS to automatically add or remove worker instances based on demand.
5) I would also implement load balancing to evenly distribute incoming requests across the multiple instances of the application. This would ensure that no single instance becomes overwhelmed with requests.
6) I would also modify the generated logfile name from securityReport.log to include the timestamp and domain name at the end, this way instances could hold multiple log files.

### 2. How would you monitor/alert on this service?
There are several layers of monitoring, metrics, and alerting that you could implement for this service depending on how it's deployed. We can use different tools depending on our cloud provider, and whether we use K8s, regular servers (ie AWS EC2s), or serverless (ie AWS Lambda). Below I will describe how I would monitor the service assuming our cloud provider is AWS.
1) I will use AWS CloudWatch to collect and monitor metrics generated by the SSL scanning service. I'll publish custom metrics to CloudWatch using the AWS CLI. Some example metrics to monitor may include the number of domains scanned, scan duration, error rates, cpu utilization, memory utilization, disk utilization, 4XX error rate, 5XX error rate.
2) I will also use AWS CloudWatch Logs. To do this I can configure the SSL scanning service to log important events and errors to CloudWatch Logs. This can be done using the AWS CLI to send log data to CloudWatch Logs. I can also define log streams for different components of the service (e.g., scanning, error handling) to facilitate troubleshooting and analysis.
3) I can then CloudWatch Alarms to monitor the metrics created earlier and trigger alerts when predefined thresholds are breached. For example, we can set up alarms to alert the team if the number of failed scans exceeds a certain threshold or if the cpu utilization exceeds it's threshold.
4) I can also integrate CloudWatch Alarms with Amazon SNS to send notifications to administrators or operators when alerts are triggered. SNS topics will be configured to deliver notifications via email, SMS, or other protocols.
5) Another way to monitor the service can be with AWS AutoScaling Groups. AutoScaling Groups can check the health of the service and deploy new instances if old ones are unhealthy.
6) We can also use AWS Lambda functions to perform automated remediation actions in response to alerts. These actions can be anything we program such as restarting instances, or performing other custom actions.
7) For additional monitoring we can also implement 3rd party tools such as Datadog, New Relic, Prometheus, Grafana (if on K8s) to collect and visualize metrics from the service. These tools provide dashboards for real-time monitoring and historical analysis of metrics.
8) For additional alerting we can implement 3rd party tools such as PagerDuty.

### 3. What would you do to handle adding new domains to scan or certificate expiry events from your service?
To handle adding new domains to scan I would follow a lot of the same steps that I mentioned in the answer to the first question.
1) I would first start by modifying the script in ssl_scan.py so that the target url for scanning is 
not hard coded to be https://www.elliottmgmt.com/. And instead have it be passed as a parameter (ie via the python click library)
to the function. This way users can dynamically pass the domain that they want to scan as an argument when running the file.
2) To automatically run on new domains I would implement a scheduled task to periodically check for new domains that need to be scanned or domains with expiring certificates. These new domains would come from a Queue such as AWS SQS. I can use cron jobs or scheduling services (e.g., AWS CloudWatch Events) to trigger the scanning process at regular intervals.
3) For certificate expiry monitoring I would add an extra function to check the expiration dates of SSL certificates associated with scanned domains. If a certificate is found to be nearing expiry, that function would raise an alert to notify administrators or operators to take appropriate action (e.g., renewing the certificate). This notification could be triggered via an api integration (ie slack, pagerduty) or using email. This could be added directly to the codebase or to a lambda function that the code would trigger if expiry is near.

### 4. After some time, your report requires more enhancements requested by the Tech team of the company. How would you handle these "continuous" requirement changes in a sustainable manner?
1) I would adopt Agile methodologies such as Scrum or Kanban to manage development efforts iteratively and incrementally. Break down requirements into small, manageable tasks or user stories, and prioritize them based on business value and stakeholder feedback. I would then use that do design a roadmap to present to stakeholders. And I'd maintain regular communication with stakeholders including doing demos, design reviews, and regular progress updates.
2) I would implement gitops standard practices such as development branches, and required code reviews before merging.
3) I would also implement standard CI/CD practices by implementing a CI/CD pipeline, scanning and testing tools, automated tests, and multiple deployment environments (ie testing, pre-prod, prod).
4) For infrastructure configurations I would use IaC tools such as AWS CDK or Terraform. This way we could infrastructure components programmatically, enabling reproducible and scalable deployments, improved visibility, and rollbacks across environments.
