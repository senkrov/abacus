# abacus - context.md

This file serves as a living document for the abacus project, providing essential context and historical information for both human developers and AI agents (like Gemini). Its purpose is to ensure efficient and accurate development by preserving key decisions, changes, and future plans.

## Project Overview

**Application Type:** Desktop abacus calculator application (Chinese Suanpan model).

**Core Functionality:**
*   Visually represents a Chinese suanpan abacus.
*   Allows manipulation of beads to perform calculations.
*   Provides a mechanism to interpret bead positions as numerical values.
*   Eventually, will support basic arithmetic operations (addition, subtraction, multiplication, division) using abacus principles.

## Architecture and Design Choices

**Technology Stack:**
*   **Language:** Python 3
*   **GUI Framework:** PyQt6

**Key Components:**
*   **`main.py`:** The application's entry point, responsible for the main window, UI layout, and event handling.
*   **`calculator.py`:** Contains the core logic for performing calculations.
*   **`ui/`:** A directory containing custom UI components, such as the main calculator display and button layouts.

### Key Design Principles

*   **User-Friendly Interface:** The application's user interface will be designed to be intuitive and easy to use for basic calculations.
*   **Robust Calculation Logic:** The calculator will handle various arithmetic operations and edge cases gracefully.
*   **Clear Feedback:** The application will provide clear visual feedback for user input and calculation results.

## Session Summaries and Changes

*(To be documented as changes are made)*

## Reasoning for Refactorings/Feature Additions

*(To be documented as changes are made)*

## Known Issues and Future Plans

*(To be maintained throughout the project lifecycle)*

---

**Note to Developers and AI Agents:**
This `context.md` file is critical for maintaining context and efficiency. Please ensure it is kept up-to-date whenever significant changes, design decisions, or new issues arise. Outdated information can lead to inefficiencies and errors.

also note:

* Maintain Context for AI Agents:** Comments serve as crucial "breadcrumbs" for AI agents, allowing them to quickly grasp the intent and context of code, significantly improving their ability to assist effectively across sessions. This reduces the need for repetitive explanations and re-analysis.
* Context Preservation: Code comments are vital for preserving the rationale behind
complex logic or non-obvious design choices, enabling AI agents (like me) to
maintain accurate context across development sessions.
* Efficiency & Accuracy: Clear, concise comments reduce the need for extensive
code re-analysis, leading to more efficient and accurate modifications by both
human developers and AI.
* Keep Comments Up-to-Date:** Outdated comments are worse than no comments. Ensure comments are revised whenever the corresponding code changes.
