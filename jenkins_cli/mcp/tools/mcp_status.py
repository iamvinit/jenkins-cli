from jenkins_cli.commands.status_cmd import status
import sys
import io

async def jenkins_status_tool(limit=10, debug=False):
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    try:
        status.callback(debug=debug, limit=limit)
        output = mystdout.getvalue()
        return {"output": output}
    except Exception as e:
        return {"error": str(e)}
    finally:
        sys.stdout = old_stdout
