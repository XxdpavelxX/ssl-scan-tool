#! /usr/bin/env python3

"""
SSL Scan Tool

This script performs SSL scans of specified websites using the SSL Labs API and generates a report with relevant security information.

Usage:
python ssl_scan.py

The SSL scan results will be printed to the console, and a log file named '/logs/securityReport.log' will be generated in the project directory.
"""

import requests
import datetime
import logging

logging.basicConfig(filename='logs/securityReport.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# The URL of the SSL Labs API
API_URL = 'https://api.ssllabs.com/api/v2/analyze'
# Our target website
TARGET_URL = 'https://www.elliottmgmt.com/'

def perform_ssl_scan(target_url):
    # Parameters for our API request
    params = {
        'host': target_url,
        'all': 'done'
    }

    try:
        response = requests.get(API_URL, params=params)
        
        if response.status_code == 200:
            results = response.json()

            scan_start = datetime.datetime.fromtimestamp(results['startTime']/1000, tz=datetime.timezone.utc, ).strftime('%Y-%m-%d_%H-%M-%S')
            status = results['status']

            with open('logs/securityReport.log', 'w') as f:
                if status == 'IN_PROGRESS':
                    logging.info("SSL scan is still in progress. Please wait ~2 minutes for the scan to complete and then rerun this file.")
                    f.write("SSL scan is still in progress. Please wait ~2 minutes for the scan to complete.\n")
                    return {
                        'Scan Start Time': scan_start,
                        'Status': status,
                        'Message': 'SSL scan is still in progress. Please wait ~2 minutes for the scan to complete and then rerun this file.'
                    }
                else:
                    logging.info("SSL scan is complete. Retrieving results...")
                    f.write("SSL scan is complete. Retrieving results...\n")
                    scan_complete = datetime.datetime.fromtimestamp(results['testTime']/1000, tz=datetime.timezone.utc, ).strftime('%Y-%m-%d %H:%M:%S')
                    overall_grade = results['endpoints'][0]['grade']

                    protocol_support = results['endpoints'][0]['details']['protocols']
                    certificate = results['endpoints'][0]['details']['cert']['issuerSubject']
                    names = results['endpoints'][0]['details']['cert']['commonNames']
                    alt_names = results['endpoints'][0]['details']['cert']['altNames']
                    secure_renegotiation = results['endpoints'][0]['details']['renegSupport']
                    hsts = results['endpoints'][0]['details']['hstsPolicy']
                    protocol_details = results['endpoints'][0]['details']['protocols']
                    heartbleed_vulnerability = results['endpoints'][0]['details']['heartbleed']
                    poodle_vulnerability = results['endpoints'][0]['details']['poodle'],
                    freak_vulnerability =  results['endpoints'][0]['details']['freak'],
                    openSslCcs_test_results = results['endpoints'][0]['details']['openSslCcs'],
                    openSslLucky_test_results = results['endpoints'][0]['details']['openSSLLuckyMinus20'],
                    poodle_test_results = results['endpoints'][0]['details']['poodleTls'],

                    logging.info("Scar Start Time: %s", scan_start)
                    logging.info("Scan Completion Time: %s", scan_complete)
                    logging.info("Overall Grade: %s", overall_grade)
                    logging.info("Status: %s", status)
                    logging.info("Protocol Support: %s", protocol_support)
                    logging.info("Certificate: %s", certificate)
                    logging.info("Names: %s", names)
                    logging.info("Alternative Names: %s", alt_names)
                    logging.info("Secure Renegotiation: %s", secure_renegotiation)
                    logging.info("HSTS: %s", hsts)
                    logging.info("Protocol Details: %s", protocol_details)
                    logging.info("Heartbleed Vulnerability: %s", heartbleed_vulnerability)
                    logging.info("Poodle Vulnerability: %s", poodle_vulnerability)
                    logging.info("Freak Vulnerability: %s", freak_vulnerability)
                    logging.info("OpenSSL CCS Injection Test: %s", openSslCcs_test_results)
                    logging.info("OpenSSLLuckyMinus20 Test: %s", openSslLucky_test_results)
                    logging.info("Poodle TLS Test: %s", poodle_test_results)

                    return {
                        'Scar Start Time': scan_start,
                        'Scan Completion Time': scan_complete,
                        'Overall Grade': overall_grade,
                        'Status': status,
                        'Protocol Support': protocol_support,
                        'Certificate': certificate,
                        'Names': names,
                        'Alternative Names': alt_names,
                        'Secure Renegotiation': secure_renegotiation,
                        'HSTS': hsts,
                        'Protocol Details': protocol_details,
                        'Heartbleed Vulnerability': heartbleed_vulnerability,
                        'Poodle Vulnerability': poodle_vulnerability,
                        'Freak Vulnerability': freak_vulnerability,
                        'OpenSSL CCS Injection Test': openSslCcs_test_results,
                        'OpenSSLLuckyMinus20 Test': openSslLucky_test_results,
                        'Poodle TLS Test': poodle_test_results,
                    }
        else:
            logging.error("Error: Failed to get SSL scan results. Status code: %s", response.status_code)
    except Exception as e:
        logging.error("An error occurred: %s", e)

if __name__ == "__main__":
    ssl_scan_results = perform_ssl_scan(TARGET_URL)
    if ssl_scan_results:
        print("SSL Scan Results: ")
        for key, value in ssl_scan_results.items():
            print(f"{key}: {value}")
    else:
        print("SSL scan failed.")
