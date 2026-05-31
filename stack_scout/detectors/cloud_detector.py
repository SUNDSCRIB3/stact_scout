"""Cloud provider detection module."""

from typing import List, Dict
from .base import Detector, DetectionResult


class CloudDetector(Detector):
    """Detects cloud providers from configuration and dependency files."""

    AWS_PATTERNS = [
        "boto3", "botocore", "aws-sdk", "aws-sdk-go", "aws/", "amazonaws",
        "aws_lambda", "aws_", "terraform-provider-aws",
    ]
    GCP_PATTERNS = [
        "google-cloud", "google-cloud-", "gcloud", "gcp-", "@google-cloud",
        "googleapis", "terraform-provider-google",
    ]
    AZURE_PATTERNS = [
        "azure-", "azure_", "azurerm", "@azure/", "azure-sdk",
        "terraform-provider-azurerm",
    ]
    DIGITALOCEAN_PATTERNS = [
        "digitalocean", "doctl",
    ]

    FILE_INDICATORS = {
        "serverless.yml": "AWS",
        "serverless.yaml": "AWS",
        "app.yaml": "GCP",
        "cloudbuild.yaml": "GCP",
        ".azure/": "Azure",
        "deploy/azure": "Azure",
    }

    def detect(self, file_paths: List[str], file_contents: Dict[str, str]) -> List[DetectionResult]:
        results = []
        detected = {}
        all_content = " ".join(file_contents.values()).lower()

        for path in file_paths:
            lower = path.lower()
            if ".aws/" in lower or "aws/" in lower:
                if "AWS" not in detected:
                    detected["AWS"] = {"sources": [], "confidence": "high"}
                detected["AWS"]["sources"].append(path)

            if any(term in lower for term in ["gcp/", "gcloud/", "google-cloud/"]):
                if "GCP" not in detected:
                    detected["GCP"] = {"sources": [], "confidence": "high"}
                detected["GCP"]["sources"].append(path)

        # Check file contents for cloud provider SDKs
        for provider_name, patterns, content_str in [
            ("AWS", self.AWS_PATTERNS, all_content),
            ("GCP", self.GCP_PATTERNS, all_content),
            ("Azure", self.AZURE_PATTERNS, all_content),
            ("DigitalOcean", self.DIGITALOCEAN_PATTERNS, all_content),
        ]:
            for pattern in patterns:
                if pattern.lower() in content_str:
                    if provider_name not in detected:
                        detected[provider_name] = {"sources": [], "confidence": "medium"}
                    detected[provider_name]["sources"].append("dependency file")

        # Check for Terraform provider files
        for path, content in file_contents.items():
            if path.endswith(".tf") or path.endswith(".tf.json"):
                content_lower = content.lower()
                if "aws" in content_lower and "AWS" not in detected:
                    detected["AWS"] = {"sources": [path], "confidence": "high"}
                if "google" in content_lower and "GCP" not in detected:
                    detected["GCP"] = {"sources": [path], "confidence": "high"}
                if "azurerm" in content_lower and "Azure" not in detected:
                    detected["Azure"] = {"sources": [path], "confidence": "high"}

        for provider_name, info in detected.items():
            results.append(DetectionResult(
                category="cloud",
                name=provider_name,
                confidence=info["confidence"],
                source_files=list(set(info["sources"]))[:5],
            ))

        return results
