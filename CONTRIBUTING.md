# Contributing to InfoStore

First off, thank you for considering contributing to InfoStore! It's people like you that make InfoStore such a great tool.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [your.email@example.com].

### Our Standards

**Examples of behavior that contributes to a positive environment:**

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Examples of unacceptable behavior:**

- The use of sexualized language or imagery
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Git
- Virtual environment tool
- Basic understanding of Django and Django REST Framework

### Development Setup

1. **Fork the repository** on GitHub

2. **Clone your fork** locally:

```bash
git clone https://github.com/your-username/infostore-api.git
cd infostore
```

3. **Create a virtual environment**:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. **Install dependencies**:

```bash
pip install -r requirements.txt
```

5. **Set up environment variables**:

```bash
cp .env.example .env
# Edit .env with your settings
```

6. **Run migrations**:

```bash
python manage.py migrate
```

7. **Create a superuser**:

```bash
python manage.py createsuperuser
```

8. **Run the development server**:

```bash
python manage.py runserver
```

9. **Create a branch** for your changes:

```bash
git checkout -b feature/your-feature-name
```

## 💡 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates.

When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if possible**
- **Include your environment details** (OS, Python version, Django version)

**Bug Report Template:**

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. Windows 10, Ubuntu 22.04]
- Python Version: [e.g. 3.13.5]
- Django Version: [e.g. 4.2]

**Additional context**
Any other relevant information.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the proposed enhancement**
- **Explain why this enhancement would be useful**
- **List any similar features in other projects**

### Pull Requests

1. **Follow the style guidelines** below
2. **Update documentation** as needed
3. **Add tests** for new features
4. **Ensure all tests pass**
5. **Update the README.md** if needed

## 🎨 Style Guidelines

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some exceptions:

- **Line length**: Maximum 120 characters
- **Imports**: Group imports in this order:
  1. Standard library imports
  2. Related third-party imports
  3. Local application imports
- **Use meaningful variable names**
- **Add docstrings** to all functions, classes, and modules

**Example:**

```python
from django.db import models
from django.conf import settings

from rest_framework import serializers

from .models import Product


def calculate_discount(price, discount_percentage):
    """
    Calculate the discounted price.
    
    Args:
        price (Decimal): Original price
        discount_percentage (int): Discount percentage (0-100)
    
    Returns:
        Decimal: Discounted price
    """
    return price * (1 - discount_percentage / 100)
```

### Django Best Practices

- Use Django's built-in features when possible
- Follow the "fat models, thin views" principle
- Use Django's class-based views appropriately
- Properly handle exceptions
- Use Django's translation framework for user-facing strings
- Write database-agnostic code

### API Design Guidelines

- Use RESTful conventions
- Use appropriate HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Return appropriate status codes
- Provide meaningful error messages
- Use pagination for list endpoints
- Version your API when making breaking changes

## 📝 Commit Messages

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (formatting, etc.)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvements
- **test**: Adding or correcting tests
- **chore**: Changes to build process or auxiliary tools

### Examples

```
feat(auth): add password reset functionality

Implemented password reset via email with token validation.
Users can now request a password reset link.

Closes #123
```

```
fix(cart): correct total calculation for multiple items

Fixed a bug where cart total was incorrectly calculated when
users had multiple items with different quantities.

Fixes #456
```

## 🔄 Pull Request Process

1. **Update the README.md** with details of changes if needed
2. **Update documentation** for any new features
3. **Add tests** for new functionality
4. **Ensure all tests pass**: `python manage.py test`
5. **Update CHANGELOG.md** following the existing format
6. **Request review** from maintainers
7. **Address review comments** promptly

### PR Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests you ran and how to reproduce them.

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where needed
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing unit tests pass locally
- [ ] Any dependent changes have been merged

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Related Issues
Closes #(issue number)
```

## 🧪 Testing

Before submitting your pull request:

1. **Run all tests**:

```bash
python manage.py test
```

2. **Check code coverage** (if applicable):

```bash
coverage run --source='.' manage.py test
coverage report
```

3. **Run linting**:

```bash
flake8 .
```

## 📞 Getting Help

If you need help:

- Check the [documentation](README.md)
- Open an issue with the `question` label
- Join our [community chat] (if available)
- Email the maintainers

## 🎯 Good First Issues

Look for issues labeled `good first issue` - these are great for newcomers!

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Git Workflow](https://guides.github.com/introduction/flow/)
- [Writing Good Commit Messages](https://chris.beams.io/posts/git-commit/)
- [PEP 8 Style Guide](https://pep8.org/)

## 🏆 Recognition

Contributors will be recognized in our README.md and release notes.

---

Thank you for contributing to InfoStore! 🎉
