"""DevOps tool detector."""

import os
from typing import List, Dict
from .base import Detector, DetectionResult


class DevOpsDetector(Detector):
    """Detects DevOps tools and CI/CD configurations."""
    
    # Map files/directories to DevOps tools
    DEVOPS_INDICATORS = {
        "Dockerfile": "Docker",
        "docker-compose.yml": "Docker Compose",
        "docker-compose.yaml": "Docker Compose",
        ".dockerignore": "Docker",
        "Jenkinsfile": "Jenkins",
        ".travis.yml": "Travis CI",
        ".circleci/config.yml": "CircleCI",
        ".gitlab-ci.yml": "GitLab CI",
        "azure-pipelines.yml": "Azure Pipelines",
        "bitbucket-pipelines.yml": "Bitbucket Pipelines",
        ".drone.yml": "Drone CI",
        "appveyor.yml": "AppVeyor",
        "Vagrantfile": "Vagrant",
        "terraform": "Terraform",
        ".terraform": "Terraform",
        "ansible": "Ansible",
        "playbook.yml": "Ansible",
        "kubernetes": "Kubernetes",
        "k8s": "Kubernetes",
        "helm": "Helm",
        "Chart.yaml": "Helm",
        "skaffold.yaml": "Skaffold",
        ".github/workflows": "GitHub Actions",
    }
    
    def detect(self, file_paths: List[str], file_contents: Dict[str, str]) -> List[DetectionResult]:
        """Detect DevOps tools."""
        results = []
        detected = {}
        
        for file_path in file_paths:
            # Check exact filename matches
            basename = os.path.basename(file_path)
            if basename in self.DEVOPS_INDICATORS:
                tool = self.DEVOPS_INDICATORS[basename]
                if tool not in detected:
                    detected[tool] = []
                detected[tool].append(file_path)
            
            # Check path contains patterns
            for pattern, tool in self.DEVOPS_INDICATORS.items():
                if pattern in file_path and tool not in detected:
                    detected[tool] = [file_path]
        
        # Special handling for GitHub Actions
        github_actions_files = [f for f in file_paths if ".github/workflows" in f and f.endswith((".yml", ".yaml"))]
        if github_actions_files:
            detected["GitHub Actions"] = github_actions_files
        
        # Special handling for Kubernetes
        k8s_files = [f for f in file_paths if any(kw in f for kw in ["k8s", "kubernetes"]) and f.endswith((".yml", ".yaml"))]
        if k8s_files and "Kubernetes" not in detected:
            detected["Kubernetes"] = k8s_files
        
        # Create results
        for tool, files in detected.items():
            results.append(DetectionResult(
                category="devops",
                name=tool,
                confidence="high",
                source_files=files[:3],  # Limit to 3 example files
                metadata={"file_count": len(files)}
            ))
        
        return results
