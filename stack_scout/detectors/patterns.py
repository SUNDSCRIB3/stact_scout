"""Pattern definitions for technology detection."""

# Language patterns
LANGUAGE_PATTERNS = {
    'Python': ['.py'],
    'TypeScript': ['.ts', '.tsx'],
    'JavaScript': ['.js', '.jsx'],
    'Go': ['.go'],
    'Java': ['.java'],
    'Rust': ['.rs'],
    'Ruby': ['.rb'],
    'PHP': ['.php'],
    'C++': ['.cpp', '.cc', '.cxx', '.hpp'],
    'C': ['.c', '.h'],
    'C#': ['.cs'],
    'Swift': ['.swift'],
    'Kotlin': ['.kt', '.kts'],
    'Scala': ['.scala'],
    'Shell': ['.sh', '.bash'],
}

# Framework detection patterns
FRAMEWORK_PATTERNS = {
    'React': {
        'package_json': ['react'],
        'files': ['*.jsx', '*.tsx'],
    },
    'Vue': {
        'package_json': ['vue'],
        'files': ['*.vue'],
    },
    'Angular': {
        'package_json': ['@angular/core'],
    },
    'Next.js': {
        'package_json': ['next'],
    },
    'Svelte': {
        'package_json': ['svelte'],
    },
    'Express': {
        'package_json': ['express'],
    },
    'Django': {
        'python_deps': ['django', 'Django'],
        'files': ['manage.py'],
    },
    'Flask': {
        'python_deps': ['flask', 'Flask'],
    },
    'FastAPI': {
        'python_deps': ['fastapi'],
    },
    'Streamlit': {
        'python_deps': ['streamlit'],
    },
    'Spring Boot': {
        'maven': ['spring-boot'],
        'gradle': ['spring-boot'],
    },
    'Rails': {
        'gemfile': ['rails'],
    },
    'Laravel': {
        'composer': ['laravel/framework'],
    },
}

# Build tools patterns
BUILD_TOOL_PATTERNS = {
    'npm': ['package-lock.json'],
    'Yarn': ['yarn.lock'],
    'pnpm': ['pnpm-lock.yaml'],
    'Vite': ['vite.config.js', 'vite.config.ts', 'vite.config.mjs'],
    'Webpack': ['webpack.config.js', 'webpack.config.ts'],
    'Rollup': ['rollup.config.js', 'rollup.config.mjs'],
    'ESLint': ['.eslintrc', '.eslintrc.js', '.eslintrc.json', '.eslintrc.yml', '.eslintrc.yaml'],
    'Prettier': ['.prettierrc', '.prettierrc.js', '.prettierrc.json', '.prettierrc.yml', '.prettierrc.yaml'],
    'TypeScript': ['tsconfig.json'],
    'pip': ['requirements.txt'],
    'Poetry': ['pyproject.toml'],  # Check for [tool.poetry] inside
    'Pipenv': ['Pipfile'],
    'Maven': ['pom.xml'],
    'Gradle': ['build.gradle', 'build.gradle.kts', 'settings.gradle', 'settings.gradle.kts'],
    'Go Modules': ['go.mod', 'go.sum'],
    'Cargo': ['Cargo.toml'],
    'Bundler': ['Gemfile', 'Gemfile.lock'],
    'Composer': ['composer.json', 'composer.lock'],
}

# DevOps patterns
DEVOPS_PATTERNS = {
    'Docker': ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml', '.dockerignore'],
    'Kubernetes': ['k8s/', 'kubernetes/'],  # Also check for kind: Deployment in yamls
    'GitHub Actions': ['.github/workflows/'],
    'GitLab CI': ['.gitlab-ci.yml'],
    'Jenkins': ['Jenkinsfile'],
    'CircleCI': ['.circleci/config.yml'],
    'Travis CI': ['.travis.yml'],
    'Terraform': ['*.tf', '.terraform/'],
    'Ansible': ['playbook.yml', 'ansible.cfg'],
    'CloudFormation': ['*.template.json'],
    'Pre-commit': ['.pre-commit-config.yaml', '.pre-commit-config.yml'],
    'Make': ['Makefile', 'makefile'],
}
