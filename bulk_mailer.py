#!/usr/bin/env python3
import os
import sys
import smtplib
import mimetypes
from email.message import EmailMessage

export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="465"
export SMTP_USE_SSL="1"
export SMTP_USER="niranprempanakal@gmail.com"
export SMTP_PASS="kqlp ibua ckrf dipj"


FROM_NAME = "Niran Prem"
FROM_EMAIL = SMTP_USER
SUBJECT = "Application for DevOps Engineer - Niran Prem _immediate joiner"

BODY = """Hello Hiring Manager,

I am excited to apply for the DevOps Engineer position. With above 4 years of hands-on experience across AWS, Azure, and GCP, I specialize in building and automating scalable infrastructure, managing Kubernetes clusters (EKS, AKS, GKE), and driving automation-first initiatives using Terraform, Docker, and CI/CD pipelines.

Key highlights of my expertise:
- Built and maintained enterprise CI/CD pipelines with AWS , Azure Devops, Jenkins, and GitHub Actions, reducing release cycle time by 45%.
- Automated cloud infrastructure provisioning with Terraform and Ansible, ensuring consistency across 30+ production environments.
- Managed Kubernetes clusters for microservices deployments with zero downtime rollouts.
- Implemented GitOps workflows and monitoring solutions (CloudWatch, Grafana, Zabbix) to improve system reliability.
- Strong experience in Linux administration, virtualization (VMware), and security hardening.

I am confident my skills in DevOps practices, automation, and cloud-native technologies will add value to your team. Please find my resume attached for your review. I am available to join immediately and would welcome the opportunity to discuss how I can contribute.

Best regards,
Niran Prem
📞 9895165491
✉️ niranprempanakal@gmail.com
🔗 LinkedIn: https://linkedin.com/in/niran-prem-b8b420232
"""

# ---------------- FUNCTIONS ----------------
def attach_file(msg: EmailMessage, filepath: str):
    if not os.path.isfile(filepath):
        print(f"Attachment not found: {filepath}")
        sys.exit(2)
    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)
    with open(filepath, "rb") as f:
        data = f.read()
    msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=os.path.basename(filepath))

def send_mail(to_email, resume_path, smtp):
    msg = EmailMessage()
    msg["Subject"] = SUBJECT
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = to_email
    msg.set_content(BODY)
    attach_file(msg, resume_path)
    smtp.send_message(msg)

# ---------------- MAIN SCRIPT ----------------
def main():
    if len(sys.argv) < 3:
        print("Usage: ./bulk_mailer.py recipients.txt resume.pdf")
        sys.exit(1)

    recipients_file = sys.argv[1]
    resume_path = sys.argv[2]

    if not SMTP_USER or not SMTP_PASS:
        print("Please set SMTP_USER and SMTP_PASS environment variables.")
        sys.exit(1)

    # Read recipients
    with open(recipients_file, "r") as f:
        recipients = [line.strip() for line in f if line.strip()]

    if not recipients:
        print("No recipients found in file.")
        sys.exit(1)

    print(f"Loaded {len(recipients)} recipients from {recipients_file}")
    print("Starting email sending...\n")

    success = []
    failed = []

    # Connect to SMTP server
    try:
        if USE_SSL:
            smtp = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        else:
            smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            smtp.starttls()

        smtp.login(SMTP_USER, SMTP_PASS)
    except Exception as e:
        print(f"SMTP connection failed: {e}")
        sys.exit(1)

    for i, email in enumerate(recipients, start=1):
        try:
            send_mail(email, resume_path, smtp)
            print(f"[{i}/{len(recipients)}] ✅ Sent to {email}")
            success.append(email)
        except Exception as e:
            print(f"[{i}/{len(recipients)}] ❌ Failed to {email} -> {e}")
            failed.append(email)

    smtp.quit()

    # Summary
    print("\n--- SUMMARY ---")
    print(f"✅ Sent successfully: {len(success)}")
    print(f"❌ Failed: {len(failed)}")
    if failed:
        print("Failed recipients:")
        for f in failed:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
