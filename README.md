# Selenium + Pytest Automation Portfolio

[![CI](https://github.com/YOUR-USERNAME/qa-auto-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR-USERNAME/qa-auto-portfolio/actions/workflows/ci.yml)
[![Allure Report](https://img.shields.io/badge/Allure-Report-blue)](https://YOUR-USERNAME.github.io/qa-auto-portfolio)

A Test automation framework for a blast control system, based on a comprehensive manual test plan. Built with **Selenium**, **Pytest**, and **Allure**, this framework demonstrates best practices in test automation including Page Object Model, data-driven testing, parallel execution, CI/CD integration, and hardware test isolation.

# Features
- **Complete test coverage** of all functional areas: Login, User Management, Network Management, Device Management, Dashboard, Blast Cards, Groups, Email Recipients, Reports, Device Interaction (hardware), and Firmware.
- **Page Object Model** – clean separation of locators and test logic, making tests robust and maintainable.
- **Detailed step-by-step comments** in each test, directly traceable to the manual test plan.
- **Assertions for every success criterion** – clear failure messages.
- **Hardware tests** marked with `@pytest.mark.hardware` and automatically skipped in CI (via `MOCK_HARDWARE=true`).
- **Parallel execution** with `pytest-xdist` for faster feedback.
- **Automatic screenshots** on test failure, attached to Allure reports.
- **Allure reporting** with history deployed to GitHub Pages.
- **Docker support** for consistent local and CI execution.
- **GitHub Actions** CI pipeline with matrix testing, caching, and scheduled runs.

# Project Structure
|--.github/workflows/ci.yml # CI pipelin
|--pages/ # Page Objects
|--tests/ # All test files
|--utils/ # Helpers (logger, screenshot)
|--config.py # Configuration from environment
|--.env.example # Templete for evironment variables
|--requirements.txt
|--Dockerfile
|--docker-compose.yml
|--README.md

## Quick Start

# Local Setup
1. **Clone the repository**
  ```bash
     git clone https://github.com/L-Dub/qa-auto-portfolio.git
     cd qa-auto-portfolio

     # Create and activate a virtual environment(optional)
     python -m venv venv
     source venv/bin/activate # On windows: venv\scripts\activate

     # Install dependancies
     pip install -r requirements.txt
     
     # Edit .env with your application's BASE_URL and Credentials
     cp .env.example .env
     
     # Run All non-hardware test in parallel
     pytest tests/ -m "not hardware" -n auto --alluredir=allure-results --html-report.html

     # Run hardware tests (if you have the actual setup)
     pytest tests/ -m hardware 

     # Docker
     docker-compose up --install

