Contributing
============

We welcome contributions to NotiHub! Whether you're fixing bugs, adding new features, or improving documentation, your help is appreciated.

Development Workflow
--------------------

1.  **Fork the repository** on GitHub
2.  **Create a feature branch** from ``main``
3.  **Make your changes** following the existing code style
4.  **Add tests** for new functionality
5.  **Update documentation** if needed
6.  **Run the test suite** to ensure nothing is broken
7.  **Submit a pull request** with a clear description

Code Style Guidelines
---------------------

*   Follow PEP 8 style guidelines
*   Use type hints for all function parameters and return values
*   Write docstrings for all public classes and methods
*   Keep line length under 90 characters
*   Use dataclasses for configuration objects
*   Implement proper error handling and logging

Adding New Providers
--------------------

When adding a new notification provider:

1.  Follow the step-by-step guide in the "Adding New Notifiers" section
2.  Ensure all abstract methods are implemented
3.  Add comprehensive unit tests
4.  Update this documentation
5.  Add configuration examples to README.md

Testing Requirements
--------------------

*   Minimum 85% test coverage
*   Unit tests for all public methods
*   Integration tests for external service calls (mocked)
*   Error handling tests
*   Edge case testing