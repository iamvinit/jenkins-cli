from jenkins_cli.commands.console_cmd import console
import sys
import io

async def jenkins_console_tool(build_number=None, watch=False, debug=False):
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    try:
        console.callback(debug=debug, build=build_number, watch=watch)
        output = mystdout.getvalue()
        return {"output": output}
    except Exception as e:
        return {"error": str(e)}
    finally:
        sys.stdout = old_stdout
