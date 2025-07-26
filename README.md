# Jenkins CLI Tool (jnks)

[![Release](https://github.com/iamvinit/jenkins-cli/actions/workflows/release.yml/badge.svg)](https://github.com/iamvinit/jenkins-cli/actions/workflows/release.yml)

A command-line interface for managing Jenkins jobs with MCP (Model Context Protocol) server support for AI assistants. Simple, fast, and easy to use.

## Features

- **CLI Tool**: Traditional command-line interface for Jenkins operations
- **MCP Server**: Expose Jenkins functionality to AI assistants and language models
- **Auto-Configuration**: Environment variable-based setup for seamless integration
- **Real-time Streaming**: Watch build console output in real-time
- **Parameter Management**: Smart handling of Jenkins job parameters

## Installation

```bash
pip install jnks-cli
```

This installs the `jnks` CLI tool with integrated MCP server support.

## Quick Start

1. Configure Jenkins connection:
```bash
$ jnks config
Jenkins server host (e.g., https://jenkins.example.com): https://jenkins.company.com
Jenkins API token: your-api-token
Jenkins username: your-username
Testing connection...
Connection successful! Configuration saved to ~/.jenkins/config.yaml
```

2. Initialize a job (in your project directory):
```bash
$ jnks init
Initialized job configuration in .jenkins.yaml
Found 3 parameters:
  BRANCH: $BRANCH
  ENV: staging
  DEBUG: true
```

## MCP Server (Model Context Protocol)

This package includes an MCP server that exposes Jenkins operations to AI assistants like **Cursor**, **VS Code Copilot**, and other MCP-compatible tools.

### Multi-Project Support & Project Context

**Always pass the current working directory (CWD) as the `cwd` parameter to every MCP tool call.**

- The CWD should be set to your project root (use the output of `pwd`).
- This enables seamless multi-project usage and ensures Jenkins operations are performed in the correct context.
- Most AI tools (Cursor, Copilot, etc.) allow you to set the `cwd` in their MCP server configuration. See examples below.

**Do not call MCP tools without specifying the correct CWD/project context.**

### Setup for AI Tools (with CWD)

1. **Configure Jenkins credentials** via environment variables:
```bash
export JENKINS_HOST=https://jenkins.company.com
export JENKINS_USER=your-username
export JENKINS_TOKEN=your-api-token
```

2. **Configure your AI tool** to use the MCP server:

#### For Cursor
Add to your Cursor settings:
```json
{
  "mcp": {
    "servers": {
      "jenkins": {
        "command": "jnks",
        "args": ["mcp"],
    "cwd": "/path/to/your/project"  // Always set to your project root (output of `pwd`)
      }
    }
  }
}
```

#### For VS Code Copilot
Add to your VS Code workspace settings:
```json
{
  "mcp.servers": [
    {
      "name": "jenkins",
      "command": "jnks",
      "args": ["mcp"],
    "cwd": "${workspaceFolder}"  // VS Code will substitute this with your project root
    }
  ]
}
```


3. **Start using Jenkins in your AI conversations** (the AI assistant will automatically use the correct MCP tools):
   - "Initialize Jenkins for this project"
   - "Build the main branch with ENV=staging"
   - "Show me the latest build status"
   - "Get console output from build #123"

**Important:**
- The MCP server requires the current working directory (`cwd`) for every request. This is how it supports multiple projects and ensures the correct `.jenkins.yaml` is used.
- You do **not** need to specify individual MCP tool names or parameters manually—just ensure your AI tool passes the correct `cwd`.

#### Manual Configuration
If environment variables are not set, the server will prompt for configuration on first start.

### Integration Examples

#### With Claude Desktop
Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "jenkins": {
      "command": "jnks",
      "args": ["mcp"],
      "env": {
        "JENKINS_HOST": "https://jenkins.company.com",
        "JENKINS_USER": "your-username",
        "JENKINS_TOKEN": "your-api-token"
      }
    }
  }
}
```

#### With Other MCP Clients
The server follows standard MCP protocol and can be used with any MCP-compatible client. Always ensure the `cwd` parameter is set to your project root (output of `pwd`).

## Commands

### Build (`build`)
Trigger a Jenkins job build.

```bash
# Basic build with parameters
$ jnks build BRANCH=main ENV=prod
Build #123 started

# Watch console output
$ jnks build --watch BRANCH=main
Build #124 started
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /workspace/my-job
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Checkout)
[Pipeline] checkout
...

# With debug logging
$ jnks build --debug BRANCH=main
2024-02-22 17:27:24 - DEBUG - Connecting to Jenkins server at https://jenkins.company.com
2024-02-22 17:27:24 - DEBUG - Build parameters: {"BRANCH": "main", "ENV": "staging"}
Build #125 started
```

Parameters in `.jenkins.yaml` marked with `$` are required:
```yaml
name: my-job
parameters:
  BRANCH: $BRANCH     # Required
  ENV: staging        # Optional with default
  DEBUG: true        # Optional with default
```

### Console Output (`console`)
View build console output.

```bash
# View latest build
$ jnks console
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /workspace/my-job
...

# View specific build with watch
$ jnks console --watch --build 123
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /workspace/my-job
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Build)
...
```

### Status (`status`)
View recent builds status.

```bash
$ jnks status
┌───────┬───────────────┬────────────┬─────────────────────┬──────────┐
│ Build │ Name          │ Status     │ Started             │ Duration │
├───────┼───────────────┼────────────┼─────────────────────┼──────────┤
│ 125   │ my-job        │ SUCCESS    │ 2024-02-22 17:27:24 │ 45.2s    │
│ 124   │ my-job        │ FAILURE    │ 2024-02-22 17:25:10 │ 32.8s    │
│ 123   │ my-job        │ SUCCESS    │ 2024-02-22 17:20:05 │ 38.5s    │
│ 122   │ my-job        │ SUCCESS    │ 2024-02-22 17:15:30 │ 41.1s    │
│ 121   │ my-job        │ ABORTED    │ 2024-02-22 17:10:15 │ 12.3s    │
└───────┴───────────────┴────────────┴─────────────────────┴──────────┘
```

### Open in Browser (`open`)
Open Jenkins job or build in your default browser.

```bash
# Open job page
$ jnks open
Opening https://jenkins.company.com/job/my-job in browser

# Open specific build
$ jnks open --build 123
Opening https://jenkins.company.com/job/my-job/123 in browser
```

## Global Options

- `--debug`: Enable debug logging (available for all commands)

Example debug output:
```bash
$ jnks status --debug
2024-02-22 17:27:24 - DEBUG - Connecting to Jenkins server at https://jenkins.company.com
2024-02-22 17:27:24 - DEBUG - SSL verification warnings disabled for HTTPS connection
2024-02-22 17:27:25 - DEBUG - Getting status for job my-job
2024-02-22 17:27:25 - DEBUG - Retrieved info for build #125
...
```

## Configuration

The tool stores configuration in two locations:
- Global: `~/.jenkins/config.yaml` (Jenkins connection details)
```yaml
host: https://jenkins.company.com
token: your-api-token
user: your-username
```

- Local: `.jenkins.yaml` (Job-specific settings)
```yaml
name: my-job
parameters:
  BRANCH: $BRANCH
  ENV: staging
  DEBUG: true
```

## Error Handling

Common error messages and solutions:

1. "Jenkins job not initialized":
   ```bash
   $ jnks build
   Jenkins job not initialized. Run 'jnks init' first.
   
   $ jnks init
   Initialized job configuration in .jenkins.yaml
   ```

2. "Multiple builds are running":
   ```bash
   $ jnks console
   Multiple builds are running. Please select a build number:
   Build #125
   Build #124
   
   $ jnks console --build 125
   [Pipeline] Start of Pipeline...
   ```

3. "No parameters provided":
   ```bash
   $ jnks build
   Error: No parameters provided. Required parameters:
     BRANCH: $BRANCH
   
   Example usage:
     jnks build BRANCH=main
   ```

## Quick Reference

### CLI Commands
```bash
jnks config                    # Configure Jenkins connection
jnks init                      # Initialize job in current directory
jnks build BRANCH=main         # Build with parameters
jnks status                    # Show recent build status
jnks console                   # View console output
jnks open                      # Open in browser
```

### MCP Server
```bash
jnks mcp                       # Start MCP server (AI tools will connect and pass CWD automatically)
```

### Environment Variables
```bash
export JENKINS_HOST=https://jenkins.company.com
export JENKINS_USER=your-username
export JENKINS_TOKEN=your-api-token
```

## License

MIT License - see [LICENSE](LICENSE) for details.