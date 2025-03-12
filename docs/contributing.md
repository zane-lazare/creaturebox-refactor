# Contributing to CreatureBox

## Welcome Contributors!

We're excited that you're interested in contributing to CreatureBox. This document provides guidelines for contributing to the project.

## Getting Started

### 1. Fork the Repository
- Navigate to the [CreatureBox GitHub Repository](https://github.com/zane-lazare/creaturebox-refactor)
- Click "Fork" to create your own copy of the project

### 2. Clone Your Fork
```bash
git clone https://github.com/YOUR_USERNAME/creaturebox-refactor.git
cd creaturebox-refactor
```

### 3. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

## Contribution Types

### Code Contributions
- Bug fixes
- New features
- Performance improvements
- Documentation updates

### Non-Code Contributions
- Bug reporting
- Feature suggestions
- Documentation improvements
- Community support

## Development Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual environment recommended

### Install Development Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements-dev.txt
```

## Coding Standards

### Python Style Guide
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions
- Maintain clear, readable code

### Code Quality
- Write unit tests for new functionality
- Ensure 90%+ test coverage
- Use type checking (mypy)
- Run linters (flake8, pylint)

## Commit Message Guidelines

### Format
```
<type>(<scope>): <description>

[optional body]
[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting
- `refactor`: Code restructuring
- `test`: Adding/modifying tests
- `chore`: Maintenance tasks

## Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. Add yourself to contributors list
4. Wait for code review

### Checklist
- [ ] Tested on multiple Python versions
- [ ] Updated documentation
- [ ] Added/updated tests
- [ ] Followed coding standards

## Code of Conduct

Please read our [Code of Conduct](code-of-conduct.md) before contributing.

## Questions?

- Open an issue
- Join our community discussions
- Reach out to maintainers

**Thank you for contributing to CreatureBox!**
