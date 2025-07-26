# MCP server entry point
import asyncio
from jenkins_cli.mcp.server import JenkinsMCPServer

async def main():
    """Main entry point for Jenkins MCP server"""
    server = JenkinsMCPServer()
    await server.run()

def main_sync():
    """Synchronous wrapper for main()"""
    asyncio.run(main())

if __name__ == "__main__":
    main_sync()
