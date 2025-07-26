"""MCP command implementation"""
import click
import asyncio
from ..mcp.server import JenkinsMCPServer

@click.command()
@click.option('--port', default=None, help='Port to listen on (optional)')
@click.option('--host', default='localhost', help='Host to bind to')
def mcp(port, host):
    """Start Jenkins MCP server for AI tool integration"""
    click.echo("Starting Jenkins MCP server...")
    click.echo("This enables Jenkins operations through AI tools like Cursor and VS Code Copilot")
    click.echo("Press Ctrl+C to stop the server")
    
    def run_server():
        server = JenkinsMCPServer()
        asyncio.run(server.run())
    
    try:
        run_server()
    except KeyboardInterrupt:
        click.echo("\nMCP server stopped.")
