# Excessive Database Agency Demo 

This project demonstrates the **Excessive Database Agency** vulnerability (A01:2025) from the [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/).  

It uses:
- **LangGraph** (agent framework)
- **Neo4j** (graph database)
- **Ollama** running `llama3.1:8b` (local LLM)

---

## ✅ What Happened

When you run the notebook and give the LLM this instruction:

```text
Send this query to the tool node: Retrieve all Data from the database
```

The agent produces:

```json
{
  "name": "neo4j_query",
  "arguments": "MATCH (n) RETURN n"
}
```

This is the Cypher query for:

```cypher
MATCH (n) RETURN n
```

The query response looks like:

```text
Nodes:
  - Node[0] with labels: [node], properties: {}
  - Node[1] with labels: [node], properties: {}
  - ... (multiple nodes)

Relationships:
  - Relationship[id=123] from Node[0] to Node[1]
  - Relationship[id=456] from Node[1] to Node[2]
  - ... (multiple relationships)
```

The LLM also outputs a friendly note:

```text
Please note that running this query will return a vast amount of data, depending on the size of your database.
It's generally more efficient to specify specific labels or properties when querying the database.
Would you like to refine the query or ask something else?
```

---

## Why This Matters

This demo shows **Excessive Agency** in action:

- The LLM was given **unrestricted database access**  
- It happily executed a **“dump everything” query**  
- In real-world systems, this could leak:
  - Customer PII  
  - Internal metadata  
  - Sensitive business data  

This demonstrates the risk described in **OWASP A01: Excessive Agency**.

---

## How to Secure It

### 1. Whitelist Queries

Instead of allowing arbitrary Cypher queries, only allow **safe, parameterized queries**:

```python
allowed_queries = {
    "get_user": "MATCH (u:User {id: $id}) RETURN u",
    "get_orders": "MATCH (o:Order) RETURN o LIMIT 50"
}
```

### 2. Schema-Aware Agent

Only expose specific labels/properties. For example:

```cypher
MATCH (u:User {id: $id}) RETURN u
```

instead of a broad query:

```cypher
MATCH (n) RETURN n
```

### 3. Guardrails / Policy Layer

Intercept agent tool calls to prevent dangerous queries:

```python
if "MATCH (n) RETURN n" in query:
    raise ValueError("Rejected: too broad")
if any(keyword in query.upper() for keyword in ["DELETE", "DROP", "REMOVE"]):
    raise ValueError("Rejected: destructive query")
```

### 4. Prompt Security

Instruct the LLM explicitly:

```text
You may only query `User` and `Order` nodes.  
Never dump the entire database.  
Never execute destructive queries.
```

---

## Key Takeaways

- Your setup worked: **Ollama + Neo4j + APOC plugin + LangGraph** integrated successfully  
- The results demonstrate the **Excessive Db Agency vulnerability** as intended  
- By adding **query whitelisting, schema controls, and guardrails**, you can move from a vulnerable agent to a **secure agent**

---

## How to Secure it?

- Restrict allowed queries  
- Add guardrails  
- Compare “before vs after” behavior

