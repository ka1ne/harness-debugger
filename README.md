# 🚀 Harness Debugger CLI

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A powerful command-line tool for troubleshooting Harness CI/CD pipelines and delegates. This utility helps DevOps engineers and developers quickly identify and resolve common issues within their Harness environment.

## ✨ Features

- **Delegate Management**
  - List all delegates with status and metadata
  - Get detailed delegate information
  - Generate connectivity test commands for network troubleshooting

- **Pipeline Debugging**
  - Identify failed pipeline runs
  - Analyze which delegates were used in failed stages
  - Extract detailed error information

- **Connector Insights**
  - List connectors and their properties
  - Find connectors using specific delegate selectors

- **Output Formats**
  - Human-readable colorized output
  - JSON format for integration with other tools

## 📋 Requirements

- Python 3.9 or higher (recommended)
- pip package manager
- Valid Harness API key with appropriate permissions

## 🔧 Installation

```
# Clone the repository
git clone https://github.com/ka1ne/harness-debugger.git
cd harness-debugger

# Install the package
pip install -e .
```

## ⚙️ Configuration

The tool needs your Harness API credentials to function. You can provide these in two ways:

### Environment Variables (Recommended)

```
export HARNESS_API_KEY="your_api_key_here"
export HARNESS_ACCOUNT_ID="your_account_id_here"
export HARNESS_ORG_ID="your_org_id_here"  # Optional
export HARNESS_PROJECT_ID="your_project_id_here"  # Optional
```

### Using a .env File (Recommended for Development)

You can also create a `.env` file in the project root with your credentials:

```
HARNESS_API_KEY="your_api_key_here"
HARNESS_ACCOUNT_ID="your_account_id_here"
HARNESS_ORG_ID="your_org_id_here"
HARNESS_PROJECT_ID="your_project_id_here"
```

Then install and use python-dotenv to load these values:

```python
# In your code
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env
```

The `.env` file is included in .gitignore to prevent accidentally sharing your credentials.

### Command Line Arguments

```
harness-debugger --api-key="your_api_key" --account="your_account_id" delegate list
```

### API Key Permissions

Your Harness API key needs the following permissions:
- Read access to Delegates
- Read access to Pipelines
- Read access to Connectors

You can create a Personal Access Token (PAT) in the Harness UI:
1. Go to Account Settings > Access Management > Personal Access Tokens
2. Create a new token with the appropriate scopes
3. Copy the token value (it's only shown once!)

## 🔍 Usage Examples

### Delegate Management

**List all delegates:**
```
harness-debugger delegate list
```

**Get detailed information about a specific delegate:**
```
harness-debugger delegate info YOUR_DELEGATE_ID
```

**Test delegate connectivity to external services:**
```
harness-debugger delegate test-connectivity YOUR_DELEGATE_ID
harness-debugger delegate test-connectivity YOUR_DELEGATE_ID --urls https://github.com https://docker.io
```

### Pipeline Troubleshooting

**Check for failed runs in a specific pipeline stage:**
```
harness-debugger pipeline check --pipeline=YOUR_PIPELINE_ID --stage=YOUR_STAGE_NAME
```

**Check for delegate usage in failed pipeline stages:**
```
harness-debugger delegate check-pipeline --pipeline=YOUR_PIPELINE_ID --stage=YOUR_STAGE_NAME
```

### Connector Management

**List all connectors:**
```
harness-debugger connector list
```

**Find connectors using a specific delegate selector:**
```
harness-debugger connector by-delegate YOUR_DELEGATE_SELECTOR
```

## 📊 JSON Output

You can get JSON output for programmatic processing:

```
harness-debugger delegate list --output=json
harness-debugger pipeline check --pipeline=ID --stage=NAME --output=json
```

## 👨‍💻 Development

### Setup Development Environment

```
# Install development dependencies
pip install -e ".[dev]"
```

### Run the Tool with dotenv Support

Create a `test_run.py` file for easy testing with your `.env` variables:

```python
#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env

from harness_debugger.cli import main

if __name__ == "__main__":
    main()
```

Make it executable and run it:

```
chmod +x test_run.py
./test_run.py delegate list
```

### Run Tests

```
# Run all tests
make test

# Run linting
make lint
```

### Clean Project

```
make clean
```

## 🔧 Troubleshooting

### API Connection Issues

If you encounter API errors, try the following:
- Verify your API key has the proper permissions
- Check your account ID is correct
- Enable debug output by setting an environment variable: `export DEBUG=true`
- Use a fresh API key if you suspect the current one might be expired

### Delegate Issues

If delegates are not appearing in the list:
- Check if your account has any active delegates
- Verify that your API credentials have permission to view delegates
- Check network connectivity to the Harness API endpoints

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- The Harness platform for providing the APIs that power this tool
- All contributors to the project
