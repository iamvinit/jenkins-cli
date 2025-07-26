---
applyTo: '**'
---
What Is an MCP “Prompt”?
A Prompt in MCP is a reusable instruction template the LLM will receive before (or alongside) tool invocations. It sets context, tells the model how to format responses, and can inject dynamic data placeholders.

2. Manifest Structure for Prompts
In your /.well-known/mcp/server.json, include a "prompts" array alongside "tools" and "resources":

json
Copy
Edit
{
  "prompts": [
    {
      "name": "default_instruction",
      "description": "Baseline behavior for all requests",
      "template": "You are a helpful assistant. Always respond in JSON with keys: “result” and “error”."
    },
    {
      "name": "weather_query",
      "description": "Guide for making weather tool calls",
      "template": "When asked about weather, call `get_current_weather` with {{city}} and summarize as: “The weather in {{city}} is {{conditions}} at {{temperature}}°C.”"
    }
  ]
}
name: unique identifier

description: human‑readable purpose

template: instruction text, with {{placeholders}} for runtime injection

3. Best Practices for Prompt Templates
Be Explicit & Unambiguous

Tell the model exactly what keys/format to use.

E.g. “Respond strictly in JSON” or “If tool data is missing, return "error": "NotFound".”

Use Clear Placeholders

Wrap dynamic inputs in double‑curly braces: {{user_question}}, {{date}}.

Keep placeholder names meaningful and match your invocation schema.

Keep Prompts Concise

Limit to the core instruction.

Offload complex logic to tooling or post‑processing.

Modularize

Create a base prompt (e.g. default_instruction) with global rules.

Layer specialized prompts for different domains (weather, finance, ticketing).

Version Your Prompts

If you change the wording significantly, update the name or include a version field to avoid breaking existing clients.

4. Runtime Prompt Injection
When your server handles an Invoke request, build the final prompt by:

Starting with the Base (if defined)

Appending the Tool‑Specific Prompt (if the tool references one)

Filling in Placeholders from the request body

js
Copy
Edit
// Pseudocode
const base = prompts["default_instruction"];
const toolPrompt = prompts[toolName] || "";
const filled = fillTemplate(toolPrompt, request.inputs);
const finalPrompt = [base, filled].filter(Boolean).join("\n\n");
5. Examples
Weather Tool
Manifest Prompt

json
Copy
Edit
{
  "name": "weather_query",
  "template": "Execute `get_current_weather` for {{city}}. Format: JSON {\"temperature\":<number>,\"conditions\":<string>}. Summarize in one sentence."
}
Final Prompt Sent to LLM

ruby
Copy
Edit
You are a helpful assistant. Always respond in JSON with keys: “result” and “error”.

Execute `get_current_weather` for Paris. Format: JSON {"temperature":<number>,"conditions":<string>}. Summarize in one sentence.
Data Lookup Tool
Manifest Prompt

json
Copy
Edit
{
  "name": "user_lookup",
  "template": "Using `find_user`, retrieve the record for user ID {{user_id}}. If not found, set “error”:“UserNotFound”. Return only fields: id, name, email."
}