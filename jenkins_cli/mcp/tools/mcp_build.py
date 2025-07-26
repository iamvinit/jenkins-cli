from jenkins_cli.commands.build_cmd import build
import sys
import io

async def jenkins_build_tool(parameters=None, watch=False, debug=False):
    # Convert parameters dict to CLI args
    params = []
    if parameters:
        for k, v in parameters.items():
            params.append(f"{k}={v}")
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    try:
        build.callback(watch=watch, debug=debug, params=params)
        output = mystdout.getvalue()
        return {"output": output}
    except Exception as e:
        return {"error": str(e)}
    finally:
        sys.stdout = old_stdout
