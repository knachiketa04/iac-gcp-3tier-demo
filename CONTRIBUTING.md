# Contributing to Terraform GCP 3-Tier Application

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code follows the existing style.
6. Issue that pull request!

## Code Style

### Terraform Code Style

- Use consistent indentation (2 spaces)
- Follow [Terraform style conventions](https://www.terraform.io/docs/language/style.html)
- Use meaningful variable and resource names
- Include comments for complex logic
- Run `terraform fmt` before committing

### Documentation Style

- Use clear, concise language
- Include examples where helpful
- Update README.md when adding new features
- Use emoji for visual organization (but don't overdo it)

## Testing Guidelines

Before submitting a pull request:

1. **Terraform Validation**: Run `terraform validate`
2. **Format Check**: Run `terraform fmt -check`
3. **Plan Test**: Run `terraform plan` with example values
4. **Documentation**: Ensure all changes are documented

## Reporting Bugs

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](../../issues/new).

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Feature Requests

We also use GitHub issues to track feature requests. When requesting a feature:

- Explain the use case and why this would be valuable
- Include examples if possible
- Consider if this fits the project's scope

## Project Structure

When contributing, please maintain the existing project structure:

```
├── README.md                   # Main documentation
├── docs/                       # Additional documentation
├── infrastructure/             # Terraform files (if reorganized)
├── application/               # Application code
├── scripts/                   # Deployment scripts
└── terraform.tfvars.example   # Example configuration
```

## Security

- Never commit sensitive information (API keys, passwords, etc.)
- Use `terraform.tfvars.example` for examples, not real values
- Follow the principle of least privilege for IAM roles
- Report security vulnerabilities privately (see SECURITY.md if available)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue if you have questions about contributing!
