# LangGraph Integration with ChatGroq and Custom Tools

This project demonstrates how to integrate the LangGraph library with ChatGroq for building multimodal AI workflows. It includes custom tool creation, memory-saving capabilities, and dynamic routing of tool invocations based on the conversation flow. The primary focus is on creating a chatbot that can intelligently interact with users by leveraging external tools for tasks such as weather information retrieval and search operations.

## Overview

- **LangGraph** is used to define a graph-based workflow that routes messages through different components (agent, tools).
- **ChatGroq** is the language model utilized for generating responses, specifically the "Gemma2-9b-It" model.
- **Custom Tools** are implemented to interact with external APIs (like weather data or search results).
- **MemorySaver** is integrated to preserve the chatbot's memory across different conversations.
- **StateGraph** is used to maintain the state of the conversation and make conditional routing decisions.
- **ToolNode** encapsulates external tools that are invoked as part of the workflow.

## Installation

To use this project, ensure you have the required dependencies:

pip install langgraph langchain_groq langchain_core IPython
