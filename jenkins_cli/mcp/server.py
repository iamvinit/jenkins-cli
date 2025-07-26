
import asyncio
import json
import os
from jenkins_cli.mcp.tools import mcp_build, mcp_status, mcp_console, mcp_init, mcp_open
from jenkins_cli.mcp.auto_setup import auto_configure_jenkins, auto_initialize_job

class JenkinsMCPServer:
    def __init__(self):
        # Register available tools
        self.tools = {
            "jenkins_build": mcp_build.jenkins_build_tool,
            "jenkins_status": mcp_status.jenkins_status_tool,
            "jenkins_console": mcp_console.jenkins_console_tool,
            "jenkins_init": mcp_init.jenkins_init_tool,
            "jenkins_open": mcp_open.jenkins_open_tool,
        }

    async def handle_request(self, request_json):
        try:
            req = json.loads(request_json)
            tool = req.get("tool")
            params = req.get("params", {})
            
            # Extract and handle working directory context
            cwd = params.pop("cwd", None)
            if cwd:
                # Change to the specified directory for this request
                original_cwd = os.getcwd()
                os.chdir(cwd)
                
                # Auto-initialize project if needed
                await auto_initialize_job()
            
            if tool not in self.tools:
                return json.dumps({"result": None, "error": f"Unknown tool: {tool}"})
            
            try:
                result = await self.tools[tool](**params)
                return json.dumps({"result": result, "error": None})
            finally:
                # Restore original directory
                if cwd:
                    os.chdir(original_cwd)
                    
        except Exception as e:
            return json.dumps({"result": None, "error": str(e)})

    async def run(self):
        # Auto-configure Jenkins on server startup
        await auto_configure_jenkins()
        
        print("Jenkins MCP Server started. Awaiting requests...")
        while True:
            try:
                request_json = input()
                response = await self.handle_request(request_json)
                print(response, flush=True)
            except (EOFError, KeyboardInterrupt):
                print("Shutting down MCP server.")
                break
