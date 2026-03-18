# organAIzer Project Constitution

## 1. Project Vision
The **organAIzer** project aims to build a personal AI agent designed to help users get organized.

## 2. Core Architectural Principles
The project strictly follows **Clean Architecture** principles to ensure a modular, testable, and maintainable codebase.

### 2.1 Layered Architecture
The application is organized into the following layers:
- **Domain**: Contains the core business concepts, entities, and logic. This layer is independent of any external frameworks.
- **Use Cases**: Contains the business problem-solving logic, orchestrating the flow of data to and from the domain entities.
- **Agent**: All logic related to AI agents, including LangGraph, LangChain, and DeepAgent code.
- **Controller**: Entry points for external interaction, such as FastAPI endpoints, Agent-to-Agent (A2A), Agent-to-Client (A2C), and Model Context Protocol (MCP) implementations.
- **Infrastructure**: Concrete implementations of external concerns, such as database access, API clients, and other technical details.

### 2.2 Dependency Management
- **Dependency Injection**: We use the `dependency-injector` library to manage DI across the project, ensuring that high-level modules do not depend on low-level modules.
- **Typing**: Python's type hinting is MANDATORY. All code MUST be properly typed and maintained to ensure code quality and facilitate static analysis.

## 3. Tooling and Development Workflow
The project uses **uv** for environment management, dependency handling, and execution.

### 3.1 Common `uv` Commands
- **Run the project**: `uv run main.py serve`
- **Add a dependency**: `uv add <package_name>`
- **Remove a dependency**: `uv remove <package_name>`
- **Update dependencies**: `uv lock --upgrade`
- **Run tests**: `uv run pytest`

### 3.2 Code Quality Tools
- **Ruff**: Used for linting, formatting, and (where possible) type checking.
- **Tools Utility Folder**: A `tools/` directory contains bash scripts for automated tasks:
  - Linting and formatting.
  - Running all test suites.
  - Starting the server and sending test queries.

## 4. Testing Strategy
We use **pytest** and **behave** to ensure high-quality software.

- **Unit and Integration Testing**: Managed with `pytest`.
- **Mocking**: Use `pytest-mock`. **Always use fixtures** for mocking; avoid the `@patch` decorator to maintain clean and readable test code.
- **Behavior-Driven Development (BDD)**: Managed with `behave` to ensure the software meets user requirements.

## 5. Application Entry Point
The application entry point is a **click CLI** implemented in `main.py`.
- Current primary command: `serve` (starts the application server).
