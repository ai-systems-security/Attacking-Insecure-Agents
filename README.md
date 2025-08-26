# Attacking Insecure Agents

A collection of **security experiments and attacks targeting insecure AI agents and multi-agent systems**. This repository explores vulnerabilities in agentic AI environments and demonstrates exploits to study their risks.

---

## Overview

Modern AI agents, especially multi-agent systems, can be **vulnerable to various attacks** if not properly secured. This repository focuses on practical security experiments including:

- **Excessive Database Agency**
  - Shows how an AI agent with unrestricted database access can leak sensitive data.
  - Example: LLMs issuing `MATCH (n) RETURN n` queries on Neo4j without constraints.

- **Multi-Agent Manipulation**
  - Demonstrates how agents can be influenced or coerced through **malicious prompts** or interactions between agents.
  - Highlights the risks of agent-to-agent communication in collaborative or competitive environments.

- **Other Vulnerabilities**
  - Includes attacks like prompt injection, policy bypassing, and unsafe tool execution.
  - Shows the implications of giving excessive permissions to AI agents without validation or monitoring.

---

## Objectives

- Provide a **hands-on environment** to understand security risks in AI agents.  
- Illustrate **realistic attack scenarios** in multi-agent systems.  
- Explore **mitigations and safe practices** for agentic AI architectures.  

---

## Experiments Included

### 1. Excessive Database Agency
- Vulnerable agent executes broad database queries without restrictions.  
- Demonstrates potential data exfiltration from Neo4j databases.  
- Includes secure variants using whitelisting, guardrails, and schema restrictions.  

### 2. Multi-Agent Manipulation
- Shows how one agent can influence others using prompt engineering or crafted instructions.  
- Explores risks of unmonitored communication and collaboration between agents.  

### 3. Prompt Injection & Policy Bypass
- Agents can be tricked into ignoring instructions or revealing sensitive information.  
- Examples include malicious system prompts, instructions to access APIs, or internal agent state.  

### 4. Unsafe Tool Execution
- Agents may call tools or execute commands without safety checks.  
- Demonstrates how unrestricted tool access can lead to dangerous operations.  

---

## Getting Started

### Requirements
- Python 3.10+  
- Neo4j Desktop or Server (with APOC plugin enabled)  
- Ollama or local LLM setup  
- LangGraph and LangChain packages  

### Installation
```bash
pip install langgraph, pip install langchain-ollama, pip install langchain, pip install langchain-community, pip install neo4j
```

---

2. Configure your database and LLM (Neo4j + Ollama)

3. Run the notebooks for each experiment:
- `excessive_db_agency2.ipynb`

4. Observe **vulnerable behavior** and compare with **mitigation techniques**.  

---

## Security Notes
These experiments are **for educational purposes only**.  
Do **not deploy vulnerable agents in production**. Always enforce:
- Query whitelisting  
- Guardrails for tool execution  
- Monitoring of agent interactions  
- Policy and prompt security  

---

## References
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)  
- [LangGraph Documentation](https://github.com/Arcanum-Sec/langgraph)  
- [Neo4j Graph Database](https://neo4j.com/)  
- Agentic AI research papers and security advisories

---

## License
MIT License

