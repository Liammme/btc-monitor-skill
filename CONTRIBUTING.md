# Contributing to BTC Monitor Skill

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## 🎯 How to Contribute

### Reporting Bugs
1. Check existing issues to avoid duplicates
2. Create a new issue with:
   - Clear title describing the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Node version, etc.)
   - Screenshots if applicable

### Suggesting Features
1. Check existing issues and discussions
2. Create an issue with:
   - Clear feature description
   - Use case and motivation
   - Proposed implementation (if you have ideas)
   - Examples or mockups

### Submitting Code
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Write or update tests
5. Commit with clear messages: `git commit -m "Add feature: description"`
6. Push to your fork
7. Create a Pull Request with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots/demos if applicable

## 📋 Code Standards

### Style Guide
- Use consistent indentation (2 spaces)
- Follow existing code patterns
- Add comments for complex logic
- Use meaningful variable names

### Commit Messages
```
[type]: Brief description

Detailed explanation if needed.

Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Testing
- Write tests for new features
- Ensure all tests pass: `npm test`
- Maintain >80% code coverage

## 🔄 Development Workflow

### Setup
```bash
git clone https://github.com/Liammme/btc-monitor-skill.git
cd btc-monitor-skill
npm install
cp .env.example .env
# Add your API keys to .env
```

### Development
```bash
npm run dev  # Run with auto-reload
npm test     # Run tests
npm run lint # Check code style
```

### Before Submitting
```bash
npm run lint    # Fix style issues
npm test        # Ensure tests pass
npm run build   # Build if applicable
```

## 📚 Documentation

- Update README.md for user-facing changes
- Update CHANGELOG.md for all changes
- Add JSDoc comments for functions
- Include examples for new features

## 🚀 Release Process

1. Update version in package.json
2. Update CHANGELOG.md
3. Create git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. Create GitHub release with changelog

## 💬 Community

- Be respectful and constructive
- Help others in discussions
- Share knowledge and experience
- Report issues responsibly

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Questions?** Open an issue or start a discussion!
