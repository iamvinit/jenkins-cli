from jenkins_cli.commands.open_cmd import open_cmd
import sys
import io

async def jenkins_open_tool(build_number=None, debug=False):
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    try:
        open_cmd.callback(debug=debug, build=build_number)
        output = mystdout.getvalue()
        return {"output": output}
    except Exception as e:
        return {"error": str(e)}
    finally:
        sys.stdout = old_stdout
